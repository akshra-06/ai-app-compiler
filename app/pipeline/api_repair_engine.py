
from copy import deepcopy

from app.schemas.api_schema import Endpoint

from app.pipeline.api_consistency_validator import (
    validate_api_consistency
)


CRUD_METHODS = [
    "GET",
    "POST",
    "PUT",
    "DELETE"
]


def build_missing_endpoint(
    entity,
    method
):

    entity_lower = entity.lower()

    path = f"/{entity_lower}s"

    if method in ["GET", "PUT", "DELETE"]:

        path += "/{id}"

    return Endpoint(
        path=path,
        method=method,
        entity=entity,
        auth_required=True,
        roles=["admin"]
    )


def build_analytics_endpoint(): 
    return Endpoint( path="/analytics", method="GET", entity="Analytics", endpoint_type="service", auth_required=True, roles=["admin"] )


def repair_api_schema(
    intent,
    architecture,
    database_schema,
    api_schema
):

    current_schema = deepcopy(api_schema)

    errors = validate_api_consistency(
        intent,
        architecture,
        database_schema,
        current_schema
    )

    # -----------------------------------
    # TARGETED CRUD REPAIR
    # -----------------------------------

    for error in errors:

        if "missing CRUD methods" in error:

            entity = error.split(
                " missing CRUD methods"
            )[0]

            missing_part = error.split(": ")[1]

            missing_methods = eval(
                missing_part
            )

            for method in missing_methods:

                endpoint = build_missing_endpoint(
                    entity,
                    method
                )

                current_schema.endpoints.append(
                    endpoint
                )

    # -----------------------------------
    # ANALYTICS API REPAIR
    # -----------------------------------

    analytics_exists = any(
        endpoint.path == "/analytics"
        for endpoint in current_schema.endpoints
    )

    if (
        "analytics dashboard"
        in intent.features
        and not analytics_exists
    ):

        current_schema.endpoints.append(
            build_analytics_endpoint()
        )

    # -----------------------------------
    # REVALIDATE
    # -----------------------------------

    final_errors = validate_api_consistency(
        intent,
        architecture,
        database_schema,
        current_schema
    )

    return {
        "repaired":
            len(final_errors) == 0,

        "api_schema":
            current_schema,

        "errors":
            final_errors
    }

