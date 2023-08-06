from typing import Optional

__all__ = [
    "NLP_NER"
]


class NLP_NER:
    def __init__(
        self,
        data,
        client,
        sentence_split: Optional[bool] = False
    ):
        """
        NLP named_entity_recognition Object
        """
        self._client = client
        if sentence_split:
            self.sentences = data["sentences"]
        else:
            self.ner_tags = data["ner_tags"]
        self.text = data["text"]
        self.source_language = data["source_language"]