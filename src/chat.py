from pydantic import BaseModel
from typing import List
from datetime import datetime
from src.message import Message, Summary
from src.summarizer import Summarizer

class Chat(BaseModel):
    messages: List[Message | Summary] = []

    def add_message(self, text: str):
        """
        Add a message to the chat
        """
        message = Message(text=text, position=len(self.messages), created_at=datetime.now())
        self.messages.append(message)

    def compact_messages(self, summarizer: Summarizer, every_n: int = 5):
        """
        Compact every n consecutive messages into a single summary
        """
        msgs_after_compaction = []
        msgs_to_be_compacted = []

        for message in self.messages:
            if not isinstance(message, Message):
                msgs_after_compaction.append(message)
                continue

            # if not consecutive messages, clear the buffer and start over
            if msgs_to_be_compacted and msgs_to_be_compacted[-1].position != message.position - 1:
                msgs_after_compaction.extend(msgs_to_be_compacted)
                msgs_to_be_compacted.clear()
                continue

            msgs_to_be_compacted.append(message)

            if len(msgs_to_be_compacted) == every_n:
                summary_text = summarizer.summarize(msgs_to_be_compacted)
                summary = Summary(text=summary_text, position=message.position, created_at=datetime.now(), message_ids=[msg.id for msg in msgs_to_be_compacted])

                msgs_after_compaction.append(summary)
                msgs_to_be_compacted.clear()

        msgs_after_compaction.extend(msgs_to_be_compacted)

        self.messages.clear()
        self.messages.extend(msgs_after_compaction)
        