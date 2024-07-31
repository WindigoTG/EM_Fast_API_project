from pydantic import BaseModel


class BaseResponse(BaseModel):
    status: int = 200
    error: bool = False


class BaseErrorResponse(BaseResponse):
    status: int = 400
    error: bool = True
    reason: str


class BaseNotFoundResponse(BaseErrorResponse):
    status: int = 404
