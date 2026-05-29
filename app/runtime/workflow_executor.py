
from app.runtime.plugins.plugin_runtime import (
    PluginRuntime
)


class WorkflowExecutor:

    def __init__(self):

        self.runtime = PluginRuntime()

        self.workflow_log = []

    # -----------------------------------
    # EXECUTE WORKFLOW
    # -----------------------------------

    def execute_workflow(

        self,

        workflow_name,

        steps
    ):

        results = []

        for step in steps:

            try:

                result = (
                    self.runtime.execute_action(

                        integration_id=
                            step[
                                "integration"
                            ],

                        action=
                            step[
                                "action"
                            ],

                        payload=
                            step[
                                "payload"
                            ]
                    )
                )

                results.append({

                    "step":
                        step,

                    "status":
                        "success",

                    "result":
                        result
                })

            except Exception as e:

                results.append({

                    "step":
                        step,

                    "status":
                        "failed",

                    "error":
                        str(e)
                })

                break

        workflow_result = {

            "workflow":
                workflow_name,

            "results":
                results
        }

        self.workflow_log.append(
            workflow_result
        )

        return workflow_result

    # -----------------------------------
    # FETCH LOGS
    # -----------------------------------

    def get_logs(self):

        return self.workflow_log

