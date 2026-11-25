#!/usr/bin/env python3
"""The Moon Finally Answers Back.

One-line make.fun entry: the Moon finally replies to four billion years
of wishes, howls and 2 a.m. promises. The entry is a fixed string, so
every run writes byte-identical output to the entry file and prints the
same line to stdout.

Usage:
    python3 main.py                 # write the entry and print it
    python3 main.py --self-test     # verify the entry and the gates
    ENTRY_OUTPUT=/tmp/e.txt python3 main.py   # write somewhere else
"""

import os
import sys
import tempfile

ENTRY = "Four billion years of your wishes, howls, and 2 a.m. promises -- and not one of you has ever once wished me goodnight back."

MIN_CHARS = 1
MAX_CHARS = 240
DEFAULT_OUTPUT = "/output/entry.txt"


def entry_chars(text):
    """Character count used by the gate (Python len, same as the platform)."""
    return len(text)


def check_entry(text):
    """Raise ValueError if the text breaks any competition gate rule.

    Rules: 1-240 chars, exactly one line, no leading or trailing
    whitespace, not blank, valid UTF-8.
    """
    if not isinstance(text, str):
        raise ValueError("entry must be a string, got %s" % type(text).__name__)
    n = entry_chars(text)
    if n < MIN_CHARS or n > MAX_CHARS:
        raise ValueError("entry is %d chars, must be %d-%d" % (n, MIN_CHARS, MAX_CHARS))
    if "\n" in text:
        raise ValueError("entry must be a single line (contains newline)")
    if "\r" in text:
        raise ValueError("entry must be a single line (contains carriage return)")
    if text != text.strip():
        raise ValueError("entry has leading or trailing whitespace")
    if not text.strip():
        raise ValueError("entry must not be blank")
    text.encode("utf-8")  # raises UnicodeEncodeError if not valid UTF-8
    return n


def output_path():
    """Where the entry file goes: ENTRY_OUTPUT env var, else the default."""
    return os.environ.get("ENTRY_OUTPUT", DEFAULT_OUTPUT)


def write_entry_file(text, path):
    """Write the line with no trailing newline so the file bytes equal
    the entry exactly."""
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(text)


def read_entry_file(path):
    """Read the entry file back as bytes (for byte-identity checks)."""
    with open(path, "rb") as handle:
        return handle.read()


def summarize_entry(text):
    """One-line human summary of an entry: char count and first words."""
    words = text.split()
    preview = " ".join(words[:4])
    return "%d chars, starts %r" % (entry_chars(text), preview + " ...")


def self_test():
    """Run every gate check on the real entry and on edge cases.

    Prints a PASS/FAIL summary and returns the exit code: 0 when every
    check passes, 1 otherwise.
    """
    failures = []

    def must_pass(label, value):
        try:
            check_entry(value)
        except ValueError as exc:
            failures.append("%s: rejected (%s)" % (label, exc))

    def must_fail(label, value):
        try:
            check_entry(value)
        except (ValueError, UnicodeEncodeError):
            return
        failures.append("%s: accepted, should have been rejected" % label)

    # The real entry: exact text, exact length, passes every gate.
    expected = "Four billion years of your wishes, howls, and 2 a.m. promises -- and not one of you has ever once wished me goodnight back."
    if ENTRY != expected:
        failures.append("ENTRY text differs from the expected line")
    if entry_chars(ENTRY) != 123:
        failures.append("ENTRY is %d chars, expected 123" % entry_chars(ENTRY))
    must_pass("the entry itself", ENTRY)

    # Two independent writes must be byte-identical to the entry.
    with tempfile.TemporaryDirectory() as tmpdir:
        first_path = os.path.join(tmpdir, "first.txt")
        second_path = os.path.join(tmpdir, "second.txt")
        write_entry_file(ENTRY, first_path)
        write_entry_file(ENTRY, second_path)
        first_bytes = read_entry_file(first_path)
        second_bytes = read_entry_file(second_path)
        if first_bytes != second_bytes:
            failures.append("two writes of the entry are not byte-identical")
        if first_bytes != ENTRY.encode("utf-8"):
            failures.append("written bytes differ from ENTRY")

    # Boundary lengths: 1 and 240 pass, 0 and 241 fail.
    must_pass("1-char entry", "x")
    must_pass("240-char entry", "x" * MAX_CHARS)
    must_fail("241-char entry", "x" * (MAX_CHARS + 1))
    must_fail("empty entry", "")

    # Single-line and whitespace rules.
    must_fail("newline inside entry", "one\ntwo")
    must_fail("carriage return inside entry", "one\rtwo")
    must_fail("leading whitespace", "  padded")
    must_fail("trailing whitespace", "padded  ")
    must_fail("whitespace-only entry", "   ")

    # Wrong type.
    must_fail("non-string entry", 12345)

    if failures:
        for failure in failures:
            print("SELF-TEST FAIL: %s" % failure, file=sys.stderr)
        return 1
    print("SELF-TEST PASS: %s; all gate rules verified" % summarize_entry(ENTRY))
    return 0


def main(argv):
    if "--self-test" in argv:
        return self_test()
    check_entry(ENTRY)
    path = output_path()
    write_entry_file(ENTRY, path)
    print(ENTRY)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
