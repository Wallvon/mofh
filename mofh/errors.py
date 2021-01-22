class APIError(Exception):
    """Base API error class"""

    def __init__(self, message: str, status: str):
        self.status = status

        super().__init__(message)