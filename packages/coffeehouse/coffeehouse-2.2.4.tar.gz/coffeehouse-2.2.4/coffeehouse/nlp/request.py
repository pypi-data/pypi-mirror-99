from .nlp import NLP_NER
from ..api import API
from typing import Optional

__all__ = ["NLP"]


class NLP(API):
    def __init__(self, *args, **kwargs):
        """
        Public constructor for nlp
        :param access_key:
        :param endpoint:
        """

        super().__init__(*args, **kwargs)

    def named_entity_recognition(
        self,
        text,
        language='en',
        sentence_split: Optional[bool] = False
    ):
        """
        Creates a new NER request to the API

        :type text: str
        :param text: The user input
        :raises: CoffeeHouseError
        :returns: The json payload of the response
        :rtype: str
        """
        if sentence_split:
            return NLP_NER(
                self._send(
                    "v1/nlp/named_entity_recognition",
                    input=text,
                    language=language,
                    sentence_split=1,
                ),
                self,
                sentence_split=True
            )
        else:
            return NLP_NER(
                self._send(
                    "v1/nlp/named_entity_recognition",
                    input=text,
                    language=language,
                    sentence_split=0,
                ),
                self,
                sentence_split=False
            )