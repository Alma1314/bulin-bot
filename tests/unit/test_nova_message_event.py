"""Tests for NovaMessageEvent class."""

import re
from unittest.mock import AsyncMock, patch

import pytest

from novabot.core.message.components import (
    At,
    AtAll,
    Face,
    Forward,
    Image,
    Plain,
    Reply,
)
from novabot.core.message.message_event_result import MessageEventResult
from novabot.core.platform.nova_message_event import NovaMessageEvent
from novabot.core.platform.novabot_message import NovaBotMessage, MessageMember
from novabot.core.platform.message_type import MessageType
from novabot.core.platform.platform_metadata import PlatformMetadata


class ConcreteBulinMessageEvent(NovaMessageEvent):
    """Concrete implementation of NovaMessageEvent for testing purposes."""

    async def send(self, message):
        """Send message implementation."""
        await super().send(message)


@pytest.fixture
def platform_meta():
    """Create platform metadata for testing."""
    return PlatformMetadata(
        name="test_platform",
        description="Test platform",
        id="test_platform_id",
    )


@pytest.fixture
def message_member():
    """Create a message member for testing."""
    return MessageMember(user_id="user123", nickname="TestUser")


@pytest.fixture
def novabot_message(message_member):
    """Create an NovaBotMessage for testing."""
    message = NovaBotMessage()
    message.type = MessageType.FRIEND_MESSAGE
    message.self_id = "bot123"
    message.session_id = "session123"
    message.message_id = "msg123"
    message.sender = message_member
    message.message = [Plain(text="Hello world")]
    message.message_str = "Hello world"
    message.raw_message = None
    return message


@pytest.fixture
def nova_message_event(platform_meta, novabot_message):
    """Create an NovaMessageEvent instance for testing."""
    return ConcreteBulinMessageEvent(
        message_str="Hello world",
        message_obj=novabot_message,
        platform_meta=platform_meta,
        session_id="session123",
    )


class TestBulinMessageEventInit:
    """Tests for NovaMessageEvent initialization."""

    def test_init_basic(self, nova_message_event):
        """Test basic NovaMessageEvent initialization."""
        assert nova_message_event.message_str == "Hello world"
        assert nova_message_event.role == "member"
        assert nova_message_event.is_wake is False
        assert nova_message_event.is_at_or_wake_command is False
        assert nova_message_event._extras == {}
        assert nova_message_event._result is None
        assert nova_message_event.call_llm is False

    def test_init_session(self, nova_message_event):
        """Test session initialization."""
        assert nova_message_event.session_id == "session123"
        assert nova_message_event.session.platform_name == "test_platform_id"

    def test_init_platform_reference(self, nova_message_event, platform_meta):
        """Test platform reference initialization."""
        assert nova_message_event.platform_meta == platform_meta
        assert nova_message_event.platform == platform_meta  # back compatibility

    def test_init_created_at(self, nova_message_event):
        """Test created_at timestamp is set."""
        assert nova_message_event.created_at is not None
        assert isinstance(nova_message_event.created_at, float)

    def test_init_trace(self, nova_message_event):
        """Test trace/span initialization."""
        assert nova_message_event.trace is not None
        assert nova_message_event.span is not None
        assert nova_message_event.trace == nova_message_event.span


class TestUnifiedMsgOrigin:
    """Tests for unified_msg_origin property."""

    def test_unified_msg_origin_getter(self, nova_message_event):
        """Test unified_msg_origin getter."""
        expected = "test_platform_id:FriendMessage:session123"
        assert nova_message_event.unified_msg_origin == expected

    def test_unified_msg_origin_setter(self, nova_message_event):
        """Test unified_msg_origin setter."""
        nova_message_event.unified_msg_origin = "new_platform:GroupMessage:new_session"

        assert nova_message_event.session.platform_name == "new_platform"
        assert nova_message_event.session.session_id == "new_session"


class TestSessionId:
    """Tests for session_id property."""

    def test_session_id_getter(self, nova_message_event):
        """Test session_id getter."""
        assert nova_message_event.session_id == "session123"

    def test_session_id_setter(self, nova_message_event):
        """Test session_id setter."""
        nova_message_event.session_id = "new_session_id"

        assert nova_message_event.session_id == "new_session_id"


class TestGetPlatformInfo:
    """Tests for platform info methods."""

    def test_get_platform_name(self, nova_message_event):
        """Test get_platform_name method."""
        assert nova_message_event.get_platform_name() == "test_platform"

    def test_get_platform_id(self, nova_message_event):
        """Test get_platform_id method."""
        assert nova_message_event.get_platform_id() == "test_platform_id"


class TestGetMessageInfo:
    """Tests for message info methods."""

    def test_get_message_str(self, nova_message_event):
        """Test get_message_str method."""
        assert nova_message_event.get_message_str() == "Hello world"

    def test_get_message_str_none(self, platform_meta, novabot_message):
        """Test get_message_str keeps None when source message_str is None."""
        novabot_message.message_str = None
        event = ConcreteBulinMessageEvent(
            message_str=None,
            message_obj=novabot_message,
            platform_meta=platform_meta,
            session_id="session123",
        )
        assert event.get_message_str() is None

    def test_get_messages(self, nova_message_event):
        """Test get_messages method."""
        messages = nova_message_event.get_messages()
        assert len(messages) == 1
        assert isinstance(messages[0], Plain)
        assert messages[0].text == "Hello world"

    def test_get_message_type(self, nova_message_event):
        """Test get_message_type method."""
        assert nova_message_event.get_message_type() == MessageType.FRIEND_MESSAGE

    def test_get_session_id(self, nova_message_event):
        """Test get_session_id method."""
        assert nova_message_event.get_session_id() == "session123"

    def test_get_group_id_empty_for_private(self, nova_message_event):
        """Test get_group_id returns empty for private messages."""
        assert nova_message_event.get_group_id() == ""

    def test_get_self_id(self, nova_message_event):
        """Test get_self_id method."""
        assert nova_message_event.get_self_id() == "bot123"

    def test_get_sender_id(self, nova_message_event):
        """Test get_sender_id method."""
        assert nova_message_event.get_sender_id() == "user123"

    def test_get_sender_name(self, nova_message_event):
        """Test get_sender_name method."""
        assert nova_message_event.get_sender_name() == "TestUser"

    def test_get_sender_name_empty_when_none(self, platform_meta, novabot_message):
        """Test get_sender_name returns empty string when nickname is None."""
        novabot_message.sender = MessageMember(user_id="user123", nickname=None)
        event = ConcreteBulinMessageEvent(
            message_str="test",
            message_obj=novabot_message,
            platform_meta=platform_meta,
            session_id="session123",
        )
        assert event.get_sender_name() == ""

    def test_get_sender_name_coerces_non_string(self, platform_meta, novabot_message):
        """Test get_sender_name stringifies non-string nickname values."""
        novabot_message.sender = MessageMember(user_id="user123", nickname=None)
        novabot_message.sender.nickname = 12345
        event = ConcreteBulinMessageEvent(
            message_str="test",
            message_obj=novabot_message,
            platform_meta=platform_meta,
            session_id="session123",
        )
        assert event.get_sender_name() == "12345"


