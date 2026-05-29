
from app.config.model_routing import (
    MODEL_ROUTING
)

from app.config.cost_table import (
    COST_TABLE
)


def get_stage_model(
    stage_name: str
):

    if (
        stage_name
        not in MODEL_ROUTING
    ):

        raise Exception(
            f"No routing config "
            f"for stage "
            f"'{stage_name}'"
        )

    return MODEL_ROUTING[
        stage_name
    ]


def estimate_cost(
    model_name: str,
    input_tokens: int,
    output_tokens: int
):

    if (
        model_name
        not in COST_TABLE
    ):

        return None

    pricing = COST_TABLE[
        model_name
    ]

    input_cost = (
        input_tokens / 1000
    ) * pricing[
        "input_per_1k"
    ]

    output_cost = (
        output_tokens / 1000
    ) * pricing[
        "output_per_1k"
    ]

    total = (
        input_cost
        + output_cost
    )

    return round(total, 6)

