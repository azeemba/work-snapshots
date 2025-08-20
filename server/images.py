import time
import threading
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
        
        # Thread safety locks
        self.cached_images_lock = threading.RLock()  # Protects cached_images set
        self.image_locks = {}  # Per-image locks for thumbnail generation
        self.image_locks_lock = threading.Lock()  # Protects image_locks dict

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

    def _get_image_lock(self, imageName):
        """Get or create a lock for a specific image name"""
        with self.image_locks_lock:
            if imageName not in self.image_locks:
                self.image_locks[imageName] = threading.Lock()
            return self.image_locks[imageName]

    def _prepare_single_thumbnail(self, size, imageName):
        # Quick check without lock first (optimization)
        with self.cached_images_lock:
            if imageName in self.cached_images:
                return

        # Get per-image lock to prevent multiple threads processing same image
        image_lock = self._get_image_lock(imageName)
        
        with image_lock:
            # Double-check inside lock (another thread might have created it)
            with self.cached_images_lock:
                if imageName in self.cached_images:
                    return

            original_path = Path(self.image_path, imageName)
            if not original_path.exists():
                return

            target_path = Path(self.cache_path, imageName)

            # Only create thumbnail if target doesn't exist (filesystem safety)
            if not target_path.exists():
                try:
                    with Image.open(original_path) as original:
                        original.thumbnail((size, size))
                        original.save(target_path)
                except Exception as e:
                    print(f"Failed to create thumbnail for {imageName}: {e}")
                    return
            
            # Add to cached set only after successful creation
            with self.cached_images_lock:
                self.cached_images.add(imageName)
