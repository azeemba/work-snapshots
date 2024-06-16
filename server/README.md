Work Sessiosn [Server]
======================

Depends on a react website built and available in a directory. Configure in config.conf


## Run

Make sure ../work-sessions has a recent build. You can build by running
```
npm build 
```
in that repo. That generates and puts a build in ../work-sessions/build. We use that to serve 
the frontend.

Then can run the server here:

```
python -m bottle  main --reload
```

### Alternate configuraitons 

To be accessible from mobile:

```
python -m bottle -b 0.0.0.0 main
```

While iterating on frontend, you can just run
```
npm start
```

There is a proxy configured for the react dev server
to forward requests to this server.

## Windows Setup

Created a shortcut in "C:\Users\Z\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup"

The shortcut runs run.bat

## Features Brainstorm

- Rename session
- Change session picture
- Delete picture -> Changes actual data
- Split session?
- Delete session?
- Group data by process instead of work sessions to get aggregate data?


## Data

Raw data is in a csv file that contains timestamp, process name, process title. We group them into work sessions by reading through
the whole file at startup. It's fast enough so we can leave it there.

We can create a new database to store customizations/overrides