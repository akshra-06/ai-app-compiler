
import time

from app.runtime.plugins.plugin_runtime import (
    PluginRuntime
)


class RetryExecutor:

    def __init__(self):

        self.runtime = PluginRuntime()

        self.retry_logs = []

    # -----------------------------------
    # EXECUTE WITH RETRIES
    # -----------------------------------

    def execute_with_retry(

        self,

        integration_id,

        action,

        payload,

        retries=3,

        backoff=1
    ):

        attempt = 0

        while attempt < retries:

            try:

                result = (
                    self.runtime.execute_action(

                        integration_id=
                            integration_id,

                        action=
                            action,

                        payload=
                            payload
                    )
                )

                self.retry_logs.append({

                    "integration":
                        integration_id,

                    "action":
                        action,

                    "attempt":
                        attempt + 1,

                    "status":
                        "success"
                })

                return result

            except Exception as e:

                self.retry_logs.append({

                    "integration":
                        integration_id,

                    "action":
                        action,

                    "attempt":
                        attempt + 1,

                    "status":
                        "failed",

                    "error":
                        str(e)
                })

                time.sleep(backoff)

                backoff *= 2

                attempt += 1

        raise Exception(

            f"Execution failed after "
            f"{retries} retries"
        )

    # -----------------------------------
    # FETCH RETRY LOGS
    # -----------------------------------

    def get_logs(self):

        return self.retry_logs

