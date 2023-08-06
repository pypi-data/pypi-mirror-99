import asyncio
import time
import uuid
from decimal import Decimal
from os import environ
from typing import Dict, cast
from unittest import mock

import coiled
import dask
import pytest
from dask.distributed import Client
from distributed.deploy.tests.test_local import MyWorker  # noqa: F401

from backends import ecs

from ..utils import ParseIdentifierError

pytestmark = [
    pytest.mark.django_db(transaction=True),
]


@pytest.mark.asyncio
async def test_version_error(base_user, monkeypatch):
    monkeypatch.setattr(coiled.core, "COILED_VERSION", "0.0.14")
    with pytest.raises(ImportError, match="Coiled now requires"):
        async with coiled.Cloud(asynchronous=True):
            pass


@pytest.mark.asyncio
async def test_basic(sample_user):
    async with coiled.Cloud(
        asynchronous=True,
    ) as cloud:

        assert cloud.user == sample_user.user.username
        assert sample_user.user.username in cloud.accounts
        assert cloud.default_account == sample_user.user.username


@pytest.mark.asyncio
async def test_trailing_slash(remote_access_url, sample_user):
    async with coiled.Cloud(
        server=remote_access_url + "/",
        asynchronous=True,
    ):
        pass


@pytest.mark.asyncio
async def test_server_input(remote_access_url, sample_user):
    async with coiled.Cloud(
        server=remote_access_url.split("://")[-1],
        asynchronous=True,
    ) as cloud:
        assert cloud.user == sample_user.user.username
        assert sample_user.user.username in cloud.accounts
        assert cloud.default_account == sample_user.user.username


@pytest.mark.asyncio
async def test_informative_error_org(remote_access_url, sample_user):
    with pytest.raises(PermissionError) as info:
        async with coiled.Cloud(
            server=remote_access_url.split("://")[-1],
            account="does-not-exist",
            asynchronous=True,
        ):
            pass

    assert sample_user.account.slug in str(info.value)
    assert "does-not-exist" in str(info.value)


@pytest.mark.asyncio
async def test_config(remote_access_url, sample_user):
    async with coiled.Cloud(
        user=sample_user.user.username,
        token=sample_user.user.auth_token.key,
        server=remote_access_url,
        asynchronous=True,
    ) as cloud:
        assert cloud.user == sample_user.user.username
        assert sample_user.user.username in cloud.accounts
        assert cloud.default_account == sample_user.user.username


def test_config_attribute():
    assert coiled.config == dask.config.get("coiled")


@pytest.mark.asyncio
async def test_repr(remote_access_url, sample_user):
    async with coiled.Cloud(asynchronous=True) as cloud:
        for func in [str, repr]:
            assert sample_user.user.username in func(cloud)
            assert remote_access_url in func(cloud)


@pytest.mark.asyncio
async def test__normalize_name(cloud, cleanup):
    assert cloud._normalize_name(name="foo/bar") == ("foo", "bar")
    assert cloud._normalize_name(name="bar") == (cloud.default_account, "bar")
    assert cloud._normalize_name(name="bar", context_account="baz") == ("baz", "bar")

    # Invalid name raises
    with pytest.raises(ParseIdentifierError):
        cloud._normalize_name(name="foo/bar/baz")


def test_sync(sample_user, cluster_configuration):
    with coiled.Cloud() as cloud:
        assert cloud.user == sample_user.user.username
        assert sample_user.user.username in cloud.accounts

        with coiled.Cluster(
            n_workers=0, configuration=cluster_configuration, cloud=cloud
        ) as cluster:
            assert cluster.scale(1) is None


@pytest.mark.parametrize(
    "backend_options",
    [
        {},
        pytest.param(
            {"fargate_spot": True},
            marks=pytest.mark.xfail(reason="capacity provider error"),
        ),
    ],
)
@pytest.mark.asyncio
async def test_cluster_management(
    cloud,
    sample_user,
    cluster_configuration,
    cleanup,
    backend_options,
):
    name = f"myname-{uuid.uuid4().hex}"
    result = await cloud.list_clusters()

    cluster_id = None
    try:
        cluster_id = await cloud.create_cluster(
            configuration=cluster_configuration,
            name=name,
            backend_options=backend_options,
        )

        result = await cloud.list_clusters()
        assert name in result
        await cloud.scale(cluster_id, n=1)

        async with coiled.Cluster(name=name, asynchronous=True) as cluster:
            async with Client(cluster, asynchronous=True) as client:
                await client.wait_for_workers(1)

                result = await cloud.list_clusters()
                # Check output is formatted properly
                # NOTE that if we're on AWS the scheduler doesn't really knows its
                # own public address, so we get it from the dashboard link
                if environ.get("TEST_BACKEND", "in-process") == "aws":
                    address = (
                        client.dashboard_link.replace("/status", "")
                        .replace("8787", "8786")
                        .replace("http", "tls")
                    )
                else:
                    address = client.scheduler_info()["address"]

                r = result[name]
                assert r["address"] == address
                # TODO this is returning the id of the configuration.
                # We probably don't want that
                assert isinstance(r["configuration"], int)
                assert r["dashboard_address"] == client.dashboard_link
                assert r["account"] == sample_user.user.username
                assert r["status"] == "running"

    finally:
        if cluster_id is not None:
            await cloud.delete_cluster(cluster_id=cluster_id)

    # wait for the cluster to shut down
    clusters = await cloud.list_clusters()
    for i in range(5):
        if name not in clusters:
            break
        await asyncio.sleep(1)
        clusters = await cloud.list_clusters()

    assert name not in clusters


