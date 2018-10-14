#!/usr/bin/python
import i3ipc
from collections import deque

CIRCULAR_BUFFER_DIM = 10

i3 = i3ipc.Connection()

# Circular buffer containing last used workspaces id and name
WORKSPACES_LIST = deque(maxlen = CIRCULAR_BUFFER_DIM)
first_focused = i3.get_tree().find_focused()
WORKSPACES_LIST.append({'id': first_focused.workspace().id, 'name': first_focused.workspace().name})

def is_workspace_empty(workspace_id):
	workspace = i3.get_tree().find_by_id(workspace_id)
	if not workspace:
		return True
	if workspace.workspace().leaves():
		return False
	else:
		return True

# On workspace focus, add the workspace to the circular buffer
def on_workspace_focus(self, e):
	if e.current:
		WORKSPACES_LIST.append({'id': e.current.id, 'name': e.current.name})

# On window close, if the workspace is empty
# go back to the first non empty workspace
def on_window_close(self, e):
	focused = i3.get_tree().find_focused()
	if not focused.workspace().leaves():
		# If workspace empty
		for w in reversed(WORKSPACES_LIST):
			if not is_workspace_empty(w['id']):
				i3.command('workspace ' + w['name'])
				break

# Subscribing to events
i3.on('workspace::focus', on_workspace_focus)
i3.on('window::close', on_window_close)

# Start the main loop and wait for events to come in.
i3.main()