from pydantic import BaseModel
from typing import List



class Endpoint(BaseModel):

    path: str

    method: str

    entity: str

    endpoint_type: str = "resource"

    auth_required: bool

    roles: List[str]



class APISchema(BaseModel):
    endpoints: List[Endpoint]