
from app.runtime.plugins.plugin_runtime import (
    PluginRuntime
)


runtime = PluginRuntime()


# -----------------------------------
# SLACK EXECUTION
# -----------------------------------

result_1 = runtime.execute_action(

    integration_id="slack",

    action="send_message",

    payload={

        "channel":
            "#sales",

        "message":
            "New lead created"
    }
)

print("\nSLACK RESULT\n")

print(result_1)


# -----------------------------------
# WEBHOOK EXECUTION
# -----------------------------------

result_2 = runtime.execute_action(

    integration_id="webhook",

    action="post_payload",

    payload={

        "lead_id":
            101,

        "status":
            "created"
    }
)

print("\nWEBHOOK RESULT\n")

print(result_2)


# -----------------------------------
# EXECUTION LOGS
# -----------------------------------

print("\nEXECUTION LOGS\n")

print(runtime.get_logs())

