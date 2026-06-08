import os
import sys


def is_frozen_runtime() -> bool:
    return bool(getattr(sys, "frozen", False))


def is_packaged_desktop_runtime() -> bool:
    return os.environ.get("NOVABOT_DESKTOP_CLIENT") == "1"
