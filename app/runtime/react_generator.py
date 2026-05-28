
def generate_react_pages(
    ui_schema
):

    pages = []

    for page in ui_schema.pages:

        component_name = (
            page.name
            .replace(" ", "")
        )

        lines = []

        lines.append(
            "import React from 'react';"
        )

        lines.append("")

        lines.append(
            f"export default function "
            f"{component_name}() {{"
        )

        lines.append(
            "    return ("
        )

        lines.append(
            "        <div>"
        )

        lines.append(
            f"            <h1>{page.name}</h1>"
        )

        for component in page.components:

            lines.append(
                f"            <div>"
                f"{component.type}: "
                f"{component.name}"
                f"</div>"
            )

        lines.append(
            "        </div>"
        )

        lines.append(
            "    );"
        )

        lines.append("}")

        pages.append({

            "page": page.name,

            "code": "\n".join(lines)
        })

    return pages

