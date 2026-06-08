from novabot.api import star
from novabot.api.event import NovaMessageEvent, MessageChain


class AdminCommands:
    def __init__(self, context: star.Context) -> None:
        self.context = context

    async def update_dashboard(self, event: NovaMessageEvent) -> None:
        """更新管理面板（此功能已移除）"""
        await event.send(
            MessageChain().message("此功能已移除，请手动更新管理面板。")
        )
