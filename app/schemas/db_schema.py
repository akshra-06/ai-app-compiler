from pydantic import BaseModel
from typing import List


class Column(BaseModel):
    name: str
    type: str
    nullable: bool = False
    primary_key: bool = False


class Table(BaseModel):
    name: str
    columns: List[Column]


class DatabaseSchema(BaseModel):
    tables: List[Table]