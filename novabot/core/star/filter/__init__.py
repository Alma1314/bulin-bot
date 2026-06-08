import abc

from novabot.core.config import NovaBotConfig
from novabot.core.platform.nova_message_event import NovaMessageEvent
from novabot.core.platform.message_type import MessageType


class HandlerFilter(abc.ABC):
    @abc.abstractmethod
    def filter(self, event: NovaMessageEvent, cfg: NovaBotConfig) -> bool:
        """是否应当被过滤"""
        raise NotImplementedError


__all__ = ["NovaBotConfig", "NovaMessageEvent", "HandlerFilter", "MessageType"]
