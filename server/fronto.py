"""Massage raw data to be frontend-friendly and enrich with custom data"""

from datahandling import WorkSessionsDict, WorkSession
from db_handler import Db

def makeSummaryForFrontend(workSessions: WorkSessionsDict, db: Db):
    lightSessions = []
    overrides = db.get_all_overrides()

    for identifier, w in workSessions.items():
        duration_minutes = w.duration.total_seconds() / 60
        if duration_minutes < 20:
            continue

        title = w.preferred_title
        if identifier in overrides and overrides[identifier].custom_title:
            title = overrides[identifier].custom_title

        lightSessions.append(
            {
                "id": w.identifier,
                "start": w.start.timestamp(),
                "end": w.end.timestamp(),
                "display_time": f"{w.start.strftime('%b %d, %Y %I:%M %p')} - {w.end.strftime('%I:%M %p')}",
                "duration_minutes": duration_minutes,
                "title": title,
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

