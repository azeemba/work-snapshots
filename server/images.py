import time
from PIL import Image
from pathlib import Path

from multiprocessing import Pool
from functools import partial

from datahandling import WorkSessionsDict, WorkSession


def prepare_thumbnails(workSessions: WorkSessionsDict, config):
    start = time.monotonic_ns()
    size = config.getint("ui", "thumbnail_size")
    image_path = config["main"]["images"]
    cache_path = config["main"]["cache"]

    # with Pool(6) as p:
    # p.map(partial(prepare_single_thumbnail, size, image_path, cache_path), workSessions.values())
    for session in workSessions.values():
        prepare_single_thumbnail(size, image_path, cache_path, session)

    print(
        f"Took {(time.monotonic_ns() - start)/1e9} seconds to generate all thumbnails"
    )


def prepare_single_thumbnail(size, image_path, cache_path, session: WorkSession):
    preferred = session.preferred_image + ".webp"
    original_path = Path(image_path, preferred)
    if not original_path.exists():
        print(f"Bailing on {original_path}. Doesn't exit")
        return

    target_path = Path(cache_path, preferred)
    if target_path.exists():
        print(f"Skipping generating thumbnail for {session.identifier}")
        return

    with Image.open(original_path) as original:
        original.thumbnail((size, size))
        original.save(target_path)
