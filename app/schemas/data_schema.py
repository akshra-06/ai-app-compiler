
from pydantic import BaseModel
from typing import List, Literal


class FieldSchema(BaseModel):

    name: str

    type: str

    nullable: bool = False

    isRelation: bool = False

    isPrimary: bool = False

    isUnique: bool = False


class RelationSchema(BaseModel):

    type: Literal[
        "hasMany",
        "belongsTo",
        "hasOne"
    ]

    target: str

    foreignKey: str

    onDelete: str


class EntitySchema(BaseModel):

    name: str

    tableName: str

    fields: List[FieldSchema]

    relations: List[RelationSchema]


class DataSchema(BaseModel):

    entities: List[EntitySchema]

