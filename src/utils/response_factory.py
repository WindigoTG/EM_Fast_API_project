from fastapi import status
from fastapi.responses import JSONResponse

from src.schemas.responses import BaseErrorResponse, BaseNotFoundResponse


class ResponseFactory:
    @classmethod
    def get_base_error_response(
        cls,
        reason: str,
        status_code: int = status.HTTP_400_BAD_REQUEST,
    ) -> JSONResponse:
        return JSONResponse(
            content=BaseErrorResponse(
                reason=reason
            ).model_dump(),
            status_code=status_code
        )

    @classmethod
    def get_not_found_response(
        cls,
        reason: str,
    ) -> JSONResponse:
        return JSONResponse(
            content=BaseNotFoundResponse(
                reason=reason
            ).model_dump(),
            status_code=status.HTTP_404_NOT_FOUND
        )