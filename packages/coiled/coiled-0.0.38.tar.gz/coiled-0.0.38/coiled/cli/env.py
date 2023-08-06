import pprint

import click

from ..core import (
    Cloud,
    create_software_environment,
    delete_software_environment,
    list_software_environments,
)
from .utils import CONTEXT_SETTINGS


@click.group(context_settings=CONTEXT_SETTINGS)
def env():
    """Commands for managing Coiled software environments"""
    pass


@env.command(context_settings=CONTEXT_SETTINGS)
@click.option(
    "-n", "--name", help="Name of software environment, it must be lowercase."
)
@click.option("--container", default=None, help="Base docker image to use.")
@click.option(
    "--conda",
    default=None,
    help="Conda environment file.",
    type=click.Path(exists=True),
)
@click.option(
    "--pip", default=None, help="Pip requirements file.", type=click.Path(exists=True)
)
@click.option(
    "--post-build",
    default=None,
    help="Post-build script.",
    type=click.Path(exists=True),
)
def create(name, container, conda, pip, post_build):
    """Create a Coiled software environment"""
    create_software_environment(
        name=name, container=container, conda=conda, pip=pip, post_build=post_build
    )


@env.command(context_settings=CONTEXT_SETTINGS)
@click.argument("name")
def delete(name: str):
    """Delete a Coiled software environment"""
    delete_software_environment(name)


@env.command(context_settings=CONTEXT_SETTINGS)
@click.argument("account", default=None, required=False)
def list(account: str):
    """List the Coiled software environments in an account"""
    pprint.pprint(list_software_environments(account))


@env.command(
    context_settings=CONTEXT_SETTINGS,
    help="View the details of a Coiled software environment",
)
@click.argument("name")
def inspect(name: str):
    """View the details of a Coiled software environment

    Parameters
    ----------
    name
        Identifier of the software environment to use, in the format (<account>/)<name>. If the software environment
        is owned by the same account as that passed into "account", the (<account>/) prefix is optional.

        For example, suppose your account is "wondercorp", but your friends at "friendlycorp" have an environment
        named "xgboost" that you want to use; you can specify this with "friendlycorp/xgboost". If you simply
        entered "xgboost", this is shorthand for "wondercorp/xgboost".

        The "name" portion of (<account>/)<name> can only contain ASCII letters, hyphens and underscores.

    Examples
    --------
    >>> import coiled
    >>> coiled.inspect("coiled/default")

    """
    with Cloud() as cloud:
        results = cloud.get_software_info(name)
        for key in ["container", "conda", "pip", "post_build"]:
            print(f"{key}:")
            pprint.pprint(results.get(key, {}))  # type: ignore
            print("\n")
