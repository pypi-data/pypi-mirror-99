# generated by datamodel-codegen:
#   filename:  modular.yaml
#   timestamp: 1985-10-26T08:21:00+00:00

from __future__ import annotations

from typing import Any, Mapping, Optional, Sequence

from pydantic import BaseModel


class Thing(BaseModel):
    attributes: Optional[Mapping[str, Any]] = None


class Thang(BaseModel):
    attributes: Optional[Sequence[Mapping[str, Any]]] = None


class Clone(Thing):
    pass
