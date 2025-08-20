from datetime import datetime
from pathlib import Path
import time
import os
import signal
from threading import Thread, Lock, Event

from typing import cast

from flask import Flask, request, abort, jsonify, send_from_directory
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

app = Flask(__name__)


def loadData():
    print("Fetching data")
    db = Db(config)
    sessions = prep(db)
    addWorkSessionSplits(sessions, db.get_all_splits())
    summary = makeSummaryForFrontend(sessions, db.get_all_overrides(), db.get_all_tags())
    imageHandler.prepare_thumbnails(sessions)
    return sessions, summary


WORK_DATA_LOCK = Lock()
DB_LOCK = Lock()  # Protects database operations for extra safety
WORK_SESSIONS, WORK_SESSIONS_SUMMARY = loadData()


def refresh_data_in_background():
    while not BG_STOP_EVENT.is_set():
        BG_STOP_EVENT.wait(60)
        refresh_data()


BG_STOP_EVENT = Event()
background_thread = Thread(target=refresh_data_in_background, daemon=True)
background_thread.start()


@app.route("/api/tags", methods=["GET"])
def get_tags():
    with DB_LOCK:
        db = Db(config)
        tags = db.get_all_tags()
        print(tags)
        return convertTagsToResponse(tags)

@app.route("/api/tags/", methods=["PUT"])
def addTag():
    if request.json is None:
        abort(400, "Request didn't contain valid JSON")
    request_data: dict = cast(dict, request.json)
    with DB_LOCK:
        db = Db(config)
        db.create_tag(request_data["tag"])
        return convertTagsToResponse(db.get_all_tags())

@app.route("/api/tags", methods=["POST"])
def updateTag():
    if request.json is None:
        abort(400, "Request didn't contain valid JSON")
    request_data: dict = cast(dict, request.json)
    with DB_LOCK:
        db = Db(config)
        parent = request_data["parent"]
        tag = request_data["tag"]
        if parent:
            db.add_tag_parent(tag, parent)
        else:
            db.remove_tag_parent(tag)
        return convertTagsToResponse(db.get_all_tags())


@app.route("/api/worksessions/<int:identifier>/split", methods=["POST"])
def addSplit(identifier):
    if request.json is None:
        abort(400, "Request didn't contain valid JSON")

    request_data: dict = cast(dict, request.json)
    print(request.json)
    timestamp = request_data["customStartTimestamp"]
    customStart = datetime.fromtimestamp(float(timestamp))
    with DB_LOCK:
        db = Db(config)
        db.add_splits(identifier, customStart)

    with WORK_DATA_LOCK:
        addWorkSessionSplits(WORK_SESSIONS, [(identifier, customStart)])
        global WORK_SESSIONS_SUMMARY
        WORK_SESSIONS_SUMMARY = makeSummaryForFrontend(
            WORK_SESSIONS, db.get_all_overrides(), db.get_all_tags()
        )
        imageHandler.prepare_thumbnails(WORK_SESSIONS)
        return jsonify(WORK_SESSIONS_SUMMARY)


@app.route("/api/worksessions/<int:identifier>", methods=["GET"])
def work_session_specific(identifier):
    with WORK_DATA_LOCK:
        chosen = None
        for summary in WORK_SESSIONS_SUMMARY:
            if summary["id"] == identifier:
                chosen = summary
        return makeDetailForFrontend(WORK_SESSIONS[identifier], chosen)


@app.route("/api/worksessions")
def work_sessions():
    with WORK_DATA_LOCK:
        return jsonify(WORK_SESSIONS_SUMMARY)


@app.route("/api/worksessions/<int:identifier>", methods=["POST"])
def work_sessions_customize(identifier):
    if request.json is None:
        abort(400, "Request didn't contain valid JSON")
    request_data: dict = cast(dict, request.json)
    with DB_LOCK:
        db = Db(config)
        db.add_override(identifier, request_data["title"], request_data["tag"])

    with WORK_DATA_LOCK:
        global WORK_SESSIONS_SUMMARY
        WORK_SESSIONS_SUMMARY = makeSummaryForFrontend(
            WORK_SESSIONS, db.get_all_overrides(), db.get_all_tags()
        )
        return jsonify(WORK_SESSIONS_SUMMARY)


@app.route("/")
def serve_root():
    return send_from_directory(frontend_dir, "index.html")


@app.route("/session/<session>")
def serve_root_still(session):
    return send_from_directory(frontend_dir, "index.html")


@app.errorhandler(404)
def error404(err):
    if request.path.endswith(".webp"):
        print(f"Failed to find {request.path}")
        return send_from_directory(config["main"]["cache"], "StupidMissingImage.webp")


@app.route("/image/<timestamp>")
def serve_images(timestamp):
    if request.args.get('thumbnail'):
        imageHandler.makeSureThumbnailExists(timestamp)
        response = send_from_directory(config["main"]["cache"], timestamp)
    else:
        response = send_from_directory(config["main"]["images"], timestamp)
    response.headers['Cache-Control'] = 'max-age=3600'
    return response


@app.route("/cache/<file>")
def serve_cached(file):
    response = send_from_directory(config["main"]["cache"], file)
    response.headers['Cache-Control'] = 'max-age=3600'
    return response


@app.route("/<path:path>")
def serve_static(path):
    return send_from_directory(frontend_dir, path)


@app.route("/api/refresh")
def refresh_data():
    WORK_DATA_LOCK.acquire(blocking=True, timeout=1)
    try:
        handle_secondary_source.handle(config)
        global WORK_SESSIONS
        global WORK_SESSIONS_SUMMARY
        WORK_SESSIONS, WORK_SESSIONS_SUMMARY = loadData()
    finally:
        WORK_DATA_LOCK.release()


@app.route("/api/exit")
def exit():
    Thread(target=shutdown_server, daemon=True).start()
    return ""


def shutdown_server():
    time.sleep(1)
    pid = os.getpid()  # Get process ID of the current Python script
    os.kill(pid, signal.SIGINT)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081, threaded=True, debug=False)
