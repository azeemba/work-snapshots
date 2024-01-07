"""
Sets up and launches snapshotting and browsing server
"""
import pathlib

from snapshotter import Snapshotter


def main():
    good_programs = [
        "Audacity.exe",
        "blender.exe",
        "Code.exe",
        "devenv.exe",
        "GitHubDesktop.exe",
        "inkscape.exe",
        "mintty.exe",
        "Resolve.exe",
        "unity.exe",
        "WindowsTerminal.exe",
    ]
    bad_programs = ["explorer.exe", "Twinkle Tray.exe"]
    frequency_minutes = 5
    storage_directory = pathlib.Path(".")
    snapshotter = Snapshotter(
        processes_designated_as_work=set(good_programs),
        storage_directory=storage_directory,
        processes_to_ignore=set(bad_programs),
        frequency_minutes=frequency_minutes)
    
    # TODO: Add pystray controls + write to CSV
    # Then update the storage path above
    snapshotter.run()


if __name__ == "__main__":
    main()