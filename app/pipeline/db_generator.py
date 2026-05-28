import json
import os

from dotenv import load_dotenv
from openai import OpenAI

from app.schemas.db_schema import DatabaseSchema


load_dotenv()


client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)


SYSTEM_PROMPT = """
Generate a database schema.

Return ONLY valid JSON.

Schema:
{
  "tables": [
    {
      "name": "string",
      "columns": [
        {
          "name": "string",
          "type": "string",
          "nullable": false,
          "primary_key": false
        }
      ]
    }
  ]
}
"""


def generate_db_schema(architecture_graph):

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
                "content": str(architecture_graph)
            }
        ]
    )

    content = response.choices[0].message.content.strip()

    if content.startswith("```json"):
        content = content.replace("```json", "")
        content = content.replace("```", "")

    parsed = json.loads(content)

    validated = DatabaseSchema(**parsed)

    return validated