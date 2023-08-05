class NoInternetConnectionException(Exception):
    """
    Exception indicating no internet connection is present
    """
    pass


class UnauthorizedException(Exception):
    """
    Exception to indicate that access is denied to the cloud api.
    """
    pass


class UnknownAuthenticationException(Exception):
    """
    Exception to indicate that something went wrong in the cloud during authentication;
    possibly an unexpected error was raised in the cloud.
    """
    pass


class UnknownCloudException(Exception):
    """
    Exception to indicate that something went wrong in the cloud; possibly an unexpected error was raised in the cloud.
    """
    pass


class BadRequestException(Exception):
    """
    Exception to indicate that the input to the rest-api was incorrect.
    """
    pass


class SafetyViolation(Exception):
    """
    Exception that is raised when a fixed-time schedule does not satisfy all safety restrictions
    """
    pass
