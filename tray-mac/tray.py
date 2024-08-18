
from datetime import datetime
import pathlib
import subprocess

import rumps
import get_windows_mac
import take_screenshot

FREQUENCY_SECONDS = 120
INTERESTING_NAMES = [
    "Audacity",
    "blender",
    "Code",
    "GitHubDesktop",
    "inkscape",
    "Resolve",
    "unity",
    "iTerm2"
]
DIRECTORY = pathlib.Path("/Users/Z/Sync/snapshots-secondary")

def _get_formatted_time():
    return datetime.now().strftime("%Y-%m-%d_%H_%M")

class WorkSnapshot(rumps.App):
    _force_ignore: bool = False
    _force_track: bool = False
    @rumps.clicked("Force Ignore")
    def toggleForceIgnore(self, menuItem: rumps.MenuItem):
        self._force_ignore = not self._force_ignore
        menuItem.state = self._force_ignore
        if self._force_ignore:
            self.icon = "book_x.png"
        else:
            self.icon = "book_open.png"

    @rumps.clicked("Force Track")
    def toggleForceTrack(self, menuItem: rumps.MenuItem):
        self._force_track = not self._force_track
        menuItem.state = self._force_track
        if self._force_track and not self._force_ignore:
            self.icon = "book_open.png"
        else:
            self.icon = "book_x.png"
    

    @rumps.timer(FREQUENCY_SECONDS)
    def checkAndCapture(self, sender):
        print("Check and capture")
        if self._force_ignore:
            print("Sending notification")
            rumps.notification(
                "Work Snapshotter",
                "Currently, is in ignore mode.",
                "Make sure you aren't doing work lol.",
                sound=False)
        
        # Now fetch windows
        processes = get_windows_mac.get_windows_across_workspaces([])

        # Check if interesting or "force track"
        if not get_windows_mac.check_if_interesting(processes, INTERESTING_NAMES):
            return

        # Snapshot + sound
        timestamp = _get_formatted_time()
        take_screenshot.take_snapshot(DIRECTORY, timestamp)
        subprocess.run(["afplay", "nice-camera-click-106269.mp3"])

        # store
        get_windows_mac.write_windows(DIRECTORY, timestamp, processes, FREQUENCY_SECONDS)

if __name__ == "__main__":
    WorkSnapshot("Work Snapshot", icon="book_open.png").run()