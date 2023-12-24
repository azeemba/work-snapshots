from pathlib import Path
from bottle import static_file, route
from configparser import ConfigParser
import json

from datahandling import makeSummaryForFrontend, prep, makeDetailForFrontend
from images import prepare_thumbnails

config = ConfigParser()
config.read("config.conf")
root = config["main"]["static"]


def loadData():
    sessions = prep(config["main"]["data"])
    summary = makeSummaryForFrontend(sessions)
    return sessions, summary


WORK_SESSIONS, WORK_SESSIONS_SUMMARY = loadData()
prepare_thumbnails(WORK_SESSIONS, config)


@route("/api/worksessions/<identifier:int>")
def work_session_specific(identifier):
    return makeDetailForFrontend(WORK_SESSIONS[identifier])


@route("/api/worksessions")
def work_sessions():
    return json.dumps(WORK_SESSIONS_SUMMARY)


@route("/")
def serve_root():
    return static_file("/index.html", root=root)

@route("/session/<session>")
def serve_root_still(session):
    return static_file("/index.html", root=root)


@route("/image/<timestamp>")
def serve_images(timestamp):
    return static_file(timestamp, root=config["main"]["images"])

@route("/cache/<file>")
def serve_cached(file):
    return static_file(file, config["main"]["cache"])

@route("/<path:path>")
def serve_static(path):
    return static_file(path, root)


@route("/api/refresh")
def refresh_data():
    global WORK_SESSIONS
    global WORK_SESSIONS_SUMMARY
    WORK_SESSIONS, WORK_SESSIONS_SUMMARY = loadData()
