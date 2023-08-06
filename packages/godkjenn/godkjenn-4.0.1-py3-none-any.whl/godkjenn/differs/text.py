import difflib
from functools import partial


def text_diff(extension_config, accepted, received):
    accepted_text = accepted.path.read_text(encoding=accepted.encoding)

    received_text = received.path.read_text(encoding=received.encoding)

    from io import StringIO

    diff = difflib.unified_diff(list(StringIO(accepted_text)), list(StringIO(received_text)), lineterm="")

    return "\n".join(diff)


def extension(extension_point):
    extension_point.add(
        name="text",
        description="Differ for text files.",
        config_options=(),
        activate=lambda _, ext: partial(text_diff, ext),
    )
