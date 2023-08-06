__all__ = ['LydiaSession', 'Session']


class LydiaSession:
    def __init__(self, data, client):
        """
        AI Session Object
        """
        self._client = client
        try:
            self.id = data['session_id']
            self.language = data['language']
            self.available = data['available']
            self.expires = data['expires']
        except KeyError:
            self.ai_emotion = data['ai_emotion']
            self.ai_emotion_probability = data['ai_emotion_probability']
            self.current_language = data['current_language']
            self.current_language_probability = data['current_language_probability']
    

    def think_thought(self, text):
        """
        Processes user input and returns an AI text Response

        :type text: str
        :param text: The user input
        :raises: CoffeeHouseError
        :returns: The JSON response from the server
        :rtype: str
        """

        return self._client.think_thought(self.id, text)

    def get_attributes(self):
        """
        Returns Session Attributes
        :type text: str
        :param text: session_id
        :raises: CoffeeHouseError
        :returns: The JSON response from the server
        :rtype: str
        """
        return self._client.get_session_attributes(self.id)

    def __str__(self):
        """
        Returns an identifier uniquely specifying this session

        :returns: The session id
        :rtype: str
        """

        return self.id


Session = LydiaSession  # For compatibility
