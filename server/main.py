from datetime import datetime
from pathlib import Path
import json
import time
import os
import signal
from threading import Thread, Lock, Event

from typing import cast

from bottle import static_file, route, request, abort, error, response
from configparser import ConfigParser

from datahandling import prep
from db_handler import Db
from fronto import makeSummaryForFrontend, makeDetailForFrontend, addWorkSessionSplits, convertTagsToResponse
from images import ImageHandler
import handle_secondary_source

config = ConfigParser()
config.read("config.conf")
imageHandler = ImageHandler(config)
frontend_dir = config["main"]["static"]


def loadData():
    print("Fetching data")
    db = Db(config)
    sessions = prep(db)
    addWorkSessionSplits(sessions, db.get_all_splits())
    summary = makeSummaryForFrontend(sessions, db.get_all_overrides(), db.get_all_tags())
    imageHandler.prepare_thumbnails(sessions)
    return sessions, summary


WORK_DATA_LOCK = Lock()
WORK_SESSIONS, WORK_SESSIONS_SUMMARY = loadData()


def refresh_data_in_background():
    while not BG_STOP_EVENT.is_set():
        BG_STOP_EVENT.wait(60)
        refresh_data()


BG_STOP_EVENT = Event()
background_thread = Thread(target=refresh_data_in_background, daemon=True)
background_thread.start()


@route("/api/tags", method="GET")
def get_tags():
    db = Db(config)
    tags = db.get_all_tags()
    print(tags)
    return convertTagsToResponse(tags)

@route("/api/tags/", method="PUT")
def addTag():
    if request.json is None:
        abort(400, "Request didn't contain valid JSON")
    request_data: dict = cast(dict, request.json)
    db = Db(config)
    db.create_tag(request_data["tag"])
    return convertTagsToResponse(db.get_all_tags())

@route("/api/tags", method="POST")
def updateTag():
    if request.json is None:
        abort(400, "Request didn't contain valid JSON")
    request_data: dict = cast(dict, request.json)
    db = Db(config)
    parent = request_data["parent"]
    tag = request_data["tag"]
    if parent:
        db.add_tag_parent(tag, parent)
    else:
        db.remove_tag_parent(tag)
    return convertTagsToResponse(db.get_all_tags())


@route("/api/worksessions/<identifier:int>/split", method="POST")
def addSplit(identifier):
    if request.json is None:
        abort(400, "Request didn't contain valid JSON")

    request_data: dict = cast(dict, request.json)
    print(request.json)
    timestamp = request_data["customStartTimestamp"]
    customStart = datetime.fromtimestamp(float(timestamp))
    db = Db(config)
    db.add_splits(identifier, customStart)

    addWorkSessionSplits(WORK_SESSIONS, [(identifier, customStart)])
    global WORK_SESSIONS_SUMMARY
    WORK_SESSIONS_SUMMARY = makeSummaryForFrontend(
        WORK_SESSIONS, db.get_all_overrides(), db.get_all_tags()
    )
    imageHandler.prepare_thumbnails(WORK_SESSIONS)
    return json.dumps(WORK_SESSIONS_SUMMARY)


@route("/api/worksessions/<identifier:int>", method="GET")
def work_session_specific(identifier):
    chosen = None
    for summary in WORK_SESSIONS_SUMMARY:
        if summary["id"] == identifier:
            chosen = summary
    return makeDetailForFrontend(WORK_SESSIONS[identifier], chosen)


@route("/api/worksessions")
def work_sessions():
    return json.dumps(WORK_SESSIONS_SUMMARY)


@route("/api/worksessions/<identifier:int>", method="POST")
def work_sessions_customize(identifier):
    if request.json is None:
        abort(400, "Request didn't contain valid JSON")
    request_data: dict = cast(dict, request.json)
    db = Db(config)
    db.add_override(identifier, request_data["title"], request_data["tag"])

    global WORK_SESSIONS_SUMMARY
    WORK_SESSIONS_SUMMARY = makeSummaryForFrontend(
        WORK_SESSIONS, db.get_all_overrides(), db.get_all_tags()
    )
    return json.dumps(WORK_SESSIONS_SUMMARY)


@route("/")
def serve_root():
    return static_file("/index.html", root=frontend_dir)


@route("/session/<session>")
def serve_root_still(session):
    return static_file("/index.html", root=frontend_dir)


@error(404)
def error404(err):
    if request.path.endswith(".webp"):
        print(f"Failed to find {request.path}")
        return static_file("StupidMissingImage.webp", root=config["main"]["cache"])


@route("/image/<timestamp>")
def serve_images(timestamp):
    response.headers['Cache-Control'] = 'max-age=3600'
    if request.query.thumbnail: # type: ignore
        imageHandler.makeSureThumbnailExists(timestamp)
        return static_file(timestamp, root=config["main"]["cache"])
    return static_file(timestamp, root=config["main"]["images"])


@route("/cache/<file>")
def serve_cached(file):
    response.headers['Cache-Control'] = 'max-age=3600'
    return static_file(file, config["main"]["cache"])


@route("/<path:path>")
def serve_static(path):
    return static_file(path, frontend_dir)


@route("/api/refresh")
def refresh_data():
    WORK_DATA_LOCK.acquire(blocking=True, timeout=1)
    try:
        handle_secondary_source.handle(config)
        global WORK_SESSIONS
        global WORK_SESSIONS_SUMMARY
        WORK_SESSIONS, WORK_SESSIONS_SUMMARY = loadData()
    finally:
        WORK_DATA_LOCK.release()


@route("/api/exit")
def exit():
    Thread(target=shutdown_server, daemon=True).start()
    return ""


def shutdown_server():
    time.sleep(1)
    pid = os.getpid()  # Get process ID of the current Python script
    os.kill(pid, signal.SIGINT)
