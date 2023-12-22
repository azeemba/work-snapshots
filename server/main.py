from pathlib import Path
from bottle import static_file, route
from configparser import ConfigParser
import json

from datahandling import makeSessionsSummary, prep

config = ConfigParser()
config.read("config.conf")
root = config["main"]["static"]

WORK_SESSIONS = prep(config["main"]["data"])
WORK_SESSIONS_SUMMARY = makeSessionsSummary(WORK_SESSIONS)

@route("/")
def serve_root():
    return static_file("/index.html", root=root)


@route("/<path:path>")
def serve_static(path):
    return static_file(path, root)

@route("/api/worksessions")
def work_sessions():
    return json.dumps(WORK_SESSIONS_SUMMARY)