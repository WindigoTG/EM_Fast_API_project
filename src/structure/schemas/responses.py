from src.schemas.responses import BaseCreateResponse, BaseResponse
from src.structure.schemas.division import DivisionSchema


class DivisionCreateResponse(BaseCreateResponse):
    data: DivisionSchema


class DivisionResponse(BaseResponse):
    data: DivisionSchema
