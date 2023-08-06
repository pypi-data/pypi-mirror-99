import json
import logging
import subprocess
import sys

import fitb
from rich.console import Console
from rich.table import Table

import godkjenn
from godkjenn.verification import MismatchError, verify

log = logging.getLogger(__name__)


def diff(vault, test_id, differ):
    """Get diff for a test.

    Args:
        vault: The FSVault to use.
        test_id: The ID of the test to diff.
        differ: The diffing algorithm to use.

    Returns: A string-able object representing the diff.

    Raises:
        KeyError: The vault does not contain both accepted and received data for the test.
    """
    profile = fitb.Profile()
    for extension_point in fitb.load_from_pkg_resources("godkjenn"):
        profile.extension_points.add(extension_point)
    config = fitb.build_default_config(profile.options())
    differ = profile.extension_points["differ"].activate(differ, config)

    try:
        received = vault.received(test_id)
        accepted = vault.accepted(test_id)
    except KeyError:
        raise KeyError("Do not have both received and accepted data. No diff possible.")

    return differ(accepted, received)


def status(vault, as_json=False, stream=sys.stdout, include_up_to_date=False):
    """Print status of godkjenn vault"""

    def artifacts():
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
                    if not include_up_to_date:
                        continue
                    message = "up-to-date"
                elif accepted == received:
                    # TODO: What about using a specialized comparator?
                    message = "status-quo"
                else:
                    message = "mismatch"

            yield test_id, message

    status = dict(artifacts())

    if as_json:
        json.dump(status, fp=stream, indent=4)
        return

    if not status:
        return

    table = Table()
    table.add_column("Test ID")
    table.add_column("Status")
    for test_id, message in status.items():
        table.add_row(test_id, message)
    console = Console(file=stream)
    console.print(table)


def review(vault, command_template):
    for artifact_id in vault.ids():
        try:
            accepted = vault.accepted(artifact_id)
            received = vault.received(artifact_id)
        except KeyError:
            continue

        command = command_template.format(received=received, accepted=accepted)
        subprocess.run(command.split())

        # This compares the *new* state of the two artifacts. If they match, then the received data will be removed as a
        # result.
        try:
            verify(
                vault,
                godkjenn.comparators.exact.compare,
                artifact_id,
                received.path.read_bytes(),
                received.mime_type,
                received.encoding,
            )
        except MismatchError:
            pass