@pytest.mark.skipif(
    not environ.get("TEST_BACKEND", "in-process") == "aws",
    reason="We need AWS",
)
@pytest.mark.asyncio
async def test_backend_option_validity(cloud_with_gpu, cluster_configuration, cleanup):
    with pytest.raises(ValueError, match="Select either fargate_spot or GPUs"):
        cluster = await cloud_with_gpu.create_cluster(
            name="gpu-cluster",
            configuration=cluster_configuration,
            worker_gpu=1,
            backend_options={"fargate_spot": True},
        )
        assert cluster


@pytest.mark.asyncio
async def test_cluster_proxied_dashboard_link(
    cloud,
    cluster_configuration,
    cleanup,
):
    # Make sure we are initially not using proxied dashboard addresses
    with dask.config.set({"coiled.dashboard.proxy": False}):
        async with coiled.Cluster(
            n_workers=1, configuration=cluster_configuration, asynchronous=True
        ) as cluster:
            async with Client(cluster, asynchronous=True) as client:
                await client.wait_for_workers(1)

                # Non-proxied dashboard address
                dashboard_address_expected = cluster._dashboard_address
                assert cluster.dashboard_link == dashboard_address_expected
                result = await cloud.list_clusters()
                dashboard_address = result[cluster.name]["dashboard_address"]
                assert dashboard_address == dashboard_address_expected

                # Switch to using proxied dashboard addresses
                with dask.config.set({"coiled.dashboard.proxy": True}):
                    cluster_id = result[cluster.name]["id"]
                    dashboard_address_expected = (
                        f"{cloud.server}/dashboard/{cluster_id}/status"
                    )
                    assert cluster.dashboard_link == dashboard_address_expected
                    result = await cloud.list_clusters()
                    dashboard_address = result[cluster.name]["dashboard_address"]
                    assert dashboard_address == dashboard_address_expected


@pytest.mark.skip(
    reason="Not working right now, and not critical at the moment. Should not block merging PRs."
)
@pytest.mark.asyncio
async def test_no_aws_credentials_warning(cloud, cluster_configuration, cleanup):
    name = "myname"
    environ["AWS_SHARED_CREDENTIALS_FILE"] = "/tmp/nocreds"
    AWS_ACCESS_KEY_ID = environ.pop("AWS_ACCESS_KEY_ID", "")
    AWS_SECRET_ACCESS_KEY = environ.pop("AWS_SECRET_ACCESS_KEY", "")
    await cloud.create_cluster(
        configuration=cluster_configuration,
        name=name,
    )

    with pytest.warns(UserWarning) as records:
        async with coiled.Cluster(name=name, asynchronous=True):
            pass

    assert (
        records[-1].message.args[0]
        == "No AWS credentials found -- none will be sent to the cluster."
    )
    del environ["AWS_SHARED_CREDENTIALS_FILE"]
    if any((AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)):
        environ["AWS_SECRET_ACCESS_KEY"] = AWS_SECRET_ACCESS_KEY
        environ["AWS_ACCESS_KEY_ID"] = AWS_ACCESS_KEY_ID


@pytest.mark.asyncio
async def test_default_account(sample_user):
    async with coiled.Cloud(
        asynchronous=True,
    ) as cloud:
        assert cloud.accounts
        assert cloud.default_account == sample_user.user.username


@pytest.mark.asyncio
async def test_cluster_class(cloud, cluster_configuration, cleanup):
    async with coiled.Cluster(
        n_workers=2, asynchronous=True, cloud=cloud, configuration=cluster_configuration
    ) as cluster:
        async with Client(cluster, asynchronous=True, timeout="120 seconds") as client:
            await client.wait_for_workers(2)

            clusters = await cloud.list_clusters()
            assert cluster.name in clusters

    # wait for the cluster to shut down
    clusters = await cloud.list_clusters()
    for i in range(5):
        if cluster.name not in clusters:
            break
        await asyncio.sleep(1)
        clusters = await cloud.list_clusters()

    assert cluster.name not in clusters


