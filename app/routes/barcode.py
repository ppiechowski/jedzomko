from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import FoodEntry
from app.schemas import BarcodeRequest
from app.services import products_service
from app.repositories import food_entries_repository

router = APIRouter(prefix="/barcode", tags=["barcode"])


@router.post("/add")
def add_barcode_entry(request: BarcodeRequest, db: Session = Depends(get_db)):
    product = products_service.get_or_create_by_barcode(db, request.barcode)

    if product is None:
        return {
            "ok": False,
            "message": f"Brak produktu w bazie: {request.barcode}"
        }

    macros = products_service.calculate_entry_macros(product, request.grams)

    entry = FoodEntry(
        name=macros["name"],
        grams=macros["grams"],
        kcal=macros["kcal"],
        protein=macros["protein"],
        fat=macros["fat"],
        carbs=macros["carbs"],
        meal_type=request.meal_type,
        source="barcode",
    )

    entry = food_entries_repository.create_entry(db, entry)

    return {
        "ok": True,
        "entry": entry,
        "product": {
            "id": product.id,
            "name": product.name,
            "brand": product.brand,
            "source": product.source,
            "verified": product.verified,
            "confidence": product.confidence,
        }
    }