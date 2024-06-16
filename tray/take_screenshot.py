import argparse
from datetime import datetime
import pathlib

from PIL import ImageGrab


def parse_args():
    parser = argparse.ArgumentParser(description="Take a screenshot and store it")
    parser.add_argument("directory", help="Where to store it", type=pathlib.Path)
    parser.add_argument(
        "-t",
        "--timestamp",
        help="Identifier for the current time",
        type=str,
        default=_get_formatted_time(),
    )
    return parser.parse_args()


def _get_formatted_time():
    return datetime.now().strftime("%Y-%m-%d_%H_%M")


def take_snapshot(storage_directory: pathlib.Path, timestamp: str):
    im = ImageGrab.grab(all_screens=True, include_layered_windows=True)

    target = storage_directory / (timestamp + ".webp")
    im.save(target)
    return target


if __name__ == "__main__":
    args = parse_args()
    take_snapshot(args.directory, args.timestamp)
    print(args.timestamp)
