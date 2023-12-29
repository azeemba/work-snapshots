"""Massage raw data to be frontend-friendly and enrich with custom data"""

from datetime import timedelta, datetime
from multiprocessing.spawn import old_main_modules
from datahandling import Snapshots, WorkSessionsDict, WorkSession, datetime2key
from db_handler import SessionOverride

def addWorkSessionSplits(workSession: WorkSessionsDict, manualSplits: list[tuple[int, datetime]]):
    for originalKey, customStart in manualSplits:
        if originalKey not in workSession:
            print(f"{originalKey=} not in Work Sessions. Skipping splitting.")
        
        currentSession = workSession[originalKey]
        snapshots = currentSession.snapshots

        older_snapshots: Snapshots = {}
        newer_snapshots: Snapshots = {}

        for fullDatetime, snapshot in snapshots.items():
            if (fullDatetime < customStart):
                older_snapshots[fullDatetime] = snapshot
            else:
                newer_snapshots[fullDatetime] = snapshot
        
        updated_title = WorkSession.pickTitle(older_snapshots)       
        workSession[originalKey] = WorkSession(
            originalKey,
            currentSession.start,
            max(older_snapshots.keys()),
            timedelta(minutes=len(older_snapshots)*5),
            updated_title,
            WorkSession.pickImageTimestamp(older_snapshots, updated_title),
            older_snapshots
        )

        newer_title = WorkSession.pickTitle(newer_snapshots)
        allTimes = newer_snapshots.keys()
        startDatetime = min(allTimes)
        endDatetime = max(allTimes)
        key = datetime2key(startDatetime)
        workSession[key] = WorkSession(
            key,
            startDatetime,
            endDatetime,
            timedelta(minutes=len(newer_snapshots)*5),
            newer_title,
            WorkSession.pickImageTimestamp(newer_snapshots, newer_title),
            newer_snapshots)




def makeSummaryForFrontend(workSessions: WorkSessionsDict, overrides: dict[int, SessionOverride]):
    lightSessions = []

    for identifier, w in workSessions.items():
        duration_minutes = w.duration.total_seconds() / 60
        if duration_minutes < 20:
            continue

        title = w.preferred_title
        tag = ""
        if identifier in overrides:
            title = overrides[identifier].custom_title
            tag = overrides[identifier].tag

        lightSessions.append(
            {
                "id": w.identifier,
                "start": w.start.timestamp(),
                "end": w.end.timestamp(),
                "display_time": f"{w.start.strftime('%b %d, %Y %I:%M %p')} - {w.end.strftime('%I:%M %p')}",
                "duration_minutes": duration_minutes,
                "title": title,
                "tag": tag,
                "image": f"/cache/{w.preferred_image}.webp",
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
