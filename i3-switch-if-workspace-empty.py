#!/usr/bin/python
import i3ipc
from collections import deque

i3 = i3ipc.Connection()

# Circular buffer containing last used workspaces
WORKSPACES_LIST = deque(maxlen = 10)
WORKSPACES_LIST.append(i3.get_tree().find_focused().workspace().name)

def is_workspace_empty(workspace_name):
	workspace = i3.get_tree().find_named(workspace_name)
	if not workspace:
		return True
	if workspace[0].workspace().leaves():
		print(workspace[0].workspace().leaves())
		return False
	else:
		return True

# On workspace focus, add the workspace to the circular buffer
def on_workspace_focus(self, e):
	if e.current:
		WORKSPACES_LIST.append(e.current.name)

# On window close, if the workspace is empty
# go back to the first non empty workspace
def on_window_close(self, e):
	focused = i3.get_tree().find_focused()
	if not focused.workspace().leaves():
		# If workspace empty
		for w in reversed(WORKSPACES_LIST):
			if not is_workspace_empty(w):
				i3.command('workspace ' + w)
				break

# Subscribing to events
i3.on('workspace::focus', on_workspace_focus)
i3.on('window::close', on_window_close)

# Start the main loop and wait for events to come in.
i3.main()