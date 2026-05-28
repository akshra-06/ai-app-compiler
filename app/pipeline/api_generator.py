import json
import os

from dotenv import load_dotenv
from openai import OpenAI

from app.schemas.api_schema import APISchema


load_dotenv()


client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)


SYSTEM_PROMPT = """
You are a backend API architect.

Generate REST API endpoints.

Rules:
- Every entity must have CRUD APIs
- Use REST conventions
- Add auth rules
- Include role permissions
- Return ONLY valid JSON

Schema:
{
  "endpoints": [
    {
      "path": "string",
      "method": "GET|POST|PUT|DELETE",
      "entity": "string",
      "auth_required": true,
      "roles": ["string"]
    }
  ]
}
"""


def generate_api_schema(
    architecture_graph,
    intent_ir
):

    response = client.chat.completions.create(
        model="openai/gpt-3.5-turbo",
       max_tokens=1200, temperature=0.2,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content":
                    f"Architecture: {architecture_graph}\n"
                    f"Intent: {intent_ir}"
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

    validated = APISchema(**parsed)

    return validated