@pytest.mark.asyncio
async def test_cluster_class_overwrite(cloud, cluster_configuration, cleanup):
    await cloud.create_software_environment(
        name="new-env", container="daskdev/dask:latest"
    )
    worker_options = {"lifetime": "6001s"}
    scheduler_options = {"synchronize_worker_interval": "59s"}
    worker_cpu = 2
    # Create a cluster where we overwrite parameters in the cluster configuration
    async with coiled.Cluster(
        n_workers=1,
        configuration=cluster_configuration,
        software="new-env",  # Override software environment
        worker_cpu=worker_cpu,  # Override worker CPU
        worker_memory="8 GiB",
        worker_options=worker_options,  # Specify worker options
        scheduler_options=scheduler_options,  # Specify scheduler options
        asynchronous=True,
        cloud=cloud,
    ) as cluster:
        async with Client(cluster, asynchronous=True) as client:
            await client.wait_for_workers(1)

            # Check that worker_options were propagated
            result = await client.run(lambda dask_worker: dask_worker.lifetime == 6001)
            assert all(result.values())
            assert all(
                w["nthreads"] == worker_cpu
                for w in client.scheduler_info()["workers"].values()
            )

            # Check that scheduler_options were propagated
            result = await client.run_on_scheduler(
                lambda dask_scheduler: dask_scheduler.synchronize_worker_interval
            )
            assert result == 59


@pytest.mark.asyncio
async def test_worker_options_scheduler_options(cloud, software_env, cleanup):
    # Create cluster configuration with worker and scheduler options
    worker_options = {"lifetime": "6001s", "nthreads": 2}
    scheduler_options = {"synchronize_worker_interval": "59s"}
    await cloud.create_cluster_configuration(
        name="my-config",
        software=software_env,
        worker_options=worker_options,
        scheduler_options=scheduler_options,
    )

    async with coiled.Cluster(
        n_workers=1, asynchronous=True, cloud=cloud, configuration="my-config"
    ) as cluster:
        async with Client(cluster, asynchronous=True) as client:
            await client.wait_for_workers(1)

            # Check that worker_options were propagated
            result = await client.run(lambda dask_worker: dask_worker.lifetime == 6001)
            assert all(result.values())
            assert all(
                w["nthreads"] == 2 for w in client.scheduler_info()["workers"].values()
            )

            # Check that scheduler_options were propagated
            result = await client.run_on_scheduler(
                lambda dask_scheduler: dask_scheduler.synchronize_worker_interval
            )
            assert result == 59


@pytest.mark.skipif(
    not all(
        (
            environ.get("TEST_BACKEND", "in-process") == "aws",
            environ.get("TEST_AWS_SECRET_ACCESS_KEY", None),
            environ.get("TEST_AWS_ACCESS_KEY_ID", None),
        )
    ),
    reason="We need external AWS account credentials",
)
@pytest.mark.asyncio
async def test_worker_class(cloud, software_env, cleanup):
    # Create cluster configuration with non-standard worker class
    await cloud.create_cluster_configuration(
        name="my-config",
        software=software_env,
        worker_class="dask.distributed.Worker",  # different than the default, nanny
    )

    async with coiled.Cluster(
        n_workers=1, asynchronous=True, cloud=cloud, configuration="my-config"
    ) as cluster:

        async with Client(cluster, asynchronous=True) as client:
            await client.wait_for_workers(1)

            # Check that worker_class was used
            result = await client.run(
                lambda dask_worker: type(dask_worker).__name__ == "Worker"
            )
            assert all(result.values())


@pytest.mark.asyncio
async def test_scaling_limits(cloud, cleanup, cluster_configuration, sample_user):
    async with coiled.Cluster(
        n_workers=sample_user.membership.limit // 2 - 1,
        name="first",
        configuration=cluster_configuration,
        asynchronous=True,
        cloud=cloud,
    ) as first:
        with pytest.raises(Exception) as info:
            await first.scale(sample_user.membership.limit * 2)

        assert "limit" in str(info.value)
        assert str(sample_user.membership.limit) in str(info.value)
        assert str(sample_user.membership.limit * 2) in str(info.value)

        async with coiled.Cluster(
            n_workers=sample_user.membership.limit // 2 - 1,
            name="second",
            configuration=cluster_configuration,
            asynchronous=True,
            cloud=cloud,
        ) as second:

            # At this point with both clusters we are maxed out at 10
            # (2 schedulers, 8 workers) all with 1 cpu each.
            # There's a 10 % buffer though

            with pytest.raises(Exception) as info:
                await second.scale(sample_user.membership.limit)

            assert "limit" in str(info.value)
            assert str(sample_user.membership.limit) in str(info.value)

            # We also shouldn't be able to create a cluster at this point
            with pytest.raises(ValueError) as create_info:
                await coiled.Cluster(
                    n_workers=sample_user.membership.limit * 2,
                    name="third",
                    configuration=cluster_configuration,
                    asynchronous=True,
                    cloud=cloud,
                )
            assert "Unable to create cluster" in str(create_info)
            # This would be nice, but currently our logic is duplicated
            # in the scale and the create methods
            # assert str(sample_user.membership.limit) in str(create_info.value)

            await second.scale(1)
            await second.scale(4)


@pytest.mark.asyncio
async def test_configuration_overrides_limits(
    cloud, cleanup, cluster_configuration, sample_user
):
    # Limits is 10
    with pytest.raises(Exception) as info:
        await coiled.Cluster(
            n_workers=2,
            name="first",
            configuration=cluster_configuration,
            worker_cpu=4,
            worker_memory="8 GiB",
            scheduler_cpu=4,
            scheduler_memory="8 GiB",
            asynchronous=True,
        )
    assert "limit" in str(info.value)


