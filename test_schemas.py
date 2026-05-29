
from app.schemas.app_intent import AppIntent

from app.schemas.data_schema import (
    DataSchema,
    EntitySchema,
    FieldSchema,
    RelationSchema
)

from app.schemas.workflow_schema import (
    WorkflowStub,
    WorkflowTrigger
)

from app.schemas.app_spec import (
    AppSpec,
    PageSpec,
    ApiEndpointSpec,
    RoleSpec,
    PermissionRule,
    IntegrationHook
)


# -----------------------------------
# TEST APP INTENT
# -----------------------------------

intent = AppIntent(

    appName="CRM",

    appType="crm",

    features=[
        "analytics",
        "subscriptions"
    ],

    entities=[
        "Lead",
        "Deal"
    ],

    integrations_requested=[
        "slack",
        "whatsapp"
    ],

    assumptions=[
        "Single tenant app"
    ]
)

print("\nAPP INTENT")
print(intent.model_dump())


# -----------------------------------
# TEST DATA SCHEMA
# -----------------------------------

lead_entity = EntitySchema(

    name="Lead",

    tableName="leads",

    fields=[

        FieldSchema(
            name="id",
            type="uuid",
            isPrimary=True
        ),

        FieldSchema(
            name="tenantId",
            type="uuid"
        ),

        FieldSchema(
            name="email",
            type="string",
            isUnique=True
        )
    ],

    relations=[

        RelationSchema(
            type="hasMany",
            target="Deal",
            foreignKey="lead_id",
            onDelete="cascade"
        )
    ]
)

schema = DataSchema(
    entities=[lead_entity]
)

print("\nDATA SCHEMA")
print(schema.model_dump())


# -----------------------------------
# TEST APP SPEC
# -----------------------------------

app_spec = AppSpec(

    pages=[

        PageSpec(
            name="Leads",
            route="/leads",
            layout="list",
            boundEntity="Lead",
            components=[
                "table",
                "form"
            ]
        )
    ],

    apiEndpoints=[

        ApiEndpointSpec(
            path="/api/leads",
            method="GET",
            handlerDescription=
                "Fetch all leads",

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
            triggerEntity="Deal",
            action="send_message"
        )
    ],

    workflowStubs=[

        WorkflowStub(

            name=
                "Notify Slack when deal closes",

            trigger=WorkflowTrigger(
                entity="Deal",
                event="status_changed",
                condition="status == closed"
            ),

            integration="slack",

            action="send_message",

            payload={
                "channel": "#sales",
                "message":
                    "Deal closed"
            }
        )
    ]
)

print("\nAPP SPEC")
print(app_spec.model_dump())

print("\nALL SCHEMA TESTS PASSED")

