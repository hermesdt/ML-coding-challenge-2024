from unittest.mock import Mock
from src.summarizer import Summarizer
from src.message import Message
from datetime import datetime

def _get_model():
    model = Mock()
    model.side_effect = lambda text: text[:10]
    return model

def test_summarize():
    summarizer = Summarizer()
    summarizer._get_model = _get_model

    messages = [
        Message(text="hello", position=0, created_at=datetime.now()),
        Message(text="how", position=1, created_at=datetime.now()),
        Message(text="are", position=2, created_at=datetime.now()),
        Message(text="you", position=3, created_at=datetime.now())
    ]
    assert summarizer.summarize(messages) == "hello\nhow\n"
