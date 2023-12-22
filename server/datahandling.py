import csv
from datetime import datetime, timedelta
from dataclasses import dataclass
from collections import defaultdict
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
    snapshots: Snapshots

    @staticmethod
    def pickTitle(snapshots: Snapshots) -> str:
        # choose window most active
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


WorkSessionsDict = dict[tuple[datetime, datetime], WorkSession]


def strToDatetime(name):
    dt = datetime.strptime(name, "%Y-%m-%d_%H_%M")
    return dt


def prep(filepath, config=None) -> WorkSessionsDict:
    groupedByTime = readData(filepath, config)
    sessions = groupIntoSessions(groupedByTime, config)
    return sessions


def makeSessionsSummary(workSessions: WorkSessionsDict):
    lightSessions = []
    for (start, end), w in workSessions.items():
        lightSessions.append(
            {
                "id": w.identifier,
                "start": w.start.timestamp(),
                "end": w.end.timestamp(),
                "duration_minutes": w.duration.total_seconds()/60,
                "title": w.preferred_title,
            }
        )
    lightSessions.sort(key=lambda x: x["start"], reverse=True)
    return lightSessions


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
    for timestamp in groupedByTime.keys():
        if (timestamp - last_timestamp) > timeout_delta:
            if (start_timestamp != datetime.min):
                workSess = WorkSession(
                    count,
                    start_timestamp,
                    last_timestamp,
                    last_timestamp - start_timestamp,
                    WorkSession.pickTitle(current_session),
                    current_session,
                )
                sessions[(start_timestamp, last_timestamp)] = workSess
            start_timestamp = timestamp
            last_timestamp = timestamp
            current_session: Snapshots = {}
            count += 1
        else:
            current_session[timestamp] = groupedByTime[timestamp]
            last_timestamp = timestamp

    sessions[(start_timestamp, last_timestamp)] = WorkSession(
        count,
        start_timestamp,
        last_timestamp,
        last_timestamp - start_timestamp,
        WorkSession.pickTitle(current_session),
        current_session,
    )
    print(
        f"Took {(time.monotonic_ns() - start)/1e9} seconds to group all data ({len(sessions)} sessions)"
    )

    return sessions
