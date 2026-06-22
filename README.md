# Basic Bot

A lightweight bot that records mouse and keyboard input and replays it later, built primarily for automated testing. It's made public so it can be accessed without requiring a GitHub login, due to a work-related constraint.

## What it does

The bot has two phases:

1. **Record** — captures mouse movement, clicks, and key presses with precise timing
2. **Replay** — plays back the recorded actions, reproducing the original timing and inputs

Both phases share a single synchronized timeline, so mouse and keyboard events stay perfectly in sync no matter how long a recording runs.

## Usage

There are two ways to control the bot:

### Console

Controlled via terminal commands. Run with `-h` to see the full list of available options and flags.

### GUI

A small always-on-top control panel with buttons for starting/stopping recording and replay, plus a clean quit option.

Three keyboard shortcuts are reserved globally (they work even when the GUI isn't focused, and are never recorded as part of a script):

| Key | Action |
|-----|--------|
| `F10` | Stop everything (recording and/or replay), keep the program running |
| `F11` | Stop everything and cleanly exit the program |
| `F12` | **Emergency stop** — kills the process immediately, no cleanup |

## Notes

- Reserved keys (`F10`–`F12`) are filtered out at the recording level, so they'll never accidentally end up baked into a replayed script.
- The emergency stop (`F12`) is intentionally abrupt, it terminates the process at the OS level rather than attempting a graceful shutdown, to guarantee it can't hang or be blocked.