class BaseHttpTypeError(Exception):
    """Exception that includes a status code for http response in addition to an error message.
    """

    def __init__(self, http_status_code: int, error_message: str):
        self.http_status_code = http_status_code
        self.error_message = error_message


class TokenIsNotJWT(BaseHttpTypeError):
    """Exception when the provided bearer token is not a JWT.
    This is indicative that you may be passing the legacy Brighthive bearer token.
    """
    pass


class FailedToDecodeJwt(BaseHttpTypeError):
    pass


class AuthorizationError(BaseHttpTypeError):
    pass
