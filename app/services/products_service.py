import json
from sqlalchemy.orm import Session
from openai import OpenAI

from app.config import settings
from app.models import Product
from app.repositories import products_repository
from app.services.barcode_service import lookup_barcode

client = OpenAI(api_key=settings.openai_api_key)


def estimate_product_with_openai(name: str) -> dict:
    prompt = f"""
Oszacuj typowe wartości odżywcze produktu na 100 g.
Zwróć WYŁĄCZNIE JSON.

Produkt:
{name}

Format:
{{
  "name": "nazwa produktu",
  "brand": null,
  "kcal_100g": 0,
  "protein_100g": 0,
  "fat_100g": 0,
  "carbs_100g": 0
}}
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )

    return json.loads(response.output_text)


def get_or_create_by_barcode(db: Session, barcode: str) -> Product | None:
    existing = products_repository.find_by_barcode(db, barcode)

    if existing:
        return existing

    data = lookup_barcode(barcode)

    if not data:
        return None

    product = Product(
        barcode=barcode,
        name=data["name"],
        brand=data.get("brand"),
        kcal_100g=data["kcal_100g"],
        protein_100g=data["protein_100g"],
        fat_100g=data["fat_100g"],
        carbs_100g=data["carbs_100g"],
        source="open_food_facts",
        verified=True,
        confidence=1.0,
    )

    return products_repository.create_product(db, product)


def get_or_create_by_name(db: Session, name: str) -> Product:
    existing = products_repository.find_by_name(db, name)

    if existing:
        return existing

    data = estimate_product_with_openai(name)

    product = Product(
        barcode=None,
        name=data["name"],
        brand=data.get("brand"),
        kcal_100g=data["kcal_100g"],
        protein_100g=data["protein_100g"],
        fat_100g=data["fat_100g"],
        carbs_100g=data["carbs_100g"],
        source="openai_estimate",
        verified=False,
        confidence=0.6,
    )

    return products_repository.create_product(db, product)


def calculate_entry_macros(product: Product, grams: float) -> dict:
    ratio = grams / 100

    return {
        "name": product.name,
        "grams": grams,
        "kcal": product.kcal_100g * ratio,
        "protein": product.protein_100g * ratio,
        "fat": product.fat_100g * ratio,
        "carbs": product.carbs_100g * ratio,
        "source": product.source,
        "product_id": product.id,
        "verified": product.verified,
        "confidence": product.confidence,
    }