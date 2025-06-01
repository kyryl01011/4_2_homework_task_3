from pydantic import BaseModel


class CtxModel(BaseModel):
    min_length: int | None = None


class ErrorItemsModel(BaseModel):
    loc: list[str | int]
    msg: str
    type: str
    ctx: CtxModel | None = None


class HTTPValidationErrorModel(BaseModel):
    detail: list[ErrorItemsModel]
