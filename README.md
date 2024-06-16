Work Snapshots
==============

If [Windows Recall](https://www.theverge.com/2024/6/13/24178144/microsoft-windows-ai-recall-feature-delay)
was not secure enough for you, here is the same feature set implemented by a
random guy who you should trust even less.

I built this so I could have a fun record of my progress through my side projects.
Though, it has also turned out to be useful in tracking the time I spend on different projects.

### Features
- Take screenshots evey few mins if any "interesting" application is running
  - A camera sound is played everytime a screenshot is taken
  - You can configure which applications count as "interesting"
- Add tags for different project to track time spent on them
- Manually disable recording even when "interesting" applications are running


### Screenshots

The home page of the dashboard shows a set of "work sessions" which is a series
of snapshots grouped together. So you know how long you worked on a specific thing
at a time.

![Website showing a list of clickable cards](demo/ui-home.png)
Each session can be tagged with a project.

You can also see your activity in aggregate in the "Stats" page. This
shows you a "heatmap" of how active you were on each day. It also
gives you a table to show you how much time you have spent on different projects.

![Website showing tables of activity time](demo/ui-stats.png)


By default, snapshots are taken when you are working on any applications
that match a hardcoded list. You can disable recording even
when those applications are open by clicking "Force Ignore Activity"

![Tray Icon showing a list of options](demo/tray.png)

### Problems
- Set up is manual (need to create two python virtual environments and a node environment)
- Windows only
- Screenshots and process data is stored in plaintext! You have to make sure sensitive
things aren't getting recorded.

### Requires:
- AutoHotKey
- Python3
- Node


## Tray

Uses autohotkey to add a tray icon to control enablement/disablement.

It also runs a timer to invoke python scripts to take screenshots and record
windows/processes of interest.

### Config for Tray

The tray component decides when you are doing something worth recording.
It does this by checking if any programs are running that match a
hardcoded list of programs. For me they are programs that I use
for coding or graphics projects.

The tray component also has the output directory hardcoded. This must be
updated before running.

### Set up for Tray

```sh
cd tray
python -m venv .venv
.venv/Scripts/pip install -r requirements.txt
```

Then you can run the AutoHotKey script which will start monitoring your windows.
If you have AutoHotKey installed, you should just be able to click on
ConstantScreenshots.ahk script to launch it.


## Server

Python server that serves as the backend for the dashboard where you
can look through the work sessions/screenshots.

### Config for Server

`server/config.conf` has a few different parameters that can be configured.

Some important things that must be changed first:

- Where the sqlite database should be
- Where the screenshots are stored

### Set up for Server

```sh
cd server
python -m venv .venv
.venv/Scripts/pip install -r requirements.txt
# Also create the sqlite database
.venv/Scripts/python setup_db.py
```

Then you can start the server with:

```sh
.venv/Scripts/python -m bottle -b 0.0.0.0 main
```

## UI

React based frontend to peruse work sessions and individual snapshots.

### Set up for UI

```sh
cd ui
npm install
npm run build
```


## FAQs

### Why windows only?

It's hard to write generic logic to pull information on what UI applications the user is
running.

`server/` and `ui/` are fully generic. You would only have to replace the `tray/` part
if you wanted to make it work on another platform.

### Can I request a feature? Can I send you a PR?

You can open an issue if you want ideas or pointers on how to implement something. It's
very unlikely that I am going to implement it.

I am also unlikely to accept major PRs here.
Feel free to fork this project and make your own version! 
You can share your forks in issues as well.
