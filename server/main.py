from pathlib import Path
from bottle import static_file, route
from configparser import ConfigParser
import json

from datahandling import makeSummaryForFrontend, prep, makeDetailForFrontend

config = ConfigParser()
config.read("config.conf")
root = config["main"]["static"]

WORK_SESSIONS = prep(config["main"]["data"])
WORK_SESSIONS_SUMMARY = makeSummaryForFrontend(WORK_SESSIONS)

@route("/api/worksessions/<identifier:int>")
def work_session_specific(identifier):
    return makeDetailForFrontend(WORK_SESSIONS[identifier])


@route("/api/worksessions")
def work_sessions():
    return json.dumps(WORK_SESSIONS_SUMMARY)


@route("/")
def serve_root():
    return static_file("/index.html", root=root)

@route("/image/<timestamp>")
def serve_images(timestamp):
    return static_file(timestamp, root=config["main"]["images"])

@route("/<path:path>")
def serve_static(path):
    return static_file(path, root)