
from app.schemas.app_spec import (
    AppSpec
)

from app.schemas.data_schema import (
    DataSchema
)

from app.integrations.registry import (
    INTEGRATION_REGISTRY
)


def validate_appspec(
    data_schema: DataSchema,
    app_spec: AppSpec
):

    errors = []

    # -----------------------------------
    # VALID ENTITY SET
    # -----------------------------------

    valid_entities = {

        entity.name

        for entity in data_schema.entities
    }

    # -----------------------------------
    # PAGE VALIDATION
    # -----------------------------------

    for page in app_spec.pages:

        if (
            page.boundEntity
            not in valid_entities
        ):

            errors.append({

                "type":
                    "invalid_page_entity",

                "message":
                    f"Page '{page.name}' "
                    f"references unknown entity "
                    f"'{page.boundEntity}'"
            })

    # -----------------------------------
    # PAGE → API CONSISTENCY
    # -----------------------------------

    api_entities = {

        endpoint.boundEntity

        for endpoint
        in app_spec.apiEndpoints
    }

    for page in app_spec.pages:

        if (
            page.boundEntity
            not in api_entities
        ):

            errors.append({

                "type":
                    "missing_api_for_page",

                "message":
                    f"Page '{page.name}' "
                    f"has no matching API endpoint"
            })

    # -----------------------------------
    # AUTH RULE VALIDATION
    # -----------------------------------

    for role in app_spec.authRules:

        for permission in (
            role.permissions
        ):

            if (
                permission.entity
                not in valid_entities
            ):

                errors.append({

                    "type":
                        "invalid_auth_entity",

                    "message":
                        f"Role '{role.role}' "
                        f"references invalid entity "
                        f"'{permission.entity}'"
                })

    # -----------------------------------
    # INTEGRATION HOOK VALIDATION
    # -----------------------------------

    for hook in (
        app_spec.integrationHooks
    ):

        if (
            hook.integrationId
            not in INTEGRATION_REGISTRY
        ):

            errors.append({

                "type":
                    "invalid_integration",

                "message":
                    f"Unknown integration "
                    f"'{hook.integrationId}'"
            })

            continue

        integration = (
            INTEGRATION_REGISTRY[
                hook.integrationId
            ]
        )

        valid_actions = {

            action.id

            for action
            in integration.actions
        }

        if (
            hook.action
            not in valid_actions
        ):

            errors.append({

                "type":
                    "invalid_integration_action",

                "message":
                    f"Integration "
                    f"'{hook.integrationId}' "
                    f"does not support "
                    f"action '{hook.action}'"
            })

    # -----------------------------------
    # WORKFLOW VALIDATION
    # -----------------------------------

    for workflow in (
        app_spec.workflowStubs
    ):

        if (
            workflow.trigger.entity
            not in valid_entities
        ):

            errors.append({

                "type":
                    "invalid_workflow_entity",

                "message":
                    f"Workflow "
                    f"'{workflow.name}' "
                    f"references invalid entity "
                    f"'{workflow.trigger.entity}'"
            })

        if (
            workflow.integration
            not in INTEGRATION_REGISTRY
        ):

            errors.append({

                "type":
                    "invalid_workflow_integration",

                "message":
                    f"Workflow "
                    f"'{workflow.name}' "
                    f"references unknown integration "
                    f"'{workflow.integration}'"
            })

            continue

        integration = (
            INTEGRATION_REGISTRY[
                workflow.integration
            ]
        )

        valid_actions = {

            action.id

            for action
            in integration.actions
        }

        if (
            workflow.action
            not in valid_actions
        ):

            errors.append({

                "type":
                    "invalid_workflow_action",

                "message":
                    f"Workflow "
                    f"'{workflow.name}' "
                    f"uses invalid action "
                    f"'{workflow.action}'"
            })

    return errors

