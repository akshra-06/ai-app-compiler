from pydantic import BaseModel
from typing import List


class Field(BaseModel):
    name: str
    type: str


class Entity(BaseModel):
    name: str
    fields: List[Field]


class Relationship(BaseModel):
    from_entity: str
    to_entity: str
    relation_type: str


class ArchitectureGraph(BaseModel):
    entities: List[Entity]
    relationships: List[Relationship]