class TestGetMessageOutline:
    """Tests for get_message_outline method."""

    def test_outline_plain_text(self, nova_message_event):
        """Test outline with plain text message."""
        outline = nova_message_event.get_message_outline()
        assert "Hello world" in outline

    def test_outline_with_image(self, platform_meta, novabot_message):
        """Test outline with image component."""
        novabot_message.message = [
            Plain(text="Look at this"),
            Image(file="http://example.com/img.jpg"),
        ]
        event = ConcreteBulinMessageEvent(
            message_str="Look at this",
            message_obj=novabot_message,
            platform_meta=platform_meta,
            session_id="session123",
        )
        outline = event.get_message_outline()
        assert "Look at this" in outline
        assert "[图片]" in outline

    def test_outline_with_at(self, platform_meta, novabot_message):
        """Test outline with At component."""
        novabot_message.message = [At(qq="12345"), Plain(text=" hello")]
        event = ConcreteBulinMessageEvent(
            message_str=" hello",
            message_obj=novabot_message,
            platform_meta=platform_meta,
            session_id="session123",
        )
        outline = event.get_message_outline()
        assert "[At:12345]" in outline

    def test_outline_with_at_all(self, platform_meta, novabot_message):
        """Test outline with AtAll component."""
        novabot_message.message = [AtAll()]
        event = ConcreteBulinMessageEvent(
            message_str="",
            message_obj=novabot_message,
            platform_meta=platform_meta,
            session_id="session123",
        )
        outline = event.get_message_outline()
        # AtAll format is "[At:all]" in the actual implementation
        assert "[At:" in outline and "all" in outline.lower()

    def test_outline_with_face(self, platform_meta, novabot_message):
        """Test outline with Face component."""
        novabot_message.message = [Face(id="123")]
        event = ConcreteBulinMessageEvent(
            message_str="",
            message_obj=novabot_message,
            platform_meta=platform_meta,
            session_id="session123",
        )
        outline = event.get_message_outline()
        assert "[表情:123]" in outline

    def test_outline_with_forward(self, platform_meta, novabot_message):
        """Test outline with Forward component."""
        # Forward requires an id parameter
        novabot_message.message = [Forward(id="test_forward_id")]
        event = ConcreteBulinMessageEvent(
            message_str="",
            message_obj=novabot_message,
            platform_meta=platform_meta,
            session_id="session123",
        )
        outline = event.get_message_outline()
        assert "[转发消息]" in outline

    def test_outline_with_reply(self, platform_meta, novabot_message):
        """Test outline with Reply component."""
        # Reply requires an id parameter
        reply = Reply(id="test_reply_id")
        reply.message_str = "Original message"
        reply.sender_nickname = "Sender"
        novabot_message.message = [reply, Plain(text=" reply")]
        event = ConcreteBulinMessageEvent(
            message_str=" reply",
            message_obj=novabot_message,
            platform_meta=platform_meta,
            session_id="session123",
        )
        outline = event.get_message_outline()
        assert "[引用消息(Sender: Original message)]" in outline

    def test_outline_with_reply_no_message(self, platform_meta, novabot_message):
        """Test outline with Reply component without message_str."""
        # Reply requires an id parameter
        reply = Reply(id="test_reply_id")
        reply.message_str = None
        novabot_message.message = [reply]
        event = ConcreteBulinMessageEvent(
            message_str="",
            message_obj=novabot_message,
            platform_meta=platform_meta,
            session_id="session123",
        )
        outline = event.get_message_outline()
        assert "[引用消息]" in outline

    def test_outline_empty_chain(self, platform_meta, novabot_message):
        """Test outline with empty message chain."""
        novabot_message.message = []
        event = ConcreteBulinMessageEvent(
            message_str="",
            message_obj=novabot_message,
            platform_meta=platform_meta,
            session_id="session123",
        )
        outline = event.get_message_outline()
        assert outline == ""

    def test_outline_very_long_plain_text(self, platform_meta, novabot_message):
        """Test outline generation for very long plain text content."""
        long_text = "A" * 20000
        novabot_message.message = [Plain(text=long_text)]
        event = ConcreteBulinMessageEvent(
            message_str=long_text,
            message_obj=novabot_message,
            platform_meta=platform_meta,
            session_id="session123",
        )
        outline = event.get_message_outline()
        assert outline.startswith("A")
        assert len(outline) >= 20000


class TestExtras:
    """Tests for extra information methods."""

    def test_set_extra(self, nova_message_event):
        """Test set_extra method."""
        nova_message_event.set_extra("key1", "value1")
        assert nova_message_event._extras["key1"] == "value1"

    def test_get_extra_with_key(self, nova_message_event):
        """Test get_extra with specific key."""
        nova_message_event.set_extra("key1", "value1")
        assert nova_message_event.get_extra("key1") == "value1"

    def test_get_extra_with_default(self, nova_message_event):
        """Test get_extra with default value."""
        result = nova_message_event.get_extra("nonexistent", "default_value")
        assert result == "default_value"

    def test_get_extra_all(self, nova_message_event):
        """Test get_extra without key returns all extras."""
        nova_message_event.set_extra("key1", "value1")
        nova_message_event.set_extra("key2", "value2")
        all_extras = nova_message_event.get_extra()
        assert all_extras == {"key1": "value1", "key2": "value2"}

    def test_clear_extra(self, nova_message_event):
        """Test clear_extra method."""
        nova_message_event.set_extra("key1", "value1")
        nova_message_event.clear_extra()
        assert nova_message_event._extras == {}


