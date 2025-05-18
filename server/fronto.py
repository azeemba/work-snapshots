"""Massage raw data to be frontend-friendly and enrich with custom data"""

from datetime import timedelta, datetime
from typing import TypedDict
from multiprocessing.spawn import old_main_modules

from datahandling import (
    Snapshots,
    WorkSessionsDict,
    WorkSession,
    datetime2key,
    calculateWorkSessionDuration,
)
from db_handler import SessionOverride, TagMapping

LightSession = TypedDict(
    "LightSession",
    {
        "id": float,
        "start": float,
        "end": float,
        "display_time": str,
        "duration_minutes": float,
        "title": str,
        "tag": str,
        "image": str,
    },
)


def addWorkSessionSplits(
    workSession: WorkSessionsDict, manualSplits: list[tuple[int, datetime]]
):
    for originalKey, customStart in manualSplits:
        if originalKey not in workSession:
            print(f"{originalKey=} not in Work Sessions. Skipping splitting.")

        currentSession = workSession[originalKey]
        snapshots = currentSession.snapshots

        older_snapshots: Snapshots = {}
        newer_snapshots: Snapshots = {}

        for fullDatetime, snapshot in snapshots.items():
            if fullDatetime < customStart:
                older_snapshots[fullDatetime] = snapshot
            else:
                newer_snapshots[fullDatetime] = snapshot

        updated_title = WorkSession.pickTitle(older_snapshots)
        workSession[originalKey] = WorkSession(
            originalKey,
            currentSession.start,
            max(older_snapshots.keys()),
            calculateWorkSessionDuration(older_snapshots),
            updated_title,
            WorkSession.pickImageTimestamp(older_snapshots, updated_title),
            older_snapshots,
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
            calculateWorkSessionDuration(newer_snapshots),
            newer_title,
            WorkSession.pickImageTimestamp(newer_snapshots, newer_title),
            newer_snapshots,
        )


def makeSummaryForFrontend(
    workSessions: WorkSessionsDict, overrides: dict[int, SessionOverride], tag_mappings: dict[str, TagMapping]
):
    lightSessions: list[LightSession] = []

    for identifier, w in workSessions.items():
        duration_minutes = w.duration.total_seconds() / 60
        if duration_minutes < 20:
            continue

        title: str = w.preferred_title
        tag: str = ""
        if identifier in overrides:
            custom_title = overrides[identifier].custom_title
            custom_tag = overrides[identifier].tag
            if custom_title is not None:
                title = custom_title

            if custom_tag is not None:
                tag = custom_tag

        lightSession: LightSession = {
            "id": w.identifier,
            "start": w.start.timestamp(),
            "end": w.end.timestamp(),
            "display_time": f"{w.start.strftime('%b %d, %Y %I:%M %p')} - {w.end.strftime('%I:%M %p')}",
            "duration_minutes": duration_minutes,
            "title": title,
            "tag": tag,
            "image": f"/cache/{w.preferred_image}.webp",
        }

        lightSessions.append(lightSession)
    lightSessions.sort(key=lambda x: x["start"], reverse=True)
    return lightSessions


def makeDetailForFrontend(workSession: WorkSession, lightSession):
    detailed_snapshots = {}
    for timestamp, snapshot in workSession.snapshots.items():
        if not snapshot:
            continue
        current = []
        timestamp = snapshot.timestamp
        timestamp_original = snapshot.timestamp_original
        for p in snapshot.processes:
            current.append(
                {"process": p.process, "title": p.title, "active": p.isActive}
            )

        detailed_snapshots[timestamp.timestamp()] = {
            "display_time": timestamp.strftime("%b %d, %Y %I:%M %p"),
            "image": f"/image/{timestamp_original}.webp",
            "processes": current,
        }
    return {"details": detailed_snapshots, "session": lightSession}

def convertTagsToResponse(tags: dict[str, TagMapping]) -> dict[str, list[dict[str, str]]]:
    tags_serialized= [t.__dict__ for t in tags.values()]
    return {"tags" : tags_serialized}