from typing import Optional


class APIError(Exception):
    """Base API error class"""

    def __init__(self, message: Optional[str], status: int):
        self.status = status

        super().__init__(message)
