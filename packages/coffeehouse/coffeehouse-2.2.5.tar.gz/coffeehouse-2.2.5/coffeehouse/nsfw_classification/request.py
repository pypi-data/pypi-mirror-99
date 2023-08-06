import base64

from ..api import API
from .classifier import NSFW_Classifier


__all__ = ['NsfwClassifier']


class NsfwClassifier(API):
    def __init__(self, *args, **kwargs):
        """
        Public constructor for nsfw_classification
        :param access_key:
        :param endpoint:
        """

        super().__init__(*args, **kwargs)

    def classify(self, image):
        """
        Creates a new NSFW Classification to the API

        :type image: bytes
        :param image: The bytes of image that will be sent
        :raises: CoffeeHouseError
        :returns: The results of nsfw image
        :rtype: NSFWClassifier
        """

        return NSFW_Classifier(
            self._send(
                'v1/image/nsfw_classification',
                image=base64.b64encode(image),
            ),
            self,
        )
