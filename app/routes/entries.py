from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import FoodEntry
from app.schemas import TextEntryRequest, ManualEntryRequest, UpdateEntryRequest
from app.services.openai_service import parse_food_text
from app.services import food_entries_service

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
            meal_type=request.meal_type,
            source="text",
        )
        db.add(entry)
        db.commit()
        db.refresh(entry)
        added.append(entry)

    return added


@router.post("/manual")
def add_manual_entry(request: ManualEntryRequest, db: Session = Depends(get_db)):
    return food_entries_service.add_manual_entry(db, request)


@router.get("/today")
def get_today(db: Session = Depends(get_db)):
    return food_entries_service.get_day(db, date.today())


@router.get("/by-date/{selected_date}")
def get_by_date(selected_date: date, db: Session = Depends(get_db)):
    return food_entries_service.get_day(db, selected_date)


@router.patch("/{entry_id}")
def update_entry(
    entry_id: int,
    request: UpdateEntryRequest,
    db: Session = Depends(get_db),
):
    updated = food_entries_service.edit_entry(db, entry_id, request)

    if not updated:
        return {"ok": False, "message": "Nie znaleziono wpisu"}

    return {"ok": True, "entry": updated}


@router.delete("/{entry_id}")
def delete_entry(entry_id: int, db: Session = Depends(get_db)):
    removed = food_entries_service.remove_entry(db, entry_id)

    if not removed:
        return {"ok": False, "message": "Nie znaleziono wpisu"}

    return {"ok": True, "message": "Usunięto wpis"}