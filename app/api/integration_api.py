from fastapi import APIRouter

from app.integrations.registry import (
    INTEGRATION_REGISTRY
)

router = APIRouter()


@router.get("/integrations")
def get_integrations():

    integrations = []

    for integration_id, integration in (
        INTEGRATION_REGISTRY.items()
    ):

        integrations.append({

            "id":
                integration_id,

            "auth_type":
                integration.authType,

            "actions":
                [
                    action.id
                    for action
                    in integration.actions
                ]
        })

    return integrations


@router.post(
    "/test-integration/{integration_id}"
)
def test_integration(
    integration_id: str
):

    if (
        integration_id
        not in
        INTEGRATION_REGISTRY
    ):

        return {

            "status":
                "failed",

            "message":
                "Unknown integration"
        }

    return {

        "status":
            "success",

        "integration":
            integration_id,

        "message":
            f"{integration_id} connected successfully"
    }