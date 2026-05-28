import json
import os

from dotenv import load_dotenv
from openai import OpenAI

from app.schemas.intent_schema import IntentIR


load_dotenv()


client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)


SYSTEM_PROMPT = """
You are an intent extraction engine.

Return ONLY valid JSON.

Schema:
{
  "app_name": "string",
  "features": ["string"],
  "roles": ["string"],
  "entities": ["string"]
}
"""


def extract_intent(user_prompt: str):

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
                "content": user_prompt
            }
        ]
    )

    content = response.choices[0].message.content

    parsed_json = json.loads(content)

    validated = IntentIR(**parsed_json)

    return validated