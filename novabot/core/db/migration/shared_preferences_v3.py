import json
import os
from typing import TypeVar

from filelock import FileLock

from novabot.core.utils.novabot_path import get_novabot_data_path

_VT = TypeVar("_VT")


class SharedPreferences:
    def __init__(self, path=None) -> None:
        if path is None:
            path = os.path.join(get_novabot_data_path(), "shared_preferences.json")
        self.path = path
        self._lock = FileLock(path + ".lock")
        self._data = self._load_preferences()

    def _load_preferences(self):
        if os.path.exists(self.path):
            try:
                with self._lock.acquire(timeout=5):
                    with open(self.path) as f:
                        return json.load(f)
            except json.JSONDecodeError:
                with self._lock.acquire(timeout=5):
                    os.remove(self.path)
        return {}

    def _save_preferences(self) -> None:
        with self._lock.acquire(timeout=5):
            with open(self.path, "w") as f:
                json.dump(self._data, f, indent=4, ensure_ascii=False)
                f.flush()


sp = SharedPreferences()
