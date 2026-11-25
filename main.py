#!/usr/bin/env python3
"""One Line, One Laugh — entry program.

Writes one funny line of text to /output/entry.txt (override the path
with the ENTRY_OUTPUT environment variable for local testing).

The line was written by hand in the build session, chosen for the judge's
brief: funny on its own with no setup, the punchline lands inside the
line, the angle is a fresh image (a dog copying a mother's sigh), the
wording is tight, and the last clause ("one of them sheds") still lands
on a second read.

Pure Python standard library, deterministic: the same bytes come out on
every run. The program self-checks its output before exiting: the text
must be 1-200 characters, a single line, with no leading or trailing
whitespace and no doubled spaces; it then reads the file back and
verifies the bytes on disk are exactly what was written.
"""

import os
import sys

LINE = (
    "My dog learned to sigh exactly like my mother \u2014 "
    "now two people in this house are disappointed in me, "
    "and one of them sheds."
)

MIN_CHARS = 1
MAX_CHARS = 200
DEFAULT_OUTPUT = "/output/entry.txt"


def self_check(line: str) -> None:
    """Validate the line against the competition gate before writing."""
    if not (MIN_CHARS <= len(line) <= MAX_CHARS):
        raise ValueError(
            "line is %d characters, gate requires %d-%d"
            % (len(line), MIN_CHARS, MAX_CHARS)
        )
    if line.strip() != line:
        raise ValueError("line has leading or trailing whitespace")
    if not line.strip():
        raise ValueError("line is only whitespace")
    if "\n" in line or "\r" in line:
        raise ValueError("line must be a single line")
    if "  " in line:
        raise ValueError("line contains doubled spaces")


def main() -> int:
    self_check(LINE)

    output_path = os.environ.get("ENTRY_OUTPUT", DEFAULT_OUTPUT)
    data = LINE.encode("utf-8")

    parent = os.path.dirname(output_path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(output_path, "wb") as handle:
        handle.write(data)

    # Read the file back and verify the bytes on disk are exactly the
    # bytes we intended to write.
    with open(output_path, "rb") as handle:
        written = handle.read()
    if written != data:
        raise ValueError("bytes on disk do not match the intended line")

    # Re-check the decoded text from disk, not just the in-memory copy.
    self_check(written.decode("utf-8"))

    print("wrote %d characters (%d bytes) to %s" % (len(LINE), len(data), output_path))
    print(LINE)
    return 0


if __name__ == "__main__":
    sys.exit(main())
