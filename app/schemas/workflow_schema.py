
from pydantic import BaseModel
from typing import Optional


class WorkflowTrigger(BaseModel):

    entity: str

    event: str

    condition: Optional[str] = None


class WorkflowStub(BaseModel):

    name: str

    trigger: WorkflowTrigger

    integration: str

    action: str

    payload: dict