class TestSetResult:
    """Tests for set_result method."""

    def test_set_result_with_message_event_result(self, nova_message_event):
        """Test set_result with MessageEventResult object."""
        result = MessageEventResult().message("Test message")
        nova_message_event.set_result(result)

        assert nova_message_event._result == result

    def test_set_result_with_string(self, nova_message_event):
        """Test set_result with string creates MessageEventResult."""
        nova_message_event.set_result("Test message")

        assert nova_message_event._result is not None
        assert len(nova_message_event._result.chain) == 1
        assert isinstance(nova_message_event._result.chain[0], Plain)

    def test_set_result_with_empty_chain(self, nova_message_event):
        """Test set_result handles empty chain correctly."""
        result = MessageEventResult()
        # chain is already an empty list by default
        nova_message_event.set_result(result)

        assert nova_message_event._result.chain == []


class TestStopContinueEvent:
    """Tests for stop_event and continue_event methods."""

    def test_stop_event_creates_result_if_none(self, nova_message_event):
        """Test stop_event creates result if none exists."""
        nova_message_event.stop_event()

        assert nova_message_event._result is not None
        assert nova_message_event.is_stopped() is True

    def test_stop_event_with_existing_result(self, nova_message_event):
        """Test stop_event with existing result."""
        nova_message_event.set_result(MessageEventResult().message("Test"))
        nova_message_event.stop_event()

        assert nova_message_event.is_stopped() is True

    def test_continue_event_creates_result_if_none(self, nova_message_event):
        """Test continue_event creates result if none exists."""
        nova_message_event.continue_event()

        assert nova_message_event._result is not None
        assert nova_message_event.is_stopped() is False

    def test_continue_event_with_existing_result(self, nova_message_event):
        """Test continue_event with existing result."""
        nova_message_event.set_result(MessageEventResult().message("Test"))
        nova_message_event.stop_event()
        nova_message_event.continue_event()

        assert nova_message_event.is_stopped() is False

    def test_is_stopped_default_false(self, nova_message_event):
        """Test is_stopped returns False by default."""
        assert nova_message_event.is_stopped() is False


class TestIsPrivateChat:
    """Tests for is_private_chat method."""

    def test_is_private_chat_true(self, nova_message_event):
        """Test is_private_chat returns True for friend message."""
        assert nova_message_event.is_private_chat() is True

    def test_is_private_chat_false(self, platform_meta, novabot_message):
        """Test is_private_chat returns False for group message."""
        novabot_message.type = MessageType.GROUP_MESSAGE
        event = ConcreteBulinMessageEvent(
            message_str="test",
            message_obj=novabot_message,
            platform_meta=platform_meta,
            session_id="session123",
        )
        assert event.is_private_chat() is False


class TestIsWakeUp:
    """Tests for is_wake_up method."""

    def test_is_wake_up_default_false(self, nova_message_event):
        """Test is_wake_up returns False by default."""
        assert nova_message_event.is_wake_up() is False

    def test_is_wake_up_when_set(self, nova_message_event):
        """Test is_wake_up returns True when is_wake is set."""
        nova_message_event.is_wake = True
        assert nova_message_event.is_wake_up() is True


class TestIsAdmin:
    """Tests for is_admin method."""

    def test_is_admin_default_false(self, nova_message_event):
        """Test is_admin returns False by default."""
        assert nova_message_event.is_admin() is False

    def test_is_admin_when_admin(self, nova_message_event):
        """Test is_admin returns True when role is admin."""
        nova_message_event.role = "admin"
        assert nova_message_event.is_admin() is True


class TestProcessBuffer:
    """Tests for process_buffer method."""

    @pytest.mark.asyncio
    async def test_process_buffer_splits_by_pattern(self, nova_message_event):
        """Test process_buffer splits buffer by pattern."""
        buffer = "Line 1\nLine 2\nLine 3\nRemaining"
        pattern = re.compile(r".*\n")

        with patch.object(
            nova_message_event, "send", new_callable=AsyncMock
        ) as mock_send:
            result = await nova_message_event.process_buffer(buffer, pattern)

            # Should have sent 3 lines and remaining should be "Remaining"
            assert mock_send.call_count == 3
            assert result == "Remaining"

    @pytest.mark.asyncio
    async def test_process_buffer_no_match(self, nova_message_event):
        """Test process_buffer returns original when no match."""
        buffer = "No newlines here"
        pattern = re.compile(r"\n")

        result = await nova_message_event.process_buffer(buffer, pattern)

        assert result == "No newlines here"


