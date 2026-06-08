from pydantic import Field
from pydantic.dataclasses import dataclass

from novabot.core.agent.run_context import ContextWrapper
from novabot.core.platform.nova_message_event import NovaMessageEvent
from novabot.core.star.context import Context


@dataclass
class NovaAgentContext:
    __pydantic_config__ = {"arbitrary_types_allowed": True}

    context: Context
    """The star context instance"""
    event: NovaMessageEvent
    """The message event associated with the agent context."""
    extra: dict[str, str] = Field(default_factory=dict)
    """Customized extra data."""


AgentContextWrapper = ContextWrapper[NovaAgentContext]
