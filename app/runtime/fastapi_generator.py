
def generate_fastapi_routes(
    api_schema
):

    output = []

    output.append(
        "from fastapi import APIRouter"
    )

    output.append(
        "from fastapi import Body"
    )

    output.append(
        "\nrouter = APIRouter()\n"
    )

    for endpoint in api_schema.endpoints:

        method = endpoint.method.lower()

        path = endpoint.path

        function_name = (
            f"{method}_"
            f"{path.strip('/').replace('/', '_').replace('{id}', 'by_id')}"
        )

        output.append(
            f'@router.{method}("{path}")'
        )

        output.append(
            f"def {function_name}("
            f"payload: dict = Body(default={{}})"
            f"):"
        )

        # -----------------------------------
        # LOGIN ENDPOINT
        # -----------------------------------

        if path == "/login":

            output.append(
                '    return {'
                '"message": "Login successful", '
                '"token": "demo-jwt-token"'
                '}'
            )

        else:

            output.append(
                f'    return {{"message": "{endpoint.method} {path}"}}'
            )

        output.append("\n")

    return "\n".join(output)

