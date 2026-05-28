from pydantic import BaseModel
from typing import List


class Component(BaseModel):

    type: str

    name: str


class Page(BaseModel):

    name: str

    route: str

    roles: List[str]

    components: List[Component]


class UISchema(BaseModel):

    pages: List[Page]