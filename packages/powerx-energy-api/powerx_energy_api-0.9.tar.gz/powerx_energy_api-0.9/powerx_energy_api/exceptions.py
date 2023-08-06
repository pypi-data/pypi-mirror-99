"""The exceptions used by PowerX Energy API Wrapper."""

class InvalidCredentialsError(Exception):
    """Error when email or password is incorrect"""

class ConnectionError(Exception):
    """Error while connecting to powerx energy api server"""    