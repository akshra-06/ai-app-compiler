
from app.integrations.registry import (
    INTEGRATION_REGISTRY
)


class PluginRuntime:

    def __init__(self):

        self.execution_log = []

    # -----------------------------------
    # EXECUTE ACTION
    # -----------------------------------

    def execute_action(

        self,

        integration_id,

        action,

        payload
    ):

        # -----------------------------
        # VALIDATE INTEGRATION
        # -----------------------------

        if (
            integration_id
            not in
            INTEGRATION_REGISTRY
        ):

            raise Exception(

                f"Unknown integration "
                f"'{integration_id}'"
            )

        integration = (
            INTEGRATION_REGISTRY[
                integration_id
            ]
        )

        # -----------------------------
        # VALIDATE ACTION
        # -----------------------------

        # -----------------------------
        # VALIDATE ACTION
        # -----------------------------

        valid_actions = {

            action_obj.id

            for action_obj
            in integration.actions
        }

        if action not in valid_actions:

            raise Exception(

                f"Action '{action}' "
                f"not supported "
                f"by '{integration_id}'"
            )


        # -----------------------------
        # MOCK EXECUTION
        # -----------------------------

        result = {

            "integration":
                integration_id,

            "action":
                action,

            "status":
                "success",

            "payload":
                payload
        }

        self.execution_log.append(
            result
        )

        return result

    # -----------------------------------
    # FETCH LOGS
    # -----------------------------------

    def get_logs(self):

        return self.execution_log

