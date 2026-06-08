import asyncio
from pathlib import Path

import click
from filelock import FileLock, Timeout

from ..utils import get_novabot_root


async def initialize_novabot(novabot_root: Path) -> None:
    """Execute NovaBot initialization logic"""
    dot_novabot = novabot_root / ".novabot"

    if not dot_novabot.exists():
        if click.confirm(
            f"Install NovaBot to this directory? {novabot_root}",
            default=True,
            abort=True,
        ):
            dot_novabot.touch()
            click.echo(f"Created {dot_novabot}")

    paths = {
        "data": novabot_root / "data",
        "config": novabot_root / "data" / "config",
        "plugins": novabot_root / "data" / "plugins",
        "temp": novabot_root / "data" / "temp",
    }

    for name, path in paths.items():
        path.mkdir(parents=True, exist_ok=True)
        click.echo(f"{'Created' if not path.exists() else 'Directory exists'}: {path}")


@click.command()
def init() -> None:
    """Initialize NovaBot"""
    click.echo("Initializing NovaBot...")
    novabot_root = get_novabot_root()
    lock_file = novabot_root / "novabot.lock"
    lock = FileLock(lock_file, timeout=5)

    try:
        with lock.acquire():
            asyncio.run(initialize_novabot(novabot_root))
            click.echo("Done! You can now run 'novabot run' to start NovaBot")
    except Timeout:
        raise click.ClickException(
            "Cannot acquire lock file. Please check if another instance is running"
        )

    except Exception as e:
        raise click.ClickException(f"Initialization failed: {e!s}")
