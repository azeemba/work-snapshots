
import time
import pathlib
import argparse
import pywinctl
import sqlite3
from contextlib import closing

from datatypes import Process

def parse_args():
    parser = argparse.ArgumentParser(description="Write windows to sqlite file")
    parser.add_argument("sqlite_file", help="Path to the sqlite file", type=pathlib.Path)
    parser.add_argument("timestamp", help="Identifier for the current time", type=str)
    parser.add_argument("-p", "--filtered-process", help="Process name(s) to filter out", action='append', default=[])
    parser.add_argument("-k", "--frequency-seconds", help="How long since the last check?", default=300)

    return parser.parse_args()

def get_current_windows(filter_list: list[str]):
    t5 = time.monotonic_ns()
    windows = pywinctl.getAllWindows()
    titleProcessMap = pywinctl.getAllAppsWindowsTitles()
    invert_dict = {}
    for process, val in titleProcessMap.items():
        if process in filter_list:
            continue

        for title in val:
            if title == "":
                # filter out processes with no title
                continue
            invert_dict[title] = process

    data: list[Process] = []
    for w in windows:
        if w.getParent() == 0 and w.title in invert_dict:
            data.append(Process(invert_dict[w.title], w.title, w.isActive))
    t6 = time.monotonic_ns()
    print(f"Pulling process data took {(t6-t5)/1e9} seconds.")

    return data

def write_processes(csv_path: pathlib.Path, processes: list[Process], timestamp: str, frequency_seconds):
    filepath = csv_path
    db_data = []
    for p in processes:
        name = p.name.replace(",", "")
        title = p.title.replace(",", "")
        isActive = "1" if p.isActive else "0"
        db_data.append((timestamp, name, title, isActive, frequency_seconds))

    with closing(sqlite3.connect(filepath)) as db:
        db.executemany("""INSERT INTO snapshot_processes
                    (datetime, process, title, isActive, recordFrequencySeconds)
                    VALUES(?, ?, ?, ?, ?)
                """, db_data)
        db.commit()


if __name__ == "__main__":
    args = parse_args()
    print(args)
    w = get_current_windows(args.filtered_process)
    print(w)

    write_processes(args.sqlite_file, w, args.timestamp, args.frequency_seconds)