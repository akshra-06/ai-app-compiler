
from app.schemas.data_schema import (
    DataSchema,
    EntitySchema,
    FieldSchema
)

from app.schemas.app_spec import (
    AppSpec,
    PageSpec,
    RoleSpec,
    PermissionRule,
    IntegrationHook
)

from app.schemas.workflow_schema import (
    WorkflowStub,
    WorkflowTrigger
)

from app.validation.appspec_validator import (
    validate_appspec
)

from app.repair.repair_engine import (
    repair_appspec
)


schema = DataSchema(

    entities=[

        EntitySchema(

            name="Lead",

            tableName="leads",

            fields=[

                FieldSchema(
                    name="id",
                    type="uuid"
                )
            ],

            relations=[]
        )
    ]
)


# -----------------------------------
# INTENTIONALLY BROKEN APPSPEC
# -----------------------------------

app_spec = AppSpec(

    pages=[

        PageSpec(

            name="Leads",

            route="/leads",

            layout="list",

            boundEntity="Lead",

            components=["table"]
        )
    ],

    apiEndpoints=[],

    authRules=[

        RoleSpec(

            role="admin",

            permissions=[

                PermissionRule(

                    entity="Lead",

                    read=True,

                    write=True,

                    delete=True
                )
            ]
        )
    ],

    integrationHooks=[

        IntegrationHook(

            integrationId="fake_slack",

            triggerEntity="Lead",

            action="send_message"
        )
    ],

    workflowStubs=[

        WorkflowStub(

            name="Broken Workflow",

            trigger=WorkflowTrigger(

                entity="UnknownEntity",

                event="created"
            ),

            integration="slack",

            action="invalid_action",

            payload={}
        )
    ]
)


# -----------------------------------
# VALIDATE
# -----------------------------------

errors = validate_appspec(
    schema,
    app_spec
)

print("\nVALIDATION ERRORS\n")

for error in errors:

    print(error)


# -----------------------------------
# REPAIR
# -----------------------------------

repair_result = repair_appspec(
    schema,
    app_spec,
    errors
)

print("\nREPAIR LOG\n")

for repair in (
    repair_result["repair_log"]
):

    print(repair)


print("\nREPAIRED SPEC\n")

print(
    repair_result[
        "repaired_spec"
    ]
)

