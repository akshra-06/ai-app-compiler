
from typing import List


REQUIRED_FIELDS = [

    "app_type",

    "primary_entity",

    "authentication",

    "user_roles"
]


def detect_missing_information(
    intent: dict
):

    missing_fields = []

    for field in REQUIRED_FIELDS:

        if field not in intent:

            missing_fields.append(
                field
            )

    return missing_fields


def generate_questions(
    missing_fields: List[str]
):

    questions = []

    for field in missing_fields:

        if field == "app_type":

            questions.append(
                "What type of application do you want to build?"
            )

        elif field == "primary_entity":

            questions.append(
                "What is the main entity in your system?"
            )

        elif field == "authentication":

            questions.append(
                "Should the system support authentication/login?"
            )

        elif field == "user_roles":

            questions.append(
                "What user roles should exist in the application?"
            )

    return questions


def run_clarification_pipeline(
    intent: dict
):

    missing_fields = (
        detect_missing_information(
            intent
        )
    )

    questions = generate_questions(
        missing_fields
    )

    return {

        "needs_clarification":
            len(missing_fields) > 0,

        "missing_fields":
            missing_fields,

        "questions":
            questions
    }

