from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from novabot.core.config import NovaBotConfig

from .context_utils import call_event_hook, call_handler

if TYPE_CHECKING:
    from novabot.core.star import PluginManager


@dataclass
class PipelineContext:
    """上下文对象，包含管道执行所需的上下文信息"""

    novabot_config: NovaBotConfig  # NovaBot 配置对象
    plugin_manager: PluginManager  # 插件管理器对象
    novabot_config_id: str
    call_handler = call_handler
    call_event_hook = call_event_hook
