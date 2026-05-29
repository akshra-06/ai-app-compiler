
from app.schemas.data_schema import (
    DataSchema,
    EntitySchema,
    FieldSchema
)

from app.schemas.app_spec import (
    AppSpec,
    PageSpec,
    ApiEndpointSpec,
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

    apiEndpoints=[

        ApiEndpointSpec(

            path="/api/leads",

            method="GET",

            handlerDescription=
                "Fetch leads",

            boundEntity="Lead",

            authRequired=True,

            rateLimited=True
        )
    ],

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

            integrationId="slack",

            triggerEntity="Lead",

            action="send_message"
        )
    ],

    workflowStubs=[

        WorkflowStub(

            name=
                "Notify Slack",

            trigger=WorkflowTrigger(

                entity="Lead",

                event="created"
            ),

            integration="slack",

            action="send_message",

            payload={
                "message":
                    "Lead created"
            }
        )
    ]
)


errors = validate_appspec(
    schema,
    app_spec
)

print("\nVALIDATION ERRORS\n")

print(errors)

if not errors:

    print(
        "\nALL VALIDATIONS PASSED"
    )

