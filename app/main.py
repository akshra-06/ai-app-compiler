from fastapi import FastAPI
from httpcore import request
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from app.pipeline.intent_extractor import extract_intent
from app.pipeline.architecture_generator import (
    generate_architecture_graph
)

from app.pipeline.db_generator import (
    generate_db_schema
)

from app.pipeline.consistency_validator import (
    validate_consistency
)

from app.pipeline.repair_engine import (
    repair_database_schema
)
from app.pipeline.api_generator import (
    generate_api_schema
)

from app.pipeline.api_consistency_validator import (
    validate_api_consistency
)

from app.pipeline.api_repair_engine import (
    repair_api_schema
)

from app.pipeline.ui_generator import (
    generate_ui_schema
)
from app.pipeline.ui_consistency_validator import (
    validate_ui_consistency
)

from app.runtime.sqlalchemy_generator import (
    generate_sqlalchemy_models
)
from app.runtime.fastapi_generator import (
    generate_fastapi_routes
)

from app.runtime.react_generator import (
    generate_react_pages
)


from app.orchestrator.pipeline_orchestrator import (
    PipelineOrchestrator
)

from app.api.integration_api import (
    router as integration_router
)

from app.api.stream_api import router as stream_router



try:

    from app.generated.fastapi_routes import (
        router
    )

except Exception:

    from fastapi import APIRouter

    router = APIRouter()



app = FastAPI()

app.add_middleware( CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"], )

app.include_router(router)
app.include_router(stream_router)
app.include_router(
    integration_router
)
class PromptRequest(BaseModel):
    prompt: str

@app.post("/generate-ir")
@app.post("/compile-app")
def generate_ir(request: PromptRequest):

    try:

        intent = extract_intent(
            request.prompt
        )

        architecture = generate_architecture_graph(
            intent
        )

        db_schema = generate_db_schema(
            architecture
        )

        api_schema = generate_api_schema(
    architecture,
    intent
)
        api_repair_result = repair_api_schema(
    intent,
    architecture,
    db_schema,
    api_schema
)
        ui_schema = generate_ui_schema(
    intent,
    architecture,
    api_repair_result["api_schema"]
)
        ui_consistency_errors = (
    validate_ui_consistency(
        intent,
        api_repair_result["api_schema"],
        ui_schema
    )
)
        
        sqlalchemy_models = (
    generate_sqlalchemy_models(
        db_schema
    )
)
        
        fastapi_routes = (
    generate_fastapi_routes(
        api_repair_result["api_schema"]
    )
)
        react_pages = generate_react_pages(
    ui_schema
)
        consistency_errors = (
            validate_consistency(
                architecture,
                db_schema
            )
        )
        repair_result = repair_database_schema(
                        architecture,
                        db_schema
)
        return {
    "intent": intent,
    "architecture": architecture,
    "database_schema": repair_result[
        "database_schema"
    ],
    "api_schema": api_schema,
    "repair_success": repair_result[
        "repaired"
    ],
    "consistency_errors": repair_result[
        "errors"
    ],
    "api_schema":
    api_repair_result["api_schema"],

"api_repair_success":
    api_repair_result["repaired"],

"api_consistency_errors":
    api_repair_result["errors"],
    "ui_schema": ui_schema,

    "ui_consistency_errors":
    ui_consistency_errors,

    "sqlalchemy_models":
    sqlalchemy_models,

    "fastapi_routes":
    fastapi_routes,

    "react_pages":
    react_pages,

}
    

    except Exception as e:

        return {
            "status": "error",
            "message": str(e)
        }
    


class OrchestrateRequest(BaseModel):
    prompt: str


@app.post("/orchestrate")
async def orchestrate_pipeline(
    request: OrchestrateRequest
):

    orchestrator = (
        PipelineOrchestrator()
    )

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

    # -----------------------------------
    # SAMPLE DATA
    # -----------------------------------

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
    intent = extract_intent(
    request.prompt
)

    result = await (
        orchestrator.execute_pipeline(

            intent,

            schema,

            broken_app_spec
        )
    )

    return result


@app.post("/orchestrate-real")
async def orchestrate_real_pipeline(
    request: OrchestrateRequest
):

    try:

        intent = extract_intent(
            request.prompt
        )

        architecture = generate_architecture_graph(
            intent
        )

        db_schema = generate_db_schema(
            architecture
        )

        api_schema = generate_api_schema(
            architecture,
            intent
        )

        api_repair_result = repair_api_schema(
            intent,
            architecture,
            db_schema,
            api_schema
        )

        ui_schema = generate_ui_schema(
            intent,
            architecture,
            api_repair_result["api_schema"]
        )
        sqlalchemy_models = (
    generate_sqlalchemy_models(
        db_schema
    )
)

        fastapi_routes = (
    generate_fastapi_routes(
        api_repair_result["api_schema"]
    )
)

        react_pages = (
    generate_react_pages(
        ui_schema
    )
)

        return {

    "intent":
        intent,

    "architecture":
        architecture,

    "database_schema":
        db_schema,

    "api_schema":
        api_repair_result["api_schema"],

    "ui_schema":
        ui_schema,

    "sqlalchemy_models":
        sqlalchemy_models,

    "fastapi_routes":
        fastapi_routes,

    "react_pages":
        react_pages
}

    except Exception as e:

        return {

            "status":
                "error",

            "message":
                str(e)
        }

