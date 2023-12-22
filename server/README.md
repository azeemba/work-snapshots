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