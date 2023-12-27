from pathlib import Path
import json
import time
import os
import signal
from threading import Thread

from typing import cast

from bottle import static_file, route, request, abort, error
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
    summary = makeSummaryForFrontend(sessions, db.get_all_overrides())
    prepare_thumbnails(sessions, config)
    return sessions, summary


WORK_SESSIONS, WORK_SESSIONS_SUMMARY = loadData()

@route("/api/tags", method="GET")
def get_tags():
    tags = db.get_all_tags()
    print(tags)
    return tags

@route("/api/tags/", method="PUT")
def addTag():
    if request.json is None:
        abort(400, "Request didn't contain valid JSON")
    request_data: dict = cast(dict, request.json)
    db.create_tag(request_data["tag"])
    return db.get_all_tags()



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
    request_data: dict = cast(dict, request.json)
    db.add_override(identifier, request_data["title"], request_data["tag"])

    global WORK_SESSIONS_SUMMARY
    WORK_SESSIONS_SUMMARY = makeSummaryForFrontend(WORK_SESSIONS, db.get_all_overrides())
    return json.dumps(WORK_SESSIONS_SUMMARY)


@route("/")
def serve_root():
    return static_file("/index.html", root=root)


@route("/session/<session>")
def serve_root_still(session):
    return static_file("/index.html", root=root)


@error(404)
def error404(err):
    if request.path.endswith(".webp"):
        print(f"Failed to find {request.path}")
        return static_file("StupidMissingImage.webp", root=config["main"]["cache"])


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


@route("/exit")
def exit():
    Thread(target=shutdown_server).start()
    return ""


def shutdown_server():
    time.sleep(1)
    pid = os.getpid()  # Get process ID of the current Python script
    os.kill(pid, signal.SIGINT)