class TestResultHelpers:
    """Tests for result helper methods."""

    def test_make_result(self, nova_message_event):
        """Test make_result creates empty MessageEventResult."""
        result = nova_message_event.make_result()
        assert isinstance(result, MessageEventResult)

    def test_plain_result(self, nova_message_event):
        """Test plain_result creates result with text."""
        result = nova_message_event.plain_result("Hello")

        assert isinstance(result, MessageEventResult)
        assert len(result.chain) == 1
        assert isinstance(result.chain[0], Plain)
        assert result.chain[0].text == "Hello"

    def test_image_result_url(self, nova_message_event):
        """Test image_result with URL."""
        result = nova_message_event.image_result("http://example.com/image.jpg")

        assert isinstance(result, MessageEventResult)
        assert len(result.chain) == 1
        assert isinstance(result.chain[0], Image)

    def test_image_result_path(self, nova_message_event):
        """Test image_result with file path."""
        result = nova_message_event.image_result("/path/to/image.jpg")

        assert isinstance(result, MessageEventResult)
        assert len(result.chain) == 1
        assert isinstance(result.chain[0], Image)


class TestGetResult:
    """Tests for get_result and clear_result methods."""

    def test_get_result_returns_none_by_default(self, nova_message_event):
        """Test get_result returns None by default."""
        assert nova_message_event.get_result() is None

    def test_get_result_returns_set_result(self, nova_message_event):
        """Test get_result returns set result."""
        result = MessageEventResult().message("Test")
        nova_message_event.set_result(result)

        assert nova_message_event.get_result() == result

    def test_clear_result(self, nova_message_event):
        """Test clear_result clears the result."""
        nova_message_event.set_result(MessageEventResult().message("Test"))
        nova_message_event.clear_result()

        assert nova_message_event.get_result() is None


class TestShouldCallLlm:
    """Tests for should_call_llm method."""

    def test_should_call_llm_default(self, nova_message_event):
        """Test call_llm default is False."""
        assert nova_message_event.call_llm is False

    def test_should_call_llm_when_set(self, nova_message_event):
        """Test should_call_llm sets call_llm."""
        nova_message_event.should_call_llm(True)
        assert nova_message_event.call_llm is True


class TestRequestLlm:
    """Tests for request_llm method."""

    def test_request_llm_basic(self, nova_message_event):
        """Test request_llm creates ProviderRequest."""
        request = nova_message_event.request_llm(prompt="Hello")

        assert request.prompt == "Hello"
        assert request.session_id == ""
        assert request.image_urls == []
        assert request.contexts == []

    def test_request_llm_with_all_params(self, nova_message_event):
        """Test request_llm with all parameters."""
        request = nova_message_event.request_llm(
            prompt="Hello",
            session_id="session123",
            image_urls=["http://example.com/img.jpg"],
            contexts=[{"role": "user", "content": "Hi"}],
            system_prompt="You are helpful",
        )

        assert request.prompt == "Hello"
        assert request.session_id == "session123"
        assert request.image_urls == ["http://example.com/img.jpg"]
        assert request.contexts == [{"role": "user", "content": "Hi"}]
        assert request.system_prompt == "You are helpful"


class TestSendStreaming:
    """Tests for send_streaming method."""

    @pytest.mark.asyncio
    async def test_send_streaming_sets_has_send_oper(self, nova_message_event):
        """Test send_streaming sets _has_send_oper flag."""
        assert nova_message_event._has_send_oper is False

        async def generator():
            yield MessageEventResult().message("Test")

        with patch(
            "novabot.core.platform.nova_message_event.Metric.upload",
            new_callable=AsyncMock,
        ):
            await nova_message_event.send_streaming(generator())

        assert nova_message_event._has_send_oper is True


class TestSendTyping:
    """Tests for send_typing method."""

    @pytest.mark.asyncio
    async def test_send_typing_default_empty(self, nova_message_event):
        """Test send_typing default implementation is empty."""
        # Should not raise any exception
        await nova_message_event.send_typing()


class TestStopTyping:
    """Tests for stop_typing method."""

    @pytest.mark.asyncio
    async def test_stop_typing_default_empty(self, nova_message_event):
        """Test stop_typing default implementation is empty."""
        await nova_message_event.stop_typing()


class TestReact:
    """Tests for react method."""

    @pytest.mark.asyncio
    async def test_react_sends_emoji(self, nova_message_event):
        """Test react sends emoji as message."""
        with patch.object(
            nova_message_event, "send", new_callable=AsyncMock
        ) as mock_send:
            await nova_message_event.react("👍")

            mock_send.assert_called_once()
            call_arg = mock_send.call_args[0][0]
            # MessageChain is a dataclass with chain attribute
            assert len(call_arg.chain) == 1
            assert isinstance(call_arg.chain[0], Plain)
            assert call_arg.chain[0].text == "👍"


