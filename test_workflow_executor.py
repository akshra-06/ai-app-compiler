
from app.runtime.workflow_executor import (
    WorkflowExecutor
)


executor = WorkflowExecutor()


workflow_steps = [

    {

        "integration":
            "slack",

        "action":
            "send_message",

        "payload": {

            "channel":
                "#sales",

            "message":
                "Lead created"
        }
    },

    {

        "integration":
            "gmail",

        "action":
            "send_email",

        "payload": {

            "to":
                "admin@test.com",

            "subject":
                "New Lead",

            "body":
                "A new lead was created"
        }
    },

    {

        "integration":
            "webhook",

        "action":
            "post_payload",

        "payload": {

            "lead_id":
                101
        }
    }
]


result = executor.execute_workflow(

    workflow_name=
        "Lead Notification Workflow",

    steps=workflow_steps
)

print("\nWORKFLOW RESULT\n")

print(result)


print("\nWORKFLOW LOGS\n")

print(
    executor.get_logs()
)

