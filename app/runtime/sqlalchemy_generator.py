
TYPE_MAPPING = {
    "uuid": "String",
    "string": "String",
    "float": "Float",
    "date": "Date",
    "timestamp": "DateTime"
}


def generate_sqlalchemy_models(
    database_schema
):

    output = []

    output.append(
        "from sqlalchemy import *"
    )

    output.append(
        "from sqlalchemy.orm import declarative_base"
    )

    output.append(
        "\nBase = declarative_base()\n"
    )

    for table in database_schema.tables:

        output.append(
            f"class {table.name}(Base):"
        )

        output.append(
            f'    __tablename__ = "{table.name.lower()}s"'
        )

        output.append("")

        for column in table.columns:

            sqlalchemy_type = TYPE_MAPPING.get(
                column.type,
                "String"
            )

            pk = (
                ", primary_key=True"
                if column.primary_key
                else ""
            )

            nullable = (
                ", nullable=True"
                if column.nullable
                else ", nullable=False"
            )

            output.append(
                f"    {column.name} = Column("
                f"{sqlalchemy_type}"
                f"{pk}"
                f"{nullable}"
                f")"
            )

        output.append("\n")

    return "\n".join(output)

