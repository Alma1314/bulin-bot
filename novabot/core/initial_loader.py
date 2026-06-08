"""NovaBot 启动器，负责初始化和启动核心组件。

工作流程:
1. 初始化核心生命周期, 传递数据库和日志代理实例到核心生命周期
2. 运行核心生命周期任务
"""

import asyncio
import traceback

from novabot.core import LogBroker, logger
from novabot.core.core_lifecycle import NovaBotCoreLifecycle
from novabot.core.db import BaseDatabase


class InitialLoader:
    """NovaBot 启动器，负责初始化和启动核心组件。"""

    def __init__(self, db: BaseDatabase, log_broker: LogBroker) -> None:
        self.db = db
        self.logger = logger
        self.log_broker = log_broker

    async def start(self) -> None:
        core_lifecycle = NovaBotCoreLifecycle(self.log_broker, self.db)

        try:
            await core_lifecycle.initialize()
        except Exception as e:
            logger.critical(traceback.format_exc())
            logger.critical(f"😭 初始化 NovaBot 失败：{e} !!!")
            return

        try:
            await core_lifecycle.start()
        except asyncio.CancelledError:
            logger.info("🌈 正在关闭 NovaBot...")
            await core_lifecycle.stop()
