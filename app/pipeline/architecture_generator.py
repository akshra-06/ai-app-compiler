import json

from app.schemas.architecture_schema import (
    ArchitectureGraph
)

from openai import OpenAI
import os
from dotenv import load_dotenv
def validate_architecture(parsed):

    for entity in parsed["entities"]:

        if len(entity["fields"]) == 0:

            raise Exception(
                f"Entity {entity['name']} has no fields"
            )

load_dotenv()


client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)


SYSTEM_PROMPT = """
You are a senior software architect.

Generate a COMPLETE architecture graph.

Rules:
- Every entity MUST contain realistic fields
- Include IDs and timestamps
- Add foreign keys when relationships exist
- Infer fields from business context
- Never return empty arrays
- Return ONLY valid JSON

Schema:
{
  "entities": [
    {
      "name": "string",
      "fields": [
        {
          "name": "string",
          "type": "string"
        }
      ]
    }
  ],
  "relationships": [
    {
      "from_entity": "string",
      "to_entity": "string",
      "relation_type": "string"
    }
  ]
}

Example:
{
  "entities": [
    {
      "name": "User",
      "fields": [
        {
          "name": "id",
          "type": "uuid"
        },
        {
          "name": "email",
          "type": "string"
        },
        {
          "name": "password_hash",
          "type": "string"
        },
        {
          "name": "role",
          "type": "string"
        }
      ]
    }
  ],
  "relationships": []
}
"""

def generate_architecture_graph(intent_ir):

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
                "content": str(intent_ir)
            }
        ]
    )

    content = response.choices[0].message.content.strip()

    if content.startswith("```json"):
        content = content.replace("```json", "")
        content = content.replace("```", "")

    parsed = json.loads(content)
    validate_architecture(parsed)
    validated = ArchitectureGraph(**parsed)

    return validated