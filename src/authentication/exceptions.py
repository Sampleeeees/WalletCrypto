from starlette.exceptions import HTTPException
from starlette import status


class BadRequestException(HTTPException):
    """Кастомний exception для помилки валідації де потрібно вказати тільки detail"""
    def __init__(self, detail: str, status_code: int = status.HTTP_400_BAD_REQUEST):
        super().__init__(detail=detail, status_code=status_code)

class NotFoundException(HTTPException):
    """Кастомний exception що щось в системі не знайшли"""
    def __init__(self, detail: str, status_code: int = status.HTTP_404_NOT_FOUND):
        super().__init__(detail=detail, status_code=status_code)