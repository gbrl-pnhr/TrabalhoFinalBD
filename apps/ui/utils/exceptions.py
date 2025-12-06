class AppError(Exception):
    """Base exception for the application."""
    def __init__(self, message: str, original_error: Exception = None):
        super().__init__(message)
        self.original_error = original_error

class APIConnectionError(AppError):
    """Raised when the backend is unreachable."""
    pass

class ResourceNotFoundError(AppError):
    """Raised when the API returns 404."""
    pass

class ValidationError(AppError):
    """Raised when the API returns 422 or 400."""
    pass