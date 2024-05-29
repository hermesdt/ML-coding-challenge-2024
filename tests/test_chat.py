import pytest
from unittest.mock import Mock
from src.chat import Chat
from src.message import Message
from datetime import datetime
from typing import List
from itertools import count as Counter

@pytest.fixture(autouse=True)
def patch_uuid4(monkeypatch):
    """
    Patch uuid4 to return a fixed value
    """
    counter = Counter()
    monkeypatch.setattr("src.message.uuid4", lambda: Mock(hex=str(next(counter))))

@pytest.fixture
def summarizer():
    summarizer = Mock()

    def summarize(messages: List[Message]):
        message_ids = [msg.id for msg in messages]
        return "Summary of messages: " + str(message_ids)
    summarizer.summarize.side_effect = summarize

    return summarizer

def test_add_message():
    chat = Chat()
    chat.add_message("Hello, world!")
    assert len(chat.messages) == 1
    assert chat.messages[0].text == "Hello, world!"
    assert chat.messages[0].position == 0
    assert chat.messages[0].created_at <= datetime.now()

def test_compact_messages(summarizer):
    chat = Chat()
    for i in range(10):
        chat.add_message(f"Message {i}")
    assert len(chat.messages) == 10

    chat.compact_messages(summarizer, every_n=3)
    assert len(chat.messages) == 4

    assert chat.messages[0].position == 2
    assert chat.messages[0].text == "Summary of messages: ['0', '1', '2']"
    assert chat.messages[1].position == 5
    assert chat.messages[1].text == "Summary of messages: ['3', '4', '5']"
    assert chat.messages[2].position == 8
    assert chat.messages[2].text == "Summary of messages: ['6', '7', '8']"
    assert chat.messages[3].position == 9
    assert chat.messages[3].text == "Message 9"

    # nothing happens as it's already compacted
    chat.compact_messages(summarizer, every_n=3)
    assert len(chat.messages) == 4

def test_compact_messages_no_compaction_no_consecutive_ids(summarizer):
    chat = Chat()
    for i in range(10):
        chat.add_message(f"Message {i}")

    chat.messages.pop(7)
    chat.messages.pop(5)
    chat.messages.pop(2)
    chat.compact_messages(summarizer, every_n=3)

    assert [m.position for m in chat.messages] == [0, 1, 3, 4, 6, 8, 9]

def test_compact_messages_no_compaction(summarizer):
    chat = Chat()
    for i in range(10):
        chat.add_message(f"Message {i}")
    assert len(chat.messages) == 10

    chat.compact_messages(summarizer, every_n=1)
    assert len(chat.messages) == 10
    