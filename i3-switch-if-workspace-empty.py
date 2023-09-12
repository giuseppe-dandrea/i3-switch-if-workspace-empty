#!/usr/bin/python
import i3ipc
import sys
from collections import deque

CIRCULAR_BUFFER_DIM = 12
KEEP_SAME_OUTPUT = False

HELP = """
Usage: i3-switch-if-worskpace-empty [options]
Options:
	--help					Display this information.
	--keep-same-output		Switch to the first previous non empty workspace only in the same output.
	
For bug reporting please open an issue on github repo:
<https://github.com/giuseppe-dandrea/i3-switch-if-workspace-empty/>"""

if len(sys.argv) == 2:
	if sys.argv[1] == "--keep-same-output":
		KEEP_SAME_OUTPUT = True
	elif sys.argv[1] == "--help":
		print(HELP)
		exit(0)
	else:
		print("Unrecognized option. Use --help for info.")
		exit(1)

i3 = i3ipc.Connection()

# Circular buffer containing last used workspaces id and name
WORKSPACES_LIST = deque(maxlen = CIRCULAR_BUFFER_DIM)
first_focused = i3.get_tree().find_focused()
WORKSPACES_LIST.append({'id': first_focused.workspace().id, 'name': first_focused.workspace().name})

def init_ws_map(wlist):
	tmp = dict()
	for ws in wlist:
		tmp[ws.name] = ws.output
	return tmp

def is_same_output(wmap, wname1, wname2):
	if wname1 == wname2:
		return True

	OUTPUT1 = wmap.get(wname1, "")
	OUTPUT2 = wmap.get(wname2, "")

	return OUTPUT1 == OUTPUT2

def is_workspace_empty(workspace_id):
	workspace = i3.get_tree().find_by_id(workspace_id)
	return not workspace or not workspace.workspace().leaves()

# On workspace focus, add the workspace to the circular buffer
def on_workspace_focus(self, e):
	if e.current:
		new_ws = {'id': e.current.id, 'name': e.current.name}
		try:
			WORKSPACES_LIST.remove(new_ws)
		except ValueError:
			pass
		WORKSPACES_LIST.append({'id': e.current.id, 'name': e.current.name})

# On window close, if the workspace is empty
# go back to the first non empty workspace
def on_window_close(self, e):
	focused = i3.get_tree().find_focused()
	if not focused.workspace().leaves():
		# If workspace empty
		wmap = init_ws_map(i3.get_workspaces())
		for w in reversed(WORKSPACES_LIST):
			if not is_workspace_empty(w['id']):
				if KEEP_SAME_OUTPUT and not is_same_output(wmap, w['name'], focused.workspace().name):
					continue
				i3.command('workspace ' + w['name'])
				break

# Subscribing to events
i3.on('workspace::focus', on_workspace_focus)
i3.on('window::close', on_window_close)

# Start the main loop and wait for events to come in.
i3.main()
