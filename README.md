Work Snapshots
==============


Requires:
- AutoHotKey
- Python3
- Node

## Tray

Uses autohotkey to add a tray icon to control enablement/disablement.

It also runs a timer to invoke python scripts to take screenshots and record
windows/processes of interest.

### Set up for Tray

```sh
cd tray
python -m venv .venv
.venv/Scripts/pip install -r requirements.txt
```

Then you can run the AutoHotKey script which will start monitoring your windows.
If you have AutoHotKey installed, you should just be able to click on
ConstantScreenshots.ahk script to launch it.

### Config for Tray

The tray component decides when you are doing something worth recording.
It does this by checking if any programs are running that match a
hardcoded list of programs. For me they are programs that I use
for coding or graphics projects.

The tray component also has the output directory hardcoded

## Server

Python server that serves as the backend for the dashboard where you
can look through the work sessions/screenshots.

### Set up for Server

```sh
cd server
python -m venv .venv
.venv/Scripts/pip install -r requirements.txt
```

Then you can start the server with:

```sh
.venv/Scripts/python -m bottle -b 0.0.0.0 main
```
