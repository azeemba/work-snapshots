from pathlib import Path
import json

from bottle import static_file, route, request, abort
from configparser import ConfigParser

from datahandling import prep 
from db_handler import Db
from fronto import makeSummaryForFrontend, makeDetailForFrontend
from images import prepare_thumbnails

config = ConfigParser()
config.read("config.conf")
db = Db(config)
root = config["main"]["static"]


def loadData():
    sessions = prep(config["main"]["data"])
    summary = makeSummaryForFrontend(sessions, db)
    prepare_thumbnails(sessions, config)
    return sessions, summary


WORK_SESSIONS, WORK_SESSIONS_SUMMARY = loadData()


@route("/api/worksessions/<identifier:int>", method="GET")
def work_session_specific(identifier):
    return makeDetailForFrontend(WORK_SESSIONS[identifier])


@route("/api/worksessions")
def work_sessions():
    return json.dumps(WORK_SESSIONS_SUMMARY)


@route("/api/worksessions/<identifier:int>", method="POST")
def work_sessions_customize(identifier):
    if request.json is None:
        abort(400, "Request didn't contain valid JSON")
    db.add_title(identifier, request.json["title"])


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
