
def validate_api_consistency(
    intent,
    architecture,
    database_schema,
    api_schema
):

    errors = []

    # -----------------------------------
    # VALID ROLE SET
    # -----------------------------------

    valid_roles = set(intent.roles)

    # -----------------------------------
    # VALID ENTITIES
    # -----------------------------------

    valid_entities = {
        entity.name
        for entity in architecture.entities
    }

    db_tables = {
        table.name
        for table in database_schema.tables
    }

    # -----------------------------------
    # CRUD TRACKER
    # -----------------------------------

    crud_tracker = {}

    for entity in valid_entities:

        crud_tracker[entity] = set()

    # -----------------------------------
    # API VALIDATION
    # -----------------------------------

    for endpoint in api_schema.endpoints:

        entity = endpoint.entity

        # -------------------------
        # RESOURCE VALIDATION
        # -------------------------

        if endpoint.endpoint_type == "resource":

            if entity not in valid_entities:

                errors.append(
                    f"API references unknown entity: {entity}"
                )

            if entity not in db_tables:

                errors.append(
                    f"No DB table for API entity: {entity}"
                )

        # -------------------------
        # ROLE VALIDATION
        # -------------------------

        for role in endpoint.roles:

            if role not in valid_roles:

                errors.append(
                    f"Invalid role '{role}' "
                    f"in endpoint {endpoint.path}"
                )

        # -------------------------
        # CRUD TRACKING
        # -------------------------

        if (
            endpoint.endpoint_type == "resource"
            and endpoint.path != "/login"
        ):

            crud_tracker[entity].add(
                endpoint.method
            )

        # -------------------------
        # LOGIN VALIDATION
        # -------------------------

        if endpoint.path == "/login":

            if endpoint.auth_required:

                errors.append(
                    "/login cannot require auth"
                )

    # -----------------------------------
    # CRUD COMPLETENESS
    # -----------------------------------

    required_methods = {
        "GET",
        "POST",
        "PUT",
        "DELETE"
    }

    for entity, methods in crud_tracker.items():

        missing_methods = list(
            required_methods - methods
        )

        if missing_methods:

            errors.append(
                f"{entity} missing CRUD methods: "
                f"{missing_methods}"
            )

    return errors

