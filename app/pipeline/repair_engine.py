from app.pipeline.db_generator import (
    generate_db_schema
)

from app.pipeline.consistency_validator import (
    validate_consistency
)


def repair_database_schema(
    architecture,
    db_schema,
    max_retries=2
):

    retries = 0

    current_schema = db_schema

    while retries < max_retries:

        errors = validate_consistency(
            architecture,
            current_schema
        )

        if len(errors) == 0:

            return {
                "repaired": True,
                "database_schema": current_schema,
                "errors": []
            }

        current_schema = generate_db_schema(
            architecture
        )

        retries += 1

    return {
        "repaired": False,
        "database_schema": current_schema,
        "errors": errors
    }