@pytest.mark.asyncio
async def test_cluster_logs(cloud, cleanup, cluster_configuration, sample_user):
    async with coiled.Cluster(
        name="first",
        configuration=cluster_configuration,
        asynchronous=True,
        backend_options={"region": "us-west-1"},
    ) as cluster:
        async with Client(cluster, asynchronous=True) as client:
            await client.wait_for_workers(1)

        logs = await cluster.get_logs()
        assert "Scheduler" in logs
        assert len(logs.keys()) == 5  # Scheduler and 4 workers
        scheduler_logs = await cluster.get_logs(workers=False)
        assert len(scheduler_logs) == 1
        worker_logs = await cluster.get_logs(scheduler=False)
        assert "Scheduler" not in worker_logs


@pytest.mark.xfail(reason="ValueError not being raised for some reason")
@pytest.mark.asyncio
async def test_default_cloud(sample_user, software_env):
    with pytest.raises(Exception) as info:
        await coiled.Cluster(configuration="foo", asynchronous=True)

    assert "foo" in str(info.value)
    assert "myorg" in str(info.value)

    async with coiled.Cloud(
        asynchronous=True,
    ):
        async with coiled.Cloud(
            asynchronous=True,
        ) as cloud_2:
            await cloud_2.create_cluster_configuration(
                name="my-config",
                worker_cpu=1,
                worker_memory="2 GiB",
                software=software_env,
            )  # type: ignore
            try:
                cluster = coiled.Cluster(configuration="my-config", asynchronous=True)
                assert cluster.cloud is cloud_2
            finally:
                await cloud_2.delete_cluster_configuration(name="my-config")


@pytest.mark.asyncio
async def test_cloud_repr_html(cloud, cleanup):
    text = cloud._repr_html_()
    assert cloud.user in text
    assert cloud.server in text
    assert cloud.default_account in text


@pytest.mark.asyncio
async def test_create_and_list_cluster_configuration(
    cloud, cleanup, sample_user, software_env
):
    # TODO decide on defaults and who should own them (defaults in the REST API
    # or maybe just the sdk client)

    # Create basic cluster configuration
    # await cloud.create_cluster_configuration(name="config-1")

    # Create a more customized cluster configuration
    await cloud.create_cluster_configuration(
        name="config-2",
        software=software_env,
        worker_cpu=4,
        worker_memory="8 GiB",
        scheduler_cpu=2,
        scheduler_memory="4 GiB",
        private=True,
    )

    result = await cloud.list_cluster_configurations()
    cfg_name = f"{sample_user.account.name}/config-2"
    assert cfg_name in result
    cfg = result[cfg_name]
    assert cfg["account"] == sample_user.user.username
    assert software_env in str(cfg["scheduler"])
    assert software_env in str(cfg["worker"])

    assert "2" in str(cfg["scheduler"])
    assert "4" in str(cfg["worker"])
    assert cfg["private"] is True


@pytest.mark.asyncio
async def test_create_and_update_cluster_configuration(
    cloud, cleanup, sample_user, software_env
):
    await cloud.create_cluster_configuration(
        name="config-3",
        software=software_env,
        worker_cpu=4,
        worker_memory="8 GiB",
        scheduler_cpu=2,
        scheduler_memory="4 GiB",
    )
    expected_cfg_name = f"{sample_user.account.name}/config-3"
    result = await cloud.list_cluster_configurations()
    assert len(result) == 1
    cfg = result[expected_cfg_name]
    assert cfg["scheduler"]["cpu"] == 2
    assert cfg["worker"]["cpu"] == 4
    assert cfg["scheduler"]["memory"] == 4
    assert cfg["private"] is False

    await cloud.create_cluster_configuration(
        name="config-3",
        software=software_env,
        worker_cpu=4,
        worker_memory="8 GiB",
        scheduler_cpu=4,
        scheduler_memory="8 GiB",
        private=True,
    )
    result = await cloud.list_cluster_configurations()
    assert len(result) == 1
    cfg = result[expected_cfg_name]
    assert cfg["scheduler"]["cpu"] == 4
    assert cfg["worker"]["cpu"] == 4
    assert cfg["scheduler"]["memory"] == 8
    assert cfg["private"] is True


