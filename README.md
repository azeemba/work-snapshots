Work Snapshots
==============

If [Windows Recall](https://www.theverge.com/2024/6/13/24178144/microsoft-windows-ai-recall-feature-delay)
was not secure enough for you, here is the same feature set implemented by a random guy who you should trust
even less.

Features:
- Take screenshots evey few mins if any "important" application is running
  - A camera sound is played everytime a screenshot is taken
- Configure which applications count as important
- Tag a collection of snapshots with a project to track time spent on different projects
- Manually disable recording even when "important" applications are running

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

### Config for Server

`server/config.conf` has a few different parameters that can be configured.

Some important things:

- Where the frontend code is
- Where the sqlite database is
- Where the screenshots are


## UI

React based frontend to peruse work sessions and individual snapshots.

### Set up for UI

```sh
cd ui
npm install
npm run build
```