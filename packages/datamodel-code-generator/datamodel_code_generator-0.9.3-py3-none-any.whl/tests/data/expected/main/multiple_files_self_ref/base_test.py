# generated by datamodel-codegen:
#   filename:  base_test.json
#   timestamp: 2019-07-26T00:00:00+00:00

from __future__ import annotations

from pydantic import BaseModel


class Model(BaseModel):
    pass


class Second(BaseModel):
    __root__: str


class First(BaseModel):
    __root__: Second
