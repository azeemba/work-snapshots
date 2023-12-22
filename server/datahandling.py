import csv
from datetime import datetime, timedelta
from dataclasses import dataclass
from collections import defaultdict
from pathlib import Path
import time

from typing import Any


@dataclass
class Process:
    timestamp: datetime
    timestamp_original: str
    process: str
    title: str
    isActive: bool


Snapshots = dict[datetime, list[Process]]


@dataclass
class WorkSession:
    identifier: int
    start: datetime
    end: datetime
    duration: timedelta
    preferred_title: str
    preferred_image: str
    snapshots: Snapshots

    @staticmethod
    def pickTitle(snapshots: Snapshots) -> str:
        # choose window most active
        # Assumes that title don't change for important activity
        active_counts = defaultdict(int)
        for processes in snapshots.values():
            for p in processes:
                if p.isActive:
                    active_counts[p.title] += 1

        max_title = ""
        max_count = 0
        for title, count in active_counts.items():
            if count > max_count:
                max_count = count
                max_title = title
        return max_title

    @staticmethod
    def pickImageTimestamp(snapshots: Snapshots, mostActiveTitle: str) -> str:
        timesteps = list(snapshots.keys())
        mid = len(timesteps) // 2
        for i in range(mid, 0, -1):
            # start in the middle
            # and look for a timestep where mostActiveTitle is active
            processes = snapshots[timesteps[i]]
            for p in processes:
                if p.title == mostActiveTitle and p.isActive:
                    return p.timestamp_original

        return ""


WorkSessionsDict = dict[int, WorkSession]


def strToDatetime(name):
    dt = datetime.strptime(name, "%Y-%m-%d_%H_%M")
    return dt


def prep(filepath, config=None) -> WorkSessionsDict:
    groupedByTime = readData(filepath, config)
    sessions = groupIntoSessions(groupedByTime, config)
    return sessions


def makeSummaryForFrontend(workSessions: WorkSessionsDict):
    lightSessions = []
    for identifier, w in workSessions.items():
        duration_minutes = w.duration.total_seconds() / 60
        if duration_minutes < 20:
            continue
        lightSessions.append(
            {
                "id": w.identifier,
                "start": w.start.timestamp(),
                "end": w.end.timestamp(),
                "display_time": f"{w.start.strftime('%b %d, %Y %I:%M %p')} - {w.end.strftime('%I:%M %p')}",
                "duration_minutes": duration_minutes,
                "title": w.preferred_title,
                "image": f"/image/{w.preferred_image}.webp",
            }
        )
    lightSessions.sort(key=lambda x: x["start"], reverse=True)
    return lightSessions


def makeDetailForFrontend(workSession: WorkSession):
    detailed_snapshots = {}
    for timestamp, processes in workSession.snapshots.items():
        if not processes:
            continue
        current = []
        timestamp = processes[0].timestamp
        timestamp_original = processes[0].timestamp_original
        for p in processes:
            current.append(
                {"process": p.process, "title": p.title, "active": p.isActive}
            )

        detailed_snapshots[timestamp.timestamp()] = {
            "display_time": timestamp.strftime("%b %d, %Y %I:%M %p"),
            "image": f"/image/{timestamp_original}.webp",
            "processes": current,
        }
    return detailed_snapshots


def readData(filepath, config=None) -> Snapshots:
    start = time.monotonic_ns()
    byTime = defaultdict(list)
    with open(filepath, "r", encoding="utf-8-sig") as csvfile:
        dialect = csv.Sniffer().sniff(csvfile.read(1024))
        csvfile.seek(0)
        reader = csv.DictReader(csvfile, dialect=dialect)
        count = 0
        for row in reader:
            dt = strToDatetime(row["Datetime"])
            p = Process(
                dt,
                row["Datetime"],
                row["Process"],
                row["Title"],
                row["IsActive"] == "1",
            )
            byTime[dt].append(p)
            count += 1
            if count == 5:
                print(byTime)

    print(f"Took {(time.monotonic_ns() - start)/1e9} seconds to read all data")
    return byTime


def groupIntoSessions(groupedByTime: Snapshots, config=None) -> WorkSessionsDict:
    start = time.monotonic_ns()
    timeout_minutes = 60
    if config is not None:
        timeout_minutes = config["filter"]["session_timeout_minutes"]

    timeout_delta = timedelta(minutes=timeout_minutes)

    sessions = {}

    start_timestamp = datetime.min
    last_timestamp = datetime.min
    current_session: Snapshots = {}
    count = 0

    def make_work_session():
        # We lambda capture a whole bunch of things but we need to
        # because we need to use it in the for loop AND outside the for loop
        title = WorkSession.pickTitle(current_session)
        return WorkSession(
            count,
            start_timestamp,
            last_timestamp,
            last_timestamp - start_timestamp,
            title,
            WorkSession.pickImageTimestamp(current_session, title),
            current_session,
        )

    for timestamp in groupedByTime.keys():
        if (timestamp - last_timestamp) > timeout_delta:
            if start_timestamp != datetime.min:
                workSess = make_work_session()
                sessions[count] = workSess
            start_timestamp = timestamp
            last_timestamp = timestamp
            current_session: Snapshots = {}
            count += 1
        else:
            current_session[timestamp] = groupedByTime[timestamp]
            last_timestamp = timestamp

    sessions[count] = make_work_session()
    print(
        f"Took {(time.monotonic_ns() - start)/1e9} seconds to group all data ({len(sessions)} sessions)"
    )

    return sessions
