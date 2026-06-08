import re

from novabot.core.config import NovaBotConfig
from novabot.core.platform.nova_message_event import NovaMessageEvent

from . import HandlerFilter


# 正则表达式过滤器不会受到 wake_prefix 的制约。
class RegexFilter(HandlerFilter):
    """正则表达式过滤器"""

    def __init__(self, regex: str | re.Pattern) -> None:
        self.regex = re.compile(regex)
        self.regex_str = self.regex.pattern

    def filter(self, event: NovaMessageEvent, cfg: NovaBotConfig) -> bool:
        return bool(self.regex.search(event.get_message_str().strip()))
