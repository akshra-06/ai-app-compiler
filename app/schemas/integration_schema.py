
from pydantic import BaseModel
from typing import List


class IntegrationAction(BaseModel):

    id: str

    description: str

    inputSchema: dict

    outputSchema: dict


class IntegrationTrigger(BaseModel):

    event: str

    description: str


class IntegrationDefinition(BaseModel):

    id: str

    displayName: str

    authType: str

    triggers: List[IntegrationTrigger]

    actions: List[IntegrationAction]

