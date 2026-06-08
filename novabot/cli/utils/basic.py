from pathlib import Path


def check_novabot_root(path: str | Path) -> bool:
    """Check if the path is an NovaBot root directory"""
    if not isinstance(path, Path):
        path = Path(path)
    if not path.exists() or not path.is_dir():
        return False
    if not (path / ".novabot").exists():
        return False
    return True


def get_novabot_root() -> Path:
    """Get the NovaBot root directory path"""
    return Path.cwd()
