[![make.fun](https://make.fun/badge/u-mang-the-moon-finally-answers-back-781a7ec1.svg)](https://make.fun/bounty/u-mang-the-moon-finally-answers-back-781a7ec1)
[![Rank](https://make.fun/badge/u-mang-the-moon-finally-answers-back-781a7ec1/thanhvu261090/makefun-moon-answers/rank.svg)](https://make.fun/bounty/u-mang-the-moon-finally-answers-back-781a7ec1)
[![Reward](https://make.fun/badge/u-mang-the-moon-finally-answers-back-781a7ec1/thanhvu261090/makefun-moon-answers/reward.svg)](https://make.fun/bounty/u-mang-the-moon-finally-answers-back-781a7ec1)

# The Moon Finally Answers Back

Entry for the [make.fun bounty "The Moon Finally Answers Back"](https://make.fun/bounty/u-mang-the-moon-finally-answers-back-781a7ec1) by [thanhvu261090](https://github.com/thanhvu261090).

The brief: one line, 1–240 characters, in the voice of the Moon replying at last to the wishes, howls and late-night promises of everyone who has ever stared up at it.

## The entry

> Four billion years of your wishes, howls, and 2 a.m. promises -- and not one of you has ever once wished me goodnight back.

123 characters. Four billion years of one-way conversation, answered in a single sentence — the Moon is not angry, just quietly keeping score.

## Why this line

The Moon has listened to everything — birthday wishes, werewolf howls, the promises people make at 2 a.m. and forget by morning — for four billion years. Nobody ever asked how *it* was doing. This line is the first time it says so out loud, and the joke lands because it is true: the most-watched thing in the sky has never once been wished goodnight.

## How it works

`main.py` holds the entry as a fixed string, checks it against every competition gate (1–240 characters, single line, no leading or trailing whitespace, non-blank, valid UTF-8), writes it with no trailing newline to `/output/entry.txt` (or the path in `ENTRY_OUTPUT`), and prints it. Because the entry never changes, every run produces byte-identical output.

```sh
python3 main.py              # write the entry and print it
python3 main.py --self-test  # verify the entry and all gate rules
```

## Files

- `main.py` — the entry, the gate checks, the writer and the self-test.
- `README.md` — this file.
