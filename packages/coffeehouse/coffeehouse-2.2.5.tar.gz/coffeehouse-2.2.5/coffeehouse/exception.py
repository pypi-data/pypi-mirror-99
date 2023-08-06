import json


__all__ = ['CoffeeHouseError']


class CoffeeHouseError(Exception):

    def __init__(self, status_code, content, request_id, response):
        """
        CoffeeHouseError Public Constructor
        :param status_code:
        :param content:
        :param request_id:
        :param response:
        """

        self.status_code = status_code
        self.content = content
        self.response = response
        self.request_id = request_id
        self.message = None
        self.error_code = None
        self.type = None
        # This part can be improved
        if content is not None:
            self.message = content['error']['message']
            self.error_code = content['error']['error_code']
            self.type = content['error']['type']
        super().__init__(self.message or content)

    @staticmethod
    def parse_and_raise(status_code, response, request_id):
        """
        Parses the response and detects the error type
        :param status_code:
        :param response:
        :param request_id:
        :return:
        """

        try:
            content = json.loads(response)
        except json.decoder.JSONDecodeError:
            raise CoffeeHouseError(status_code, None, request_id, response)

        # Parse the response
        if content['success'] is False:
            # Check if the type is available
            if 'error' in content and 'type' in content['error']:
                # COA Exception handler
                raise _mapping.get(
                    content['error']['error_code'],
                    CoffeeHouseError,
                )(status_code, content, request_id, response)
            # If detecting the type fails, it's a generic error
            raise CoffeeHouseError(status_code, content, request_id, response)
        return content


class InternalServerError(CoffeeHouseError):
    """
    An unexpected internal server error,
    this incident should be reported to support
    """
    pass


class ServiceError(CoffeeHouseError):
    """
    This error can be a generic error,
    see the error message for more details
    """
    pass

class EmptyOutputRequest(Exception):
    pass

_mapping = {
    -1: InternalServerError,
    0: ServiceError,
}
