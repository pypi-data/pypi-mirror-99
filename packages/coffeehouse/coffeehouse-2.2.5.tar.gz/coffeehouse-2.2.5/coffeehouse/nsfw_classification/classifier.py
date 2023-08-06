from ..utils import attrdict

__all__ = ['Classifier', 'NSFW_Classifier']


class NSFW_Classifier:
    def __init__(
        self,
        data,
        client,
    ):
        """
        NSFW Classifier Object
        """
        self._client = client
        self.nsfw_classification = attrdict(data['nsfw_classification'])


Classifier = NSFW_Classifier  # For compatibility
