import time
from PIL import Image
from pathlib import Path

from multiprocessing import Pool
from functools import partial

from datahandling import WorkSessionsDict, WorkSession


class ImageHandler:
    def __init__(self, config):
        self.image_path = config["main"]["images"]
        self.cache_path = config["main"]["cache"]
        cache_dir = Path(self.cache_path)
        cache_dir.mkdir(exist_ok=True)

        self.thumbnail_size = config.getint("ui", "thumbnail_size")
        self.cached_images = set(str(s.name) for s in cache_dir.glob("*.webp"))

    def prepare_thumbnails(self, workSessions: WorkSessionsDict):
        start = time.monotonic_ns()

        # with Pool(6) as p:
        # p.map(partial(prepare_single_thumbnail, size, image_path, cache_path), workSessions.values())
        for session in workSessions.values():
            preferred = session.preferred_image + ".webp"
            self._prepare_single_thumbnail(self.thumbnail_size, preferred)

        print(
            f"Took {(time.monotonic_ns() - start)/1e9} seconds to generate all thumbnails"
        )

    def makeSureThumbnailExists(self, image):
        self._prepare_single_thumbnail(self.thumbnail_size, image)

    def _prepare_single_thumbnail(self, size, imageName):
        if imageName in self.cached_images:
            return

        original_path = Path(self.image_path, imageName)
        if not original_path.exists():
            return

        target_path = Path(self.cache_path, imageName)

        with Image.open(original_path) as original:
            original.thumbnail((size, size))
            original.save(target_path)
        self.cached_images.add(imageName)