@pytest.mark.skipif(
    not environ.get("TEST_BACKEND", "in-process") == "aws",
    reason="This needs the ECS backend",
)
@pytest.mark.asyncio
async def test_create_and_update_cluster_configuration_validates(
    cloud_with_gpu, cleanup, sample_gpu_user, software_env
):
    with pytest.raises(Exception) as exc_info:
        await cloud_with_gpu.create_cluster_configuration(
            name="config-4",
            software=software_env,
            worker_cpu=1,
            worker_memory="111 GiB",
            scheduler_cpu=2,
            scheduler_memory="4 GiB",
        )
    result = str(exc_info)
    assert "Invalid CPU and memory" in result

    await cloud_with_gpu.create_cluster_configuration(
        name="config-4",
        software=software_env,
        worker_cpu=4,
        worker_memory="17 GiB",
        scheduler_cpu=2,
        scheduler_memory="4 GiB",
    )

    with pytest.raises(Exception) as exc_info:
        await cloud_with_gpu.create_cluster_configuration(
            name="config-4",
            software=software_env,
            worker_cpu=4,
            worker_gpu=1,
            worker_memory="21 GiB",
            scheduler_cpu=2,
            scheduler_memory="4 GiB",
        )
    result = str(exc_info)
    assert "Coiled currently does not support" in result


@pytest.mark.asyncio
async def test_cluster_configuration_with_gpu(
    cloud_with_gpu, cleanup, sample_gpu_user, software_env
):
    await cloud_with_gpu.create_cluster_configuration(
        name="config-4",
        software=software_env,
        worker_cpu=2,
        worker_gpu=1,
        worker_memory="4 GiB",
        scheduler_cpu=1,
        scheduler_memory="2 GiB",
    )
    result = await cloud_with_gpu.list_cluster_configurations()
    assert len(result) == 1
    assert result["mygpuuser/config-4"]["worker"]["gpu"] == 1


@pytest.mark.asyncio
async def test_cluster_configuration_update_gpu(
    cloud_with_gpu, cleanup, sample_gpu_user, software_env
):
    await cloud_with_gpu.create_cluster_configuration(
        name="x",
        software=software_env,
    )
    result = await cloud_with_gpu.list_cluster_configurations()
    assert not result["mygpuuser/x"]["worker"]["gpu"]

    await cloud_with_gpu.create_cluster_configuration(
        name="x",
        software=software_env,
        worker_gpu=1,
    )
    result = await cloud_with_gpu.list_cluster_configurations()
    assert result["mygpuuser/x"]["worker"]["gpu"]


@pytest.mark.asyncio
async def test_delete_cluster_configuration(cloud, cleanup, sample_user, software_env):
    # Initially no configurations
    result = await cloud.list_cluster_configurations()
    assert not result

    # Create two configurations
    await cloud.create_cluster_configuration(
        name="config-1",
        software=software_env,
        worker_cpu=1,
        worker_memory="2 GiB",
        # environment={"foo": "bar"},
    )
    await cloud.create_cluster_configuration(
        name="config-2",
        software=software_env,
        worker_cpu=2,
        worker_memory="4 GiB",
        # environment={"foo": "bar"},
    )

    result = await cloud.list_cluster_configurations()
    assert len(result) == 2

    # Delete one of the configurations
    await cloud.delete_cluster_configuration(name="config-1")
    result = await cloud.list_cluster_configurations()
    assert len(result) == 1
    assert f"{sample_user.account.name}/config-2" in result


@pytest.mark.asyncio
async def test_invalid_fargate_resources_raises(
    cloud,
    cleanup,
    cluster_configuration,
    backend,
):
    del backend["in_process"]
    if not isinstance(backend, ecs.ClusterManager):
        raise pytest.skip()

    with pytest.raises(ValueError, match="Invalid CPU and memory combination"):
        await coiled.Cluster(
            configuration=cluster_configuration,
            worker_cpu=1,
            worker_memory="64 GiB",
            asynchronous=True,
        )


@pytest.mark.skip(reason="infinite loop error")
@pytest.mark.asyncio
async def test_current_click(sample_user, clean_configuration):
    with mock.patch("coiled.utils.input") as mock_input:
        with mock.patch("click.prompt") as mock_prompt:
            mock_input.side_effect = [sample_user.user.username, "n"]
            mock_prompt.return_value = "foo"
            with pytest.raises(Exception):
                await coiled.Cloud.current()


@pytest.mark.skip(reason="infinite loop error")
@pytest.mark.asyncio
async def test_current_click_2(sample_user, clean_configuration):
    with mock.patch("coiled.utils.input") as mock_input:
        with mock.patch("click.prompt") as mock_prompt:
            mock_input.side_effect = [sample_user.user.username, "n"]
            mock_prompt.return_value = "foo"
            with pytest.raises(Exception):
                await coiled.Cluster(configuration="default", asynchronous=True)


@pytest.mark.asyncio
async def test_current(sample_user, clean_configuration):
    with dask.config.set(
        {
            "coiled.user": sample_user.user.username,
            "coiled.token": str(sample_user.user.auth_token),
        }
    ):
        await coiled.Cloud.current()
        # await coiled.Cluster(configuration="default", asynchronous=True)  # no cluster config


@pytest.mark.asyncio
async def test_default_org_username(second_user):
    async with coiled.Cloud(asynchronous=True) as cloud:
        assert cloud.default_account == second_user.user.username


@pytest.mark.asyncio
async def test_account_config(sample_user, second_account):
    with dask.config.set({"coiled.account": second_account.account.slug}):
        async with coiled.Cloud(
            asynchronous=True,
        ) as cloud:
            assert cloud.default_account == second_account.account.slug


