from pydantic import BaseModel
from typing import List


class IntentIR(BaseModel):

    app_name: str

    features: List[str]

    roles: List[str]

    entities: List[str]