from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime, date, time

from app.database import get_db
from app.models import FoodEntry
from app.schemas import TextEntryRequest
from app.services.openai_service import parse_food_text

router = APIRouter(prefix="/entries", tags=["entries"])

@router.post("/text")
def add_text_entry(request: TextEntryRequest, db: Session = Depends(get_db)):
    parsed = parse_food_text(request.text)
    added = []

    for item in parsed["items"]:
        entry = FoodEntry(
            name=item["name"],
            grams=item["grams"],
            kcal=item["kcal"],
            protein=item["protein"],
            fat=item["fat"],
            carbs=item["carbs"],
            source="text"
        )
        db.add(entry)
        db.commit()
        db.refresh(entry)
        added.append(entry)

    return added

@router.get("/today")
def get_today(db: Session = Depends(get_db)):
    start = datetime.combine(date.today(), time.min)
    end = datetime.combine(date.today(), time.max)

    entries = db.query(FoodEntry).filter(
        FoodEntry.created_at >= start,
        FoodEntry.created_at <= end
    ).order_by(FoodEntry.created_at.desc()).all()

    totals = {
        "kcal": sum(e.kcal for e in entries),
        "protein": sum(e.protein for e in entries),
        "fat": sum(e.fat for e in entries),
        "carbs": sum(e.carbs for e in entries),
    }

    return {
        "entries": entries,
        "totals": totals
    }

@router.delete("/{entry_id}")
def delete_entry(entry_id: int, db: Session = Depends(get_db)):
    entry = db.query(FoodEntry).filter(FoodEntry.id == entry_id).first()

    if not entry:
        return {"ok": False, "message": "Nie znaleziono wpisu"}

    db.delete(entry)
    db.commit()

    return {"ok": True, "message": "Usunięto wpis"}