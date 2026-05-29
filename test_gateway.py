
from app.gateway.model_gateway import (
    get_stage_model,
    estimate_cost
)


intent_model = get_stage_model(
    "intent_extraction"
)

print("\nINTENT MODEL\n")

print(intent_model)


cost = estimate_cost(

    model_name="gpt-4o-mini",

    input_tokens=1000,

    output_tokens=500
)

print("\nESTIMATED COST\n")

print(cost)

