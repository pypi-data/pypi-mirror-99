import difflib


def binary_diff(accepted, received):
    diff = difflib.diff_bytes(
        difflib.unified_diff, [accepted.path.read_bytes()], [received.path.read_bytes()], lineterm=b""
    )
    return "\n".join(map(str, diff))


def extension(extension_point):
    extension_point.add(name="binary", description="Differ for binary files.", activate=lambda _full, _ext: binary_diff)
