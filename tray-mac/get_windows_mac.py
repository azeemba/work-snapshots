"""Fetches window information and writes a JSON file

Does not write to sqlite database. 
Something else has to synchronize the JSON fiels with the main database.

Note that this application needs Screenrecording priviliges to be able
to fetch process names
"""
import Quartz
import AppKit

import pathlib
import json

from datatypes import Process
from dataclasses import asdict

def _get_frontmost():
    workspace = AppKit.NSWorkspace.sharedWorkspace()    
    app = workspace.frontmostApplication()
    return (app.localizedName(), app.processIdentifier())

def get_windows_across_workspaces(filter_list: list[str] = None):
    if filter_list is None:
        filter_list = []

    processes: list[Process] = []
    front = _get_frontmost()
    
    # Get all windows
    window_list = Quartz.CGWindowListCopyWindowInfo(Quartz.kCGWindowListExcludeDesktopElements, Quartz.kCGNullWindowID)
    for window in window_list:
        pid = window.get('kCGWindowOwnerPID')
        proc_name = window.get('kCGWindowOwnerName', '')
        # Needs screen recording priviliges
        title = window.get('kCGWindowName')
        size = window.get('kCGWindowBounds')
        alpha = window.get('kCGWindowAlpha')
        layer = window.get('kCGWindowLayer')
        if proc_name in filter_list or not title or size["Height"] < 200 or size["Width"] < 200 or alpha < 0.5 or layer != 0:
            continue
        # print(f"{pid}, {proc_name}, {title}, {layer}")

        processes.append(Process(proc_name, title, pid == front[1]))

    print(processes)
    return processes

def check_if_interesting(processes: list[Process], interesting: list[str]):
    lower_interesting = [i.lower() for i in interesting]
    return any(p.name.lower() in lower_interesting for p in processes)

def write_windows(destination_dir: pathlib.Path, timestamp: str, processes: list[Process], frequency_seoncds: int):
    with open(destination_dir / (timestamp + ".json"), "w") as f:
        json.dump({
            "processes": [asdict(p) for p in processes],
            "frequencySeconds": frequency_seoncds
        }, f)

if __name__ == "__main__":
    windows = get_windows_across_workspaces()
