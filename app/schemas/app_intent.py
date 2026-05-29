
from pydantic import BaseModel
from typing import List, Literal


class AppIntent(BaseModel):

    appName: str

    appType: Literal[
        "crm",
        "project_management",
        "ecommerce",
        "hr_tool",
        "inventory",
        "content_platform",
        "analytics",
        "custom"
    ]

    features: List[str]

    entities: List[str]

    integrations_requested: List[str]

    assumptions: List[str]

    clarification_required: bool = False

    clarification_question: str | None = None

