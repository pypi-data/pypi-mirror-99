# generated by datamodel-codegen:
#   filename:  api.yaml
#   timestamp: 2019-07-26T00:00:00+00:00

from typing import (
    List,
    Optional,
)

from pydantic import (
    AnyUrl,
    BaseModel,
    Field,
)


class Pet(BaseModel):
    id: int
    name: str
    tag: Optional[str]


class Pets(BaseModel):
    __root__: List["Pet"]


class User(BaseModel):
    id: int
    name: str
    tag: Optional[str]


class Users(BaseModel):
    __root__: List["User"]


class Id(BaseModel):
    __root__: str


class Rules(BaseModel):
    __root__: List[str]


class Error(BaseModel):
    code: int
    message: str


class Api(BaseModel):
    api_key: Optional[
        str
    ] = Field(
        None,
        alias="apiKey",
        description="To be used as a dataset parameter value",
    )
    api_version_number: Optional[
        str
    ] = Field(
        None,
        alias="apiVersionNumber",
        description="To be used as a version parameter value",
    )
    api_url: Optional[
        AnyUrl
    ] = Field(
        None,
        alias="apiUrl",
        description="The URL describing the dataset's fields",
    )
    api_documentation_url: Optional[
        AnyUrl
    ] = Field(
        None,
        alias="apiDocumentationUrl",
        description="A URL to the API console for each API",
    )


class Apis(BaseModel):
    __root__: List["Api"]


class Event(BaseModel):
    name: Optional[str]


class Result(BaseModel):
    event: Optional["Event"]
