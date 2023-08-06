import json
import logging
import sys
from pathlib import Path

import click
import fitb
from exit_codes import ExitCode

from godkjenn.artifact import Artifact
from godkjenn.vaults.fs_vault import FSVault
from godkjenn.version import __version__

log = logging.getLogger(__name__)


@click.group()
@click.option(
    "--cwd",
    "-C",
    type=click.Path(exists=True, readable=True, file_okay=False),
    default=Path("."),
    help="Directory from which to start search for the data-dir.",
)
@click.option(
    "--data-dir",
    "-d",
    default=".godkjenn",
    help="Directory (relative to --cwd) containing the vault.",
)
@click.option(
    "--verbosity",
    default="WARNING",
    help="The logging level to use.",
    type=click.Choice(
        [name for lvl, name in sorted(logging._levelToName.items()) if lvl > 0],
        case_sensitive=True,
    ),
)
@click.version_option(version=__version__)
@click.pass_context
def cli(ctx, cwd, data_dir, verbosity):
    """Command-line interface for godkjenn."""
    logging_level = getattr(logging, verbosity)
    logging.basicConfig(level=logging_level)

    godkjenn_dir = Path(cwd) / data_dir
    vault = FSVault(godkjenn_dir / "vault")
    ctx.obj = vault


@cli.command()
@click.argument("test_id")
@click.pass_obj
def accept(vault, test_id):
    """Accept the current received data for a test."""
    try:
        vault.accept(test_id)
    except KeyError:
        log.error("No received data for {}".format(test_id))
        return ExitCode.DATA_ERR

    return ExitCode.OK


@cli.command()
@click.pass_obj
def accept_all(vault):
    """Accept all received data for a configuration/root directory."""
    for test_id in vault.ids():
        try:
            vault.accept(test_id)
        except KeyError:
            # This just means there isn't any received data for the ID, just accepted.
            pass

    return ExitCode.OK


@cli.command()
@click.argument("test_id")
@click.argument("destination", type=click.File(mode="wb"))
@click.pass_obj
def accepted(vault, test_id, destination):
    """Get accepted data for a test."""
    try:
        artifact = vault.accepted(test_id)
    except KeyError:
        print(f"No accepted data for id {test_id}", file=sys.stderr)
        return ExitCode.DATA_ERR

    destination.write(artifact.data)

    return ExitCode.OK


@cli.command()
@click.argument("test_id")
@click.argument("data_source", type=click.File(mode="rb"))
@click.pass_obj
def receive(vault, test_id, data_source):
    """Receive new data for a test."""
    data = data_source.read()
    vault.receive(test_id, Artifact(data=data))

    return ExitCode.OK


@cli.command()
@click.argument("test_id")
@click.argument("destination", type=click.File(mode="wb"))
@click.pass_obj
def received(vault, test_id, destination):
    """Get received data for a test."""
    try:
        artifact = vault.received(test_id)
    except KeyError:
        print(f"No received data for {test_id}", file=sys.stderr)
        return ExitCode.DATA_ERR

    destination.write(artifact.data)

    return ExitCode.OK


@cli.command()
@click.argument("test_id")
@click.argument("differ")
@click.pass_obj
def diff(vault, test_id, differ):
    """Get received data for a test."""
    profile = fitb.Profile()
    for extension_point in fitb.load_from_pkg_resources("godkjenn"):
        profile.extension_points.add(extension_point)
    config = fitb.build_default_config(profile.options())
    differ = profile.extension_points["differ"].activate(differ, config)

    try:
        received = vault.received(test_id)
        accepted = vault.accepted(test_id)
    except KeyError:
        print(
            "Do not have both received and accepted data. No diff possible.",
            file=sys.stderr,
        )
        return ExitCode.DATA_ERR

    diff = differ(accepted, received)
    print(diff)

    return ExitCode.OK


@cli.command()
@click.option("--as-json", is_flag=True)
@click.pass_obj
def status(vault, as_json):
    """Print status of godkjenn vault"""
    status = {}
    for test_id in vault.ids():
        try:
            accepted = vault.accepted(test_id)
        except KeyError:
            accepted = None

        try:
            received = vault.received(test_id)
        except KeyError:
            received = None

        if accepted is None:
            if received is None:
                assert False, "Test ID with no information: {}".format(test_id)
            else:
                message = "initialized"
        else:
            if received is None:
                message = "up-to-date"
            elif accepted == received:
                # TODO: What about using a specialized comparator?
                message = "status-quo"
            else:
                message = "mismatch"
        status[test_id] = message

    if as_json:
        print(json.dumps(status, indent=4))
    else:
        for test_id, message in status.items():
            print(test_id, message)


def main(argv=None, standalone_mode=True):
    return cli(argv, standalone_mode=standalone_mode)


if __name__ == "__main__":
    sys.exit(main())
