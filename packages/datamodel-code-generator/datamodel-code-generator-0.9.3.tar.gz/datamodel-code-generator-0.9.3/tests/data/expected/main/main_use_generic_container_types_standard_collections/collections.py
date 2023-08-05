# generated by datamodel-codegen:
#   filename:  modular.yaml
#   timestamp: 1985-10-26T08:21:00+00:00

from __future__ import annotations

from collections.abc import Sequence
from typing import Optional

from pydantic import AnyUrl, BaseModel, Field

from . import models


class Pets(BaseModel):
    __root__: Sequence[models.Pet]


class Users(BaseModel):
    __root__: Sequence[models.User]


class Rules(BaseModel):
    __root__: Sequence[str]


class Api(BaseModel):
    apiKey: Optional[str] = Field(
        None, description='To be used as a dataset parameter value'
    )
    apiVersionNumber: Optional[str] = Field(
        None, description='To be used as a version parameter value'
    )
    apiUrl: Optional[AnyUrl] = Field(
        None, description="The URL describing the dataset's fields"
    )
    apiDocumentationUrl: Optional[AnyUrl] = Field(
        None, description='A URL to the API console for each API'
    )


class Apis(BaseModel):
    __root__: Sequence[Api]
