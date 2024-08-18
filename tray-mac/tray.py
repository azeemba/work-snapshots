
import rumps

FREQUENCY_SECONDS = 120

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
    
    @rumps.clicked("Sync Now")
    def syncToPrimaryServer(self, menuItem: rumps.MenuItem):
        print("Not implemented syncing yet")
    
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

        # Check if interesting or "force track"

        # Snapshot + store

if __name__ == "__main__":
    WorkSnapshot("Work Snapshot", icon="book_open.png").run()