
from app.runtime.retry_executor import (
    RetryExecutor
)


executor = RetryExecutor()


# -----------------------------------
# SUCCESS CASE
# -----------------------------------

result = executor.execute_with_retry(

    integration_id="slack",

    action="send_message",

    payload={

        "message":
            "Retry test"
    }
)

print("\nSUCCESS RESULT\n")

print(result)


# -----------------------------------
# FAILURE CASE
# -----------------------------------

try:

    executor.execute_with_retry(

        integration_id="slack",

        action="invalid_action",

        payload={},

        retries=3
    )

except Exception as e:

    print("\nFINAL FAILURE\n")

    print(str(e))


# -----------------------------------
# RETRY LOGS
# -----------------------------------

print("\nRETRY LOGS\n")

print(
    executor.get_logs()
)

