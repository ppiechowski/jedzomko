import json
from openai import OpenAI
from app.config import settings

client = OpenAI(api_key=settings.openai_api_key)

def parse_food_text(text: str):
    prompt = f"""
Zamień tekst użytkownika na listę produktów spożywczych.
Zwróć WYŁĄCZNIE poprawny JSON, bez komentarzy.

Tekst użytkownika:
{text}

Format:
{{
  "items": [
    {{
      "name": "nazwa produktu",
      "grams": 100,
      "kcal": 120,
      "protein": 10,
      "fat": 2,
      "carbs": 15
    }}
  ]
}}
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )

    return json.loads(response.output_text)