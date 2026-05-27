from fastapi import HTTPException, status


class AppException(HTTPException):
    """Base application HTTP exception."""

    def __init__(self, status_code: int, detail: str, code: str | None = None) -> None:
        super().__init__(status_code=status_code, detail=detail)
        self.code = code


class UnauthorizedError(AppException):
    def __init__(self, detail: str = "Not authenticated") -> None:
        super().__init__(status.HTTP_401_UNAUTHORIZED, detail, code="unauthorized")


class ForbiddenError(AppException):
    def __init__(self, detail: str = "Forbidden") -> None:
        super().__init__(status.HTTP_403_FORBIDDEN, detail, code="forbidden")


class ConflictError(AppException):
    def __init__(self, detail: str = "Conflict") -> None:
        super().__init__(status.HTTP_409_CONFLICT, detail, code="conflict")


class BadRequestError(AppException):
    def __init__(self, detail: str = "Bad request") -> None:
        super().__init__(status.HTTP_400_BAD_REQUEST, detail, code="bad_request")
