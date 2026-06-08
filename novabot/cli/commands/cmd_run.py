import asyncio
import os
import sys
import traceback
from pathlib import Path

import click
from filelock import FileLock, Timeout

from ..utils import check_novabot_root, get_novabot_root


async def run_novabot(novabot_root: Path) -> None:
    """Run NovaBot"""
    from novabot.core import LogBroker, LogManager, db_helper, logger
    from novabot.core.initial_loader import InitialLoader

    log_broker = LogBroker()
    LogManager.set_queue_handler(logger, log_broker)
    db = db_helper

    core_lifecycle = InitialLoader(db, log_broker)

    await core_lifecycle.start()


@click.option("--reload", "-r", is_flag=True, help="Auto-reload plugins")
@click.command()
def run(reload: bool) -> None:
    """Run NovaBot"""
    try:
        os.environ["NOVABOT_CLI"] = "1"
        novabot_root = get_novabot_root()

        if not check_novabot_root(novabot_root):
            raise click.ClickException(
                f"{novabot_root} is not a valid NovaBot root directory. Use 'novabot init' to initialize",
            )

        os.environ["NOVABOT_ROOT"] = str(novabot_root)
        sys.path.insert(0, str(novabot_root))

        if reload:
            click.echo("Plugin auto-reload enabled")
            os.environ["NOVABOT_RELOAD"] = "1"

        lock_file = novabot_root / "novabot.lock"
        lock = FileLock(lock_file, timeout=5)
        with lock.acquire():
            asyncio.run(run_novabot(novabot_root))
    except KeyboardInterrupt:
        click.echo("NovaBot has been shut down.")
    except Timeout:
        raise click.ClickException(
            "Cannot acquire lock file. Please check if another instance is running"
        )
    except Exception as e:
        raise click.ClickException(f"Runtime error: {e}\n{traceback.format_exc()}")
