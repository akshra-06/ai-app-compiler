
from app.clarification.clarification_engine import (
    run_clarification_pipeline
)


intent = {

    "app_name":
        "CRM System"
}


result = run_clarification_pipeline(
    intent
)

print("\nCLARIFICATION RESULT\n")

print(result)

