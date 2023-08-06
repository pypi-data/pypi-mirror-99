import shutil
from unittest import mock

import coiled
import pytest
from click.testing import CliRunner
from coiled.cli.upload import upload

from ...utils import ExperimentalFeatureWarning
from ..utils import conda_command, parse_conda_command

if shutil.which("conda") is None:
    pytest.skip(
        "Conda is needed to upload local software environments", allow_module_level=True
    )


@pytest.mark.test_group("veryslow")
def test_upload(sample_user):
    name = "coiled-test-foo"
    fqn = f"{sample_user.account.name}/{name}"
    parse_conda_command(
        [conda_command(), "create", "-y", "-q", "--name", name, "--json", "toolz"]
    )

    assert fqn not in coiled.list_software_environments()

    runner = CliRunner()
    with pytest.warns(ExperimentalFeatureWarning):
        result = runner.invoke(upload, args=f"--name {name}")
    assert result.exit_code == 0

    assert fqn in coiled.list_software_environments()


@pytest.mark.xfail(reason="unknown")
def test_upload_raises():

    with mock.patch("os.environ"):
        runner = CliRunner()
        with pytest.warns(ExperimentalFeatureWarning):
            result = runner.invoke(upload)

    assert result.exit_code != 0
    err_msg = str(result.exception).lower()
    assert "cannot be determined" in err_msg
    assert "--name" in err_msg
    assert "activate" in err_msg
