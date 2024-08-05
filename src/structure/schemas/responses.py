from src.schemas.responses import BaseCreateResponse, BaseResponse
from src.structure.schemas.division import DivisionSchema
from src.structure.schemas.division_position import DivisionPositionSchema
from src.structure.schemas.position import PositionSchema


class DivisionCreateResponse(BaseCreateResponse):
    data: DivisionSchema


class DivisionResponse(BaseResponse):
    data: DivisionSchema


class DivisionPositionCreateResponse(BaseCreateResponse):
    data: DivisionPositionSchema


class DivisionPositionResponse(BaseResponse):
    data: DivisionPositionSchema


class PositionCreateResponse(BaseCreateResponse):
    data: PositionSchema


class PositionResponse(BaseResponse):
    data: PositionSchema