class TestGetGroup:
    """Tests for get_group method."""

    @pytest.mark.asyncio
    async def test_get_group_returns_none_for_private(self, nova_message_event):
        """Test get_group returns None for private chat."""
        result = await nova_message_event.get_group()
        assert result is None

    @pytest.mark.asyncio
    async def test_get_group_with_group_id_param(self, nova_message_event):
        """Test get_group with group_id parameter."""
        # Default implementation returns None
        result = await nova_message_event.get_group(group_id="group123")
        assert result is None


class TestMessageTypeHandling:
    """Tests for message type handling edge cases."""

    def test_message_type_from_valid_string(self, platform_meta):
        """Valid MessageType string should be converted correctly."""
        message = NovaBotMessage()
        message.type = "FRIEND_MESSAGE"
        message.message = []
        event = ConcreteBulinMessageEvent(
            message_str="test",
            message_obj=message,
            platform_meta=platform_meta,
            session_id="session123",
        )
        assert event.session.message_type == MessageType.FRIEND_MESSAGE
        assert event.get_message_type() == MessageType.FRIEND_MESSAGE

    def test_message_type_from_invalid_string_defaults_to_friend(self, platform_meta):
        """Invalid message type should default to FRIEND_MESSAGE."""
        message = NovaBotMessage()
        message.type = "InvalidMessageType"
        message.message = []
        event = ConcreteBulinMessageEvent(
            message_str="test",
            message_obj=message,
            platform_meta=platform_meta,
            session_id="session123",
        )
        assert event.session.message_type == MessageType.FRIEND_MESSAGE
        assert event.get_message_type() == MessageType.FRIEND_MESSAGE

    def test_message_type_from_none_defaults_to_friend(self, platform_meta):
        """None message type should default to FRIEND_MESSAGE."""
        message = NovaBotMessage()
        message.type = None
        message.message = []
        event = ConcreteBulinMessageEvent(
            message_str="test",
            message_obj=message,
            platform_meta=platform_meta,
            session_id="session123",
        )
        assert event.session.message_type == MessageType.FRIEND_MESSAGE
        assert event.get_message_type() == MessageType.FRIEND_MESSAGE

    def test_message_type_from_integer_defaults_to_friend(self, platform_meta):
        """Integer message type should default to FRIEND_MESSAGE."""
        message = NovaBotMessage()
        message.type = 123
        message.message = []
        event = ConcreteBulinMessageEvent(
            message_str="test",
            message_obj=message,
            platform_meta=platform_meta,
            session_id="session123",
        )
        assert event.session.message_type == MessageType.FRIEND_MESSAGE
        assert event.get_message_type() == MessageType.FRIEND_MESSAGE


class TestDefensiveGetattr:
    """Tests for defensive getattr behavior in NovaMessageEvent."""

    def test_get_messages_without_message_attr(self, nova_message_event):
        """get_messages should handle message_obj without 'message' attribute."""
        nova_message_event.message_obj = type("DummyMessage", (), {})()
        messages = nova_message_event.get_messages()
        assert isinstance(messages, list)

    def test_get_message_type_without_type_attr(self, nova_message_event):
        """get_message_type should handle message_obj without 'type' attribute."""
        nova_message_event.message_obj = type("DummyMessage", (), {})()
        message_type = nova_message_event.get_message_type()
        assert isinstance(message_type, MessageType)

    def test_get_sender_fields_without_sender_attr(self, nova_message_event):
        """get_sender_id and get_sender_name should handle missing 'sender'."""
        nova_message_event.message_obj = type("DummyMessage", (), {})()
        sender_id = nova_message_event.get_sender_id()
        sender_name = nova_message_event.get_sender_name()
        assert isinstance(sender_id, str)
        assert isinstance(sender_name, str)

    def test_get_message_type_with_non_enum_type(self, nova_message_event):
        """get_message_type should handle message_obj.type that is not a MessageType."""

        class DummyMessage:
            def __init__(self):
                self.type = "not_an_enum"
                self.message = []

        nova_message_event.message_obj = DummyMessage()
        message_type = nova_message_event.get_message_type()
        assert isinstance(message_type, MessageType)
