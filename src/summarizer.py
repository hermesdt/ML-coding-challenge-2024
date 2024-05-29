from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from transformers import pipeline, Pipeline
from src.config import SUMMARIZER_MODEL_ID
from src.message import Message

class Summarizer(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    summarizer_model_id: str = SUMMARIZER_MODEL_ID
    model: Pipeline = None

    def _get_model(self):
        if not self.model:
            self.model = pipeline("summarization", model=self.summarizer_model_id)

        return self.model

    def summarize(self, messages: List[Message]):
        """
        Summarize a list of messages using a pre-trained model
        """

        concatenated_msgs = "\n".join([message.text for message in messages])
        model = self._get_model()
        summary = model(concatenated_msgs)
        return summary
