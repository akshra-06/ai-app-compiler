
from pydantic import BaseModel
from typing import List

from app.schemas.workflow_schema import (
    WorkflowStub
)


class PageSpec(BaseModel):

    name: str

    route: str

    layout: str

    boundEntity: str

    components: List[str]


class ApiEndpointSpec(BaseModel):

    path: str

    method: str

    handlerDescription: str

    boundEntity: str

    authRequired: bool

    rateLimited: bool


class PermissionRule(BaseModel):

    entity: str

    read: bool

    write: bool

    delete: bool


class RoleSpec(BaseModel):

    role: str

    permissions: List[PermissionRule]


class IntegrationHook(BaseModel):

    integrationId: str

    triggerEntity: str

    action: str


class AppSpec(BaseModel):

    pages: List[PageSpec]

    apiEndpoints: List[ApiEndpointSpec]

    authRules: List[RoleSpec]

    integrationHooks: List[
        IntegrationHook
    ]

    workflowStubs: List[
        WorkflowStub
    ]

