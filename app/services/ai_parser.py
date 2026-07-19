import json
from pathlib import Path

from openai import OpenAI
from pydantic import ValidationError

from app.config import settings
from app.ai_schemas import AIResponse


PROMPT_PATH = Path(__file__).parent.parent / "prompts" / "food_parser.txt"

client = OpenAI(api_key=settings.openai_api_key)


def build_prompt(user_message: str) -> str:
    system_prompt = PROMPT_PATH.read_text(encoding="utf-8")

    return f"""{system_prompt}

Wiadomość użytkownika:

{user_message}
"""


def clean_json_output(raw_output: str) -> str:
    cleaned = raw_output.strip()

    if cleaned.startswith("```json"):
        cleaned = cleaned.removeprefix("```json").strip()
    elif cleaned.startswith("```"):
        cleaned = cleaned.removeprefix("```").strip()

    if cleaned.endswith("```"):
        cleaned = cleaned.removesuffix("```").strip()

    return cleaned


def parse_message(user_message: str) -> AIResponse:
    prompt = build_prompt(user_message)

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt,
    )

    raw_output = clean_json_output(response.output_text)

    try:
        parsed_json = json.loads(raw_output)
        return AIResponse.model_validate(parsed_json)

    except json.JSONDecodeError as exc:
        raise ValueError(
            f"OpenAI zwróciło niepoprawny JSON: {raw_output}"
        ) from exc

    except ValidationError as exc:
        raise ValueError(
            f"Odpowiedź OpenAI nie pasuje do schematu AIResponse: {raw_output}"
        ) from exc