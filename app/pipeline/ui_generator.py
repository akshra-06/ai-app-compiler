import json
import os

from dotenv import load_dotenv
from openai import OpenAI

from app.schemas.ui_schema import UISchema


load_dotenv()


client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)


SYSTEM_PROMPT = """
You are a senior frontend architect.

Generate a UI schema.

Rules:
- Create pages for all entities
- Create tables for list pages
- Create forms for create/update flows
- Add dashboard page if analytics exist
- Respect role access
- Return ONLY valid JSON

Schema:
{
  "pages": [
    {
      "name": "string",
      "route": "string",
      "roles": ["string"],
      "components": [
        {
          "type": "table|form|chart|navbar",
          "name": "string"
        }
      ]
    }
  ]
}
"""


def generate_ui_schema(
    intent,
    architecture,
    api_schema
):

    response = client.chat.completions.create(
        model="openai/gpt-3.5-turbo",
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content":
                    f"Intent: {intent}\n"
                    f"Architecture: {architecture}\n"
                    f"APIs: {api_schema}"
            }
        ]
    )

    content = (
        response
        .choices[0]
        .message
        .content
        .strip()
    )

    if content.startswith("```json"):

        content = content.replace(
            "```json",
            ""
        )

        content = content.replace(
            "```",
            ""
        )

    parsed = json.loads(content)

    validated = UISchema(**parsed)

    return validated