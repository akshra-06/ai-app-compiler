
import asyncio

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

from app.orchestrator.pipeline_orchestrator import (
    PipelineOrchestrator
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


broken_app_spec = AppSpec(

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


intent = {

    "app_name":
        "CRM"
}


async def run():

    orchestrator = (
        PipelineOrchestrator()
    )

    result = await (
        orchestrator.execute_pipeline(

            intent,

            schema,

            broken_app_spec
        )
    )

    print("\nPIPELINE RESULT\n")

    print(result)


asyncio.run(run())

