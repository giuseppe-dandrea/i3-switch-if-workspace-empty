# i3 switch if workspace empty
## About
Python script using i3ipc to connect to i3wm: on window close, if the current workspace is empty, move to the first previous non empty workspace.

**N.B.** everytime you restart i3, you lose your previous history, so for the first tag will not work.

## Dependencies
1. i3ipc-python <https://github.com/acrisci/i3ipc-python>

## Installation
1. Clone the repo
2. Install i3ipc-python: `pip install i3ipc`
3. Add to your i3 config: `exec_always /parent/path/i3-switch-if-workspace-empty.py`
4. Restart i3