@pytest.mark.asyncio
async def test_list_clusters_account(
    second_account, cloud, cluster_configuration, cleanup
):
    # Create cluster in first account
    await cloud.create_cluster(
        name="cluster-1",
        configuration=cluster_configuration,
    )

    # Create cluster in second account
    await cloud.create_software_environment(
        name=f"{second_account.account.slug}/env-2",
        container="daskdev/dask:latest",
    )
    await cloud.create_cluster_configuration(
        name=f"{second_account.account.slug}/config-2",
        software="env-2",
    )
    await cloud.create_cluster(
        name="cluster-2",
        configuration=f"{second_account.account.slug}/config-2",
        account=second_account.account.slug,
    )

    # Ensure account= in list_clusters filters by the specified account
    result = await cloud.list_clusters(account=second_account.account.slug)
    assert len(result) == 1
    assert "cluster-2" in result

    # Cleanup second_account since regular cleanup uses the default account
    await asyncio.sleep(
        1
    )  # Allow the scheduler time to phone home. TODO: find a better way!
    await asyncio.gather(
        *[
            cloud.delete_cluster(
                cluster_id=c["id"],
                account=second_account.account.slug,
            )
            for c in result.values()
        ]
    )


@pytest.mark.asyncio
async def test_account_options_and_overrides(
    account_with_options, cloud, cluster_configuration
):
    await cloud.create_cluster(
        name="cluster",
        configuration=cluster_configuration,
        account=account_with_options.account.slug,
    )

    result = await cloud.list_clusters(account=account_with_options.account.slug)
    assert result["cluster"]["options"] == {"region": "us-east-2"}
    await cloud.create_cluster(
        name="cluster-2",
        configuration=cluster_configuration,
        account=account_with_options.account.slug,
        backend_options={"region": "us-west-1"},
    )
    result = await cloud.list_clusters(account=account_with_options.account.slug)
    assert result["cluster-2"]["options"] == {"region": "us-west-1"}

    # Don't use the regular cleanup since it uses the default account
    await asyncio.sleep(
        1
    )  # Allow the scheduler time to phone home. TODO: find a better way!
    await asyncio.gather(
        *[
            cloud.delete_cluster(
                cluster_id=c["id"],
                account=account_with_options.account.slug,
            )
            for c in result.values()
        ]
    )


@pytest.mark.asyncio
async def test_connect_to_existing_cluster(cloud, cluster_configuration, cleanup):
    async with coiled.Cluster(
        n_workers=0, asynchronous=True, configuration=cluster_configuration
    ) as a:
        async with Client(a, asynchronous=True):
            pass  # make sure that the cluster is up

        async with coiled.Cluster(n_workers=0, asynchronous=True, name=a.name) as b:
            assert a.scheduler_address == b.scheduler_address

        async with Client(a, asynchronous=True):
            pass  # make sure that a is still up


@pytest.mark.asyncio
async def test_connect_same_name(cloud, cluster_configuration, cleanup, capsys):
    # Ensure we can connect to an existing, running cluster with the same name
    async with coiled.Cluster(
        name="foo-123",
        n_workers=0,
        asynchronous=True,
        configuration=cluster_configuration,
    ) as cluster1:
        async with coiled.Cluster(
            name="foo-123",
            asynchronous=True,
            configuration=cluster_configuration,
        ) as cluster2:
            assert cluster1.name == cluster2.name
            captured = capsys.readouterr()
            assert "using existing cluster" in captured.out.lower()
            assert cluster1.name in captured.out


@pytest.mark.asyncio
async def test_create_cluster_with_account_in_config(
    cloud, cleanup, cloud_with_account
):
    # If user sets 'account' in their coiled.yml we want to be
    # # able to create clusters without <account>/<name>
    # If jess sets 'account' to fedex list_cluster_configurations
    # should return the fedex configs.
    result = await cloud_with_account.list_cluster_configurations()
    assert "fedex/fedex-config" in result

    try:
        async with coiled.Cluster(configuration="fedex-config"):
            pass  # cluster created without any issue
    except ValueError as e:
        pytest.fail(f"Unable to find {e}")


def test_public_api_software_environments(sample_user):
    results = coiled.list_software_environments()
    assert not results

    name = "foo"
    coiled.create_software_environment(name=name, container="daskdev/dask:latest")
    results = coiled.list_software_environments()
    assert len(results) == 1
    expected_env_name = f"{sample_user.account.name}/foo"
    assert expected_env_name in results
    assert results[expected_env_name]["container"] == "daskdev/dask:latest"

    coiled.delete_software_environment(name)
    results = coiled.list_software_environments()
    assert not results


def test_public_api_cluster_configurations(sample_user, software_env):
    results = coiled.list_cluster_configurations()
    assert not results

    name = "foo"
    coiled.create_cluster_configuration(name=name, software=software_env)
    expected_cfg_name = f"{sample_user.account.name}/foo"
    results = coiled.list_cluster_configurations()
    assert len(results) == 1
    assert expected_cfg_name in results
    assert results[expected_cfg_name]["scheduler"]["software"] == software_env

    coiled.delete_cluster_configuration(name)
    results = coiled.list_cluster_configurations()
    assert not results


