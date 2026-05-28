def validate_consistency(
    architecture,
    database_schema
):

    errors = []

    architecture_entities = {
        entity.name: entity
        for entity in architecture.entities
    }

    database_tables = {
        table.name: table
        for table in database_schema.tables
    }

    # -----------------------------------
    # ENTITY ↔ TABLE VALIDATION
    # -----------------------------------

    for entity_name, entity in architecture_entities.items():

        if entity_name not in database_tables:

            errors.append(
                f"Missing DB table for entity: {entity_name}"
            )

            continue

        table = database_tables[entity_name]

        entity_fields = {
            field.name
            for field in entity.fields
        }

        table_columns = {
            column.name
            for column in table.columns
        }

        # -----------------------------------
        # FIELD ↔ COLUMN VALIDATION
        # -----------------------------------

        missing_columns = (
            entity_fields - table_columns
        )

        extra_columns = (
            table_columns - entity_fields
        )

        if missing_columns:

            errors.append(
                f"{entity_name} missing columns: "
                f"{missing_columns}"
            )

        if extra_columns:

            errors.append(
                f"{entity_name} has extra columns: "
                f"{extra_columns}"
            )

    return errors