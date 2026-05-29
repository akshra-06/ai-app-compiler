
from copy import deepcopy

from app.integrations.registry import (
    INTEGRATION_REGISTRY
)


def repair_appspec(
    data_schema,
    app_spec,
    validation_errors
):

    repaired_spec = deepcopy(
        app_spec
    )

    repair_log = []

    valid_entities = {

        entity.name

        for entity
        in data_schema.entities
    }

    # -----------------------------------
    # REPAIR LOOP
    # -----------------------------------

    for error in validation_errors:

        error_type = error["type"]

        # ===================================
        # CONSISTENCY REPAIR
        # ===================================

        if (
            error_type
            == "missing_api_for_page"
        ):

            message = error["message"]

            for page in repaired_spec.pages:

                if page.name in message:

                    repaired_spec.apiEndpoints.append({

                        "path":
                            f"/api/{page.boundEntity.lower()}s",

                        "method":
                            "GET",

                        "handlerDescription":
                            f"Auto-generated endpoint "
                            f"for {page.boundEntity}",

                        "boundEntity":
                            page.boundEntity,

                        "authRequired":
                            True,

                        "rateLimited":
                            True
                    })

                    repair_log.append({

                        "strategy":
                            "consistency_repair",

                        "error":
                            error,

                        "outcome":
                            "repaired"
                    })

        # ===================================
        # INVALID INTEGRATION REPAIR
        # ===================================

        elif (
            error_type
            == "invalid_integration"
        ):

            for hook in (
                repaired_spec.integrationHooks
            ):

                if (
                    hook.integrationId
                    not in
                    INTEGRATION_REGISTRY
                ):

                    hook.integrationId = (
                        "webhook"
                    )

                    repair_log.append({

                        "strategy":
                            "field_repair",

                        "error":
                            error,

                        "outcome":
                            "repaired"
                    })

        # ===================================
        # INVALID WORKFLOW ENTITY
        # ===================================

        elif (
            error_type
            == "invalid_workflow_entity"
        ):

            fallback_entity = (
                next(
                    iter(valid_entities)
                )
            )

            for workflow in (
                repaired_spec.workflowStubs
            ):

                if (
                    workflow.trigger.entity
                    not in valid_entities
                ):

                    workflow.trigger.entity = (
                        fallback_entity
                    )

                    repair_log.append({

                        "strategy":
                            "consistency_repair",

                        "error":
                            error,

                        "outcome":
                            "repaired"
                    })

        # ===================================
        # INVALID WORKFLOW ACTION
        # ===================================

        elif (
            error_type
            == "invalid_workflow_action"
        ):

            for workflow in (
                repaired_spec.workflowStubs
            ):

                if (
                    workflow.integration
                    in INTEGRATION_REGISTRY
                ):

                    integration = (
                        INTEGRATION_REGISTRY[
                            workflow.integration
                        ]
                    )

                    fallback_action = (
                        integration.actions[0].id
                    )

                    workflow.action = (
                        fallback_action
                    )

                    repair_log.append({

                        "strategy":
                            "field_repair",

                        "error":
                            error,

                        "outcome":
                            "repaired"
                    })

    return {

        "repaired_spec":
            repaired_spec,

        "repair_log":
            repair_log
    }