@pytest.mark.django_db
def test_public_api_cluster_configurations_with_gpu(sample_user, software_env):
    # should not be able to use GPUs
    assert not sample_user.account.can_use_gpus

    name = "foo"
    with pytest.raises(Exception) as e:
        coiled.create_cluster_configuration(
            name=name, software=software_env, worker_gpu=1
        )
        assert "cannot configure clusters with GPUs" in e.value.args[0]

    # Allow GPUs
    sample_user.account.can_use_gpus = True
    sample_user.account.save()

    coiled.create_cluster_configuration(name=name, software=software_env, worker_gpu=1)
    results = coiled.list_cluster_configurations()
    expected_cfg_name = f"{sample_user.account.name}/foo"
    assert len(results) == 1
    assert expected_cfg_name in results

    coiled.delete_cluster_configuration(name)


def test_public_api_clusters(sample_user, cluster_configuration):
    results = coiled.list_clusters()
    assert not results

    name = "foo"
    coiled.create_cluster(name=name, configuration=cluster_configuration)
    results = coiled.list_clusters()
    results = cast(Dict[str, Dict], results)
    assert len(results) == 1  # type: ignore
    assert name in results

    coiled.delete_cluster(name=name)
    results = coiled.list_clusters()
    assert not results


@pytest.mark.asyncio
async def test_multi_region(cloud, cluster_configuration, cleanup):
    async with coiled.Cluster(
        n_workers=1,
        name="uswest1",
        asynchronous=True,
        configuration=cluster_configuration,
        backend_options={"region": "us-west-1"},
    ) as cluster:
        async with Client(cluster, asynchronous=True):
            clusters = await cloud.list_clusters()
            assert cluster.name in clusters


@pytest.mark.asyncio
async def test_backend_options(cloud, cluster_configuration, cleanup):
    """Region is supported for now"""
    async with coiled.Cluster(
        n_workers=1,
        name="uswest2",
        asynchronous=True,
        configuration=cluster_configuration,
        backend_options={"region": "us-west-1"},
    ) as cluster:
        async with Client(cluster, asynchronous=True):
            clusters = await cloud.list_clusters()
            assert cluster.name in clusters


@pytest.mark.django_db(transaction=True)  # implied by `live_server`, but explicit
def test_public_api_clusters_wanting_gpu_but_not_having_access(
    sample_user, software_env
):
    CONFIGURATION_NAME = "foo"
    # Enable, so we can create the cluster ocnfiguration...
    sample_user.account.can_use_gpus = True
    sample_user.account.save()

    coiled.create_cluster_configuration(
        name=CONFIGURATION_NAME, software=software_env, worker_gpu=1
    )

    # Now restore to normal disabled state
    sample_user.account.can_use_gpus = False
    sample_user.account.save()

    # Assert we get an error trying to launch a cluster when we can't use GPUs
    with pytest.raises(Exception) as e:
        coiled.create_cluster(name="baz", configuration=CONFIGURATION_NAME)
    assert "cannot launch clusters with GPUs" in e.value.args[0]


def test_create_cluster_raises_exception_from_backend(
    monkeypatch, backend, cluster_configuration
):
    def fake_create_dask_cluster(*args, **kwargs):
        raise AssertionError("test assertion")

    for name, backend_manager in backend.items():
        monkeypatch.setattr(
            backend_manager, "create_dask_cluster", fake_create_dask_cluster
        )
    with pytest.raises(Exception) as e:
        coiled.create_cluster(name="foo", configuration=cluster_configuration)

    assert "test assertion" in e.value.args[0]


@pytest.mark.skip(reason="don't have s3fs on default testing configuration")
@pytest.mark.asyncio
async def test_aws_credentials(cloud, cluster_configuration, cleanup):
    s3fs = pytest.importorskip("s3fs")
    anon = s3fs.S3FileSystem(anon=True)
    try:
        anon.ls("coiled-data")
    except Exception:
        pass
    else:
        raise ValueError("Need to test against private bucket")

    s3 = s3fs.S3FileSystem()
    try:
        s3.ls("coiled-data")
    except Exception:
        # no local credentials for private bucket coiled-data
        pytest.skip()

    async with coiled.Cluster(
        n_workers=1,
        asynchronous=True,
        configuration=cluster_configuration,
    ) as a:
        async with Client(a, asynchronous=True) as client:

            def f():
                import s3fs

                s3 = s3fs.S3FileSystem()
                return s3.ls("coiled-data")

            await client.submit(f)  # ensure that this doesn't raise


