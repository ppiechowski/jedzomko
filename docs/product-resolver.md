# Product Resolver

Product Resolver odpowiada za znalezienie produktu i danych odżywczych.

## Kolejność źródeł

1. Lokalna baza `products`
2. Open Food Facts
3. OpenAI estimate

## Zasady

- OpenAI jest używane tylko jako fallback.
- Produkty z OpenAI mają:
  - `source = openai_estimate`
  - `verified = false`
  - `confidence = 0.60`
- Produkty z Open Food Facts mają:
  - `source = open_food_facts`
  - `verified = true`
  - `confidence = 1.00`
- Produkty ręczne mają:
  - `source = manual`
  - `verified = true`
  - `confidence = 0.95`

## Docelowy flow

Użytkownik wpisuje:

`200 g skyru`

AI rozpoznaje:

```json
{
  "intent": "add_food",
  "foods": [
    {
      "name": "skyr",
      "grams": 200
    }
  ]
}