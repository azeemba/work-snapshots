"""
Primary creates screenshots and writes to sqlite.
Secondary creates screenshots and writes JSON files that need to be merged with primary data.
This file helps with that.
"""

from pathlib import Path
from configparser import ConfigParser
import os
import shutil
from collections import defaultdict

from datetime import datetime

import json

from db_handler import Db


def should_handle_secondary(config: ConfigParser):
    return config.has_section("secondary_data") and config["secondary_data"].get(
        "location"
    )


def _find_available_snapshots(config: ConfigParser):
    if not should_handle_secondary(config):
        return defaultdict()
    # Check there is an image and a JSON file
    location = Path(config["secondary_data"]["location"])

    files = os.listdir(location)
    files_by_timestamps: dict[str, set[Path]] = defaultdict(set)

    for f in files:
        file_path = location / f
        name = file_path.stem

        # dt = datetime.strptime(name, "%Y-%m-%d_%H_%M")
        # age = (dt - datetime.now())
        # if age.total_seconds() < 60:
        #     continue

        files_by_timestamps[name].add(file_path)

    return files_by_timestamps


def _move_all_to_primary(
    files_by_timestamps: dict[str, set[Path]], config: ConfigParser
):
    db = Db(config)
    for timestamp, files in files_by_timestamps.items():
        print("Will work on: ", timestamp, files)
        _move_single_to_primary(timestamp, files, db, config)


def _move_single_to_primary(
    timestamp: str, file_paths: set[Path], db: Db, config: ConfigParser
):
    if len(file_paths) != 2:
        print("I expect json and image file but got ", file_paths)
        return

    json_file = None
    img_file = None
    for f in file_paths:
        if f.suffix.lower() == ".json":
            json_file = f
        elif f.suffix.lower() == ".webp":
            img_file = f

    if json_file is None or img_file is None:
        return

    # Steps:
    # - Write data
    # - Copy image
    # - Delete image
    # - Delete data

    try:
        _write_process_data(timestamp, json_file, db)
        _copy_image_to_primary(img_file, config)
        img_file.unlink(missing_ok=True)
        json_file.unlink(missing_ok=True)
    except Exception as e:
        print("Failed to process secondary data", e, json_file)


def _write_process_data(timestamp: str, file_path: Path, db: Db):
    data = json.loads(file_path.read_text())

    processes = data["processes"]
    frequency_seconds = data["frequencySeconds"]

    db.add_processes(processes, frequency_seconds, timestamp, source="secondary")


def _copy_image_to_primary(image: Path, config: ConfigParser):
    destination = Path(config["main"]["images"])
    shutil.copy2(image, destination)


def handle(config: ConfigParser):
    if should_handle_secondary(config):
        data = _find_available_snapshots(config)
        _move_all_to_primary(data, config)


if __name__ == "__main__":
    config = ConfigParser()
    config.read("config.conf")

    handle(config)