@pytest.mark.asyncio
async def test_fully_qualified_names(cloud, cleanup, sample_user):
    # Ensure that fully qualified <account>/<name> can be used

    account = sample_user.user.username
    name = "foo"
    full_name = f"{account}/{name}"
    await cloud.create_software_environment(full_name, container="dask/daskdev")
    result = await cloud.list_software_environments(account)
    assert f"{sample_user.account.name}/{name}" in result

    await cloud.create_cluster_configuration(full_name, software=full_name)
    result = await cloud.list_cluster_configurations(account)
    assert f"{sample_user.account.name}/{name}" in result

    await cloud.delete_cluster_configuration(full_name)
    assert not await cloud.list_cluster_configurations(account)

    await cloud.delete_software_environment(full_name)
    assert not await cloud.list_software_environments(account)


@pytest.mark.asyncio
async def test_create_cluster_warns(cluster_configuration):
    with pytest.warns(UserWarning, match="use coiled.Cluster()"):
        coiled.create_cluster(name="foo", configuration=cluster_configuration)
    coiled.delete_cluster("foo")


@pytest.mark.skipif(
    not all(
        (
            environ.get("TEST_BACKEND", "in-process") == "aws",
            environ.get("TEST_AWS_SECRET_ACCESS_KEY", None),
            environ.get("TEST_AWS_ACCESS_KEY_ID", None),
        )
    ),
    reason="We need external AWS account credentials",
)
@pytest.mark.asyncio
async def test_aws_external_account(external_aws_account_user):
    user = external_aws_account_user
    name = "aws"
    async with coiled.Cloud(account=user.username, asynchronous=True) as cloud:
        await cloud.create_software_environment(
            name=name, container="daskdev/dask:latest"
        )  # type: ignore
        result = await cloud.list_software_environments()  # type: ignore
        assert name in result
        await cloud.create_cluster_configuration(
            name=name,
            software=name,
            worker_cpu=1,
            worker_memory="2 GiB",
            scheduler_cpu=1,
            scheduler_memory="2 GiB",
        )  # type: ignore
        result = await cloud.list_cluster_configurations()  # type: ignore
        assert name in result
        async with coiled.Cluster(
            name=name, n_workers=1, asynchronous=True, configuration=name, cloud=cloud
        ) as cluster:
            async with Client(cluster, asynchronous=True) as client:
                await client.wait_for_workers(1)
                clusters = await cloud.list_clusters()
                assert cluster.name in clusters


@pytest.mark.skipif(
    not environ.get("TEST_BACKEND", "in-process") == "aws",
    reason="We only have AWS tracking cost for now",
)
def test_public_cluster_cost_estimate(sample_user, cluster_configuration):
    costs = coiled.cluster_cost_estimate(configuration=cluster_configuration)
    assert "$" in costs
    assert "/hr" in costs
    cost = Decimal(costs[1:-3])
    assert cost > Decimal(0)


@pytest.mark.skipif(
    not environ.get("TEST_BACKEND", "in-process") == "aws",
    reason="We only have AWS tracking cost for now",
)
def test_public_cluster_cost_estimate_overrides(sample_user, cluster_configuration):
    costs = coiled.cluster_cost_estimate(
        n_workers=10,
        configuration=cluster_configuration,
        worker_cpu=4,
        worker_memory=16,
        scheduler_cpu=2,
        scheduler_memory=4,
        backend_options={"region": "us-west-1"},
    )
    assert "$" in costs
    assert "/hr" in costs
    cost = Decimal(costs[1:-3])
    assert cost > Decimal(4)


@pytest.mark.asyncio
async def test_cloud_event_loop_blocking(cloud, cleanup, sample_user, software_env):
    """
    Test making many concurrent requests doesn't block the server's event loop,
    by calling a method (that calls an API endpoint) that deliberately just does
    an asynchronous wait. If the event loop is blocked, the requests will be
    serialized and take a long time; if not, many will run concurrently.
    """

    interval = 2

    async def _wait(name):
        result = await cloud._noop_wait(interval)
        return result["waited"]

    repetitions = 20
    overall_start = time.time()
    results = await asyncio.gather(*[_wait(str(name)) for name in range(repetitions)])
    overall_end = time.time()

    # Ensure sleeps have happened concurrently
    assert (overall_end - overall_start) < (repetitions * interval)

    assert all(result < 3 for result in results)


def test_public_api_list_core_usage_table(sample_user, capfd):
    coiled.list_core_usage()
    capture = capfd.readouterr()

    assert "Account_limit" not in capture.out
    assert "10" in capture.out
    assert "Core usage" in capture.out


def test_public_api_list_core_usage_json(sample_user):
    result = coiled.list_core_usage(json=True)

    assert result["account_limit"] == 10  # type: ignore
    assert result["user_total"] == 0  # type: ignore
    assert result["account_total"] == 0  # type: ignore
    assert result["jobs_total"] == 0  # type: ignore
    assert result["clusters_total"] == 0  # type: ignore


def test_public_api_list_local_versions(sample_user, capfd):
    coiled.list_local_versions()
    capture = capfd.readouterr()

    assert "Python Version" in capture.out
    assert "Versions" in capture.out


def test_public_api_info(sample_user):
    result = coiled.info(json=True)

    assert "python_version" in result  # type: ignore
    assert "account_limit" in result  # type: ignore
