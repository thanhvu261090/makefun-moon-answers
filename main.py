#!/usr/bin/env python3
"""The Moon Finally Answers Back.

Writes one line (1-240 characters) -- the Moon replying at last to the
wishes, howls and late-night promises of everyone staring up at it --
to /output/entry.txt.

Deterministic: the entry is a fixed string; every run writes byte-identical
output.
"""

import os
import sys

ENTRY = (
    "Four billion years of your wishes, howls, and 2 a.m. promises "
    "-- and not one of you has ever once wished me goodnight back."
)

MAX_CHARS = 240


def gate_check(text: str) -> None:
    """Enforce the competition gate: 1-240 chars, single line, no
    leading/trailing whitespace, non-blank, valid UTF-8."""
    if not isinstance(text, str):
        raise ValueError("entry must be a string")
    if not (1 <= len(text) <= MAX_CHARS):
        raise ValueError(f"entry is {len(text)} chars, must be 1-{MAX_CHARS}")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if text != text.strip():
        raise ValueError("entry must not have leading/trailing whitespace")
    if not text.strip():
        raise ValueError("entry must not be only whitespace")
    text.encode("utf-8")


def resolve_output_path() -> str:
    """Output path comes from ENTRY_OUTPUT, defaulting to /output/entry.txt."""
    return os.environ.get("ENTRY_OUTPUT", "/output/entry.txt")


def write_entry(text: str, out_path: str) -> None:
    """Write exactly the line, no trailing newline, so the gated file is
    byte-identical to the entry."""
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8", newline="") as f:
        f.write(text)


def run_self_test() -> int:
    """Expanded self-test: verify the entry and each gate rule.

    Covers: the exact entry text and length, byte-identical repeat
    writes, and rejection of a 241-char string, a multi-line string,
    a string with a carriage return, leading/trailing whitespace, an
    empty string, a whitespace-only string, and a non-string value.
    Returns 0 on success, 1 on any failure.
    """
    failures = []

    def expect_reject(label: str, value) -> None:
        try:
            gate_check(value)
        except ValueError:
            return
        failures.append(f"{label}: gate_check accepted it")

    def expect_accept(label: str, value) -> None:
        try:
            gate_check(value)
        except ValueError as exc:
            failures.append(f"{label}: gate_check rejected it ({exc})")

    expected = (
        "Four billion years of your wishes, howls, and 2 a.m. promises "
        "-- and not one of you has ever once wished me goodnight back."
    )
    if ENTRY != expected:
        failures.append("ENTRY does not match the expected line")
    if len(ENTRY) != len(expected):
        failures.append(f"ENTRY is {len(ENTRY)} chars, expected {len(expected)}")
    expect_accept("entry", ENTRY)

    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        p1 = os.path.join(tmp, "a.txt")
        p2 = os.path.join(tmp, "b.txt")
        write_entry(ENTRY, p1)
        write_entry(ENTRY, p2)
        with open(p1, "rb") as f:
            first = f.read()
        with open(p2, "rb") as f:
            second = f.read()
        if first != second:
            failures.append("repeat writes are not byte-identical")
        if first != ENTRY.encode("utf-8"):
            failures.append("written bytes do not match ENTRY")

    expect_accept("240-char string", "x" * 240)
    expect_reject("241-char string", "x" * 241)
    expect_accept("1-char string", "x")
    expect_reject("multi-line string", "first line\nsecond line")
    expect_reject("carriage-return string", "first line\rsecond line")
    expect_reject("leading whitespace", "  padded")
    expect_reject("trailing whitespace", "padded  ")
    expect_reject("empty string", "")
    expect_reject("whitespace-only string", "   ")
    expect_reject("non-string value", 12345)

    if failures:
        for failure in failures:
            print(f"SELF-TEST FAIL: {failure}", file=sys.stderr)
        return 1
    print(f"SELF-TEST PASS: entry {len(ENTRY)} chars, gate rules verified")
    return 0


def main() -> int:
    gate_check(ENTRY)
    out_path = resolve_output_path()
    write_entry(ENTRY, out_path)
    print(ENTRY)
    return 0


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        sys.exit(run_self_test())
    sys.exit(main())
