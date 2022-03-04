from fastapi.exceptions import HTTPException


class TestRequestException(HTTPException):
    pass


class DevToException(HTTPException):
    pass
