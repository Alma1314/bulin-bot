import argparse
import asyncio
import mimetypes
import os
import sys
from pathlib import Path

import runtime_bootstrap

runtime_bootstrap.initialize_runtime_bootstrap()

from novabot.core import LogBroker, LogManager, db_helper, logger  # noqa: E402
from novabot.core.initial_loader import InitialLoader  # noqa: E402
from novabot.core.utils.novabot_path import (  # noqa: E402
    get_novabot_config_path,
    get_novabot_knowledge_base_path,
    get_novabot_plugin_path,
    get_novabot_root,
    get_novabot_site_packages_path,
    get_novabot_temp_path,
)
from novabot.core.utils.runtime_env import is_packaged_desktop_runtime  # noqa: E402

# 将父目录添加到 sys.path
sys.path.append(Path(__file__).parent.as_posix())

logo_tmpl = r"""
布林bot（猫猫特供版）
"""


def check_env() -> None:
    if not (sys.version_info.major == 3 and sys.version_info.minor >= 13):
        logger.error("请使用 Python3.13+ 运行本项目。")
        exit()

    novabot_root = get_novabot_root()
    if novabot_root not in sys.path:
        sys.path.insert(0, novabot_root)

    site_packages_path = get_novabot_site_packages_path()
    if not is_packaged_desktop_runtime() and site_packages_path not in sys.path:
        sys.path.append(site_packages_path)

    os.makedirs(get_novabot_config_path(), exist_ok=True)
    os.makedirs(get_novabot_plugin_path(), exist_ok=True)
    os.makedirs(get_novabot_temp_path(), exist_ok=True)
    os.makedirs(get_novabot_knowledge_base_path(), exist_ok=True)
    os.makedirs(site_packages_path, exist_ok=True)

    # 针对问题 #181 的临时解决方案
    mimetypes.add_type("text/javascript", ".js")
    mimetypes.add_type("text/javascript", ".mjs")
    mimetypes.add_type("application/json", ".json")


async def main_async() -> None:
    """主异步入口"""

    db = db_helper

    # 打印 logo
    logger.info(logo_tmpl)

    core_lifecycle = InitialLoader(db, log_broker)
    await core_lifecycle.start()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="NovaBot")
    args = parser.parse_args()

    check_env()

    # 启动日志代理
    log_broker = LogBroker()
    LogManager.set_queue_handler(logger, log_broker)

    # 只使用一次 asyncio.run()
    asyncio.run(main_async())
