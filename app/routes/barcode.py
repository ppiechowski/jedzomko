from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import FoodEntry
from app.schemas import BarcodeRequest
from app.services.barcode_service import lookup_barcode

router = APIRouter(prefix="/barcode", tags=["barcode"])

@router.post("/add")
def add_barcode_entry(request: BarcodeRequest, db: Session = Depends(get_db)):
    product = lookup_barcode(request.barcode)

    if product is None:
        return {
            "ok": False,
            "message": f"Brak produktu w bazie: {request.barcode}"
        }

    ratio = request.grams / 100

    entry = FoodEntry(
        name=product["name"],
        grams=request.grams,
        kcal=product["kcal_100g"] * ratio,
        protein=product["protein_100g"] * ratio,
        fat=product["fat_100g"] * ratio,
        carbs=product["carbs_100g"] * ratio,
        source="barcode"
    )

    db.add(entry)
    db.commit()
    db.refresh(entry)

    return {
        "ok": True,
        "entry": entry
    }