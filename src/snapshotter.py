import pathlib
import threading
import time
import os
from datetime import datetime

from PIL import ImageGrab
import pywinctl

from datatypes import Process


class Snapshotter(threading.Thread):
    def __init__(
        self,
        processes_designated_as_work: set[str],
        storage_directory: pathlib.Path,
        processes_to_ignore: set[str] | None = None,
        frequency_minutes=5,
    ):
        """
        Sets up a snapshotter that runs on its on thread with `run`

            processes_designated_as_work: set[str]: When a process from the set is running
            with and active window, a snapshot of the screen is taken

            storage_directory: pathlib.Path: Where to place the screenshots

            processes_to_ignore: set[str] | None = None: There are some noisy processes
            like explorer.exe. Those are filtered out from the metadata of the screenshot
        """
        threading.Thread.__init__(self)

        self.processes_designated_as_work = processes_designated_as_work
        self.processes_to_ignore = (
            processes_to_ignore if processes_to_ignore else set("explorer.exe")
        )

        self.storage_directory = storage_directory
        self.frequency_minutes = frequency_minutes

        self._last_snapshot_t = 0.0  # will be overridden later

        self.daemon = True  # should die with parent process
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def _get_current_windows(self):
        t5 = time.monotonic_ns()
        windows = pywinctl.getAllWindows()
        titleProcessMap = pywinctl.getAllAppsWindowsTitles()
        invert_dict = {}
        for process, val in titleProcessMap.items():
            if process in self.processes_to_ignore:
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

    def _trigger_workflow(self):
        processes = self._get_current_windows()
        if self._should_take_snapshot(processes):
            self._take_snapshot()
            self._write_processes(processes, self._get_formatted_time())
            self._last_snapshot_t = time.monotonic()

    def _should_take_snapshot(self, current_processes: list[Process]) -> bool:
        for process in current_processes:
            if process.name in self.processes_designated_as_work:
                return True

        return False

    def _get_formatted_time(self):
        return datetime.now().strftime("%Y-%m-%d_%H_%M")

    def _take_snapshot(self):
        im = ImageGrab.grab(all_screens=True, include_layered_windows=True)
        im.save(self.storage_directory / (self._get_formatted_time() + ".webp"))

    def _write_processes(self, processes: list[Process], timestamp: str):
        filepath = self.storage_directory / "open-windows.csv"
        csv_rows = []
        for p in processes:
            name = p.name.replace(",", "")
            title = p.title.replace(",", "")
            isActive = "1" if p.isActive else "0"
            # writing naively for now. Will change to db later anyways.
            csv_rows.append(f"{timestamp}, {name}, {title}, {isActive}\n")

        with open(filepath, "a") as fh:
            fh.writelines(csv_rows)

    def run(self):
        self._last_snapshot_t = time.monotonic()
        self._trigger_workflow()

        while not self._stop_event.is_set():
            time.sleep(1)
            passed_time = time.monotonic() - self._last_snapshot_t

            if passed_time > self.frequency_minutes * 60:
                self._trigger_workflow()
