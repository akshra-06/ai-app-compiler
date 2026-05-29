
from app.integrations.registry import (
    INTEGRATION_REGISTRY
)


print("\nREGISTERED INTEGRATIONS\n")

for integration_id, integration in (
    INTEGRATION_REGISTRY.items()
):

    print(
        f"{integration_id}"
    )

    print(
        f"Auth Type: {integration.authType}"
    )

    print("Actions:")

    for action in integration.actions:

        print(
            f" - {action.id}"
        )

    print("-" * 40)

