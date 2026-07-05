from datetime import date
from sqlalchemy.orm import Session

from app.models import FoodEntry
from app.schemas import ManualEntryRequest, UpdateEntryRequest
from app.repositories import food_entries_repository


def calculate_totals(entries):
    return {
        "kcal": sum(e.kcal for e in entries),
        "protein": sum(e.protein for e in entries),
        "fat": sum(e.fat for e in entries),
        "carbs": sum(e.carbs for e in entries),
    }


def add_manual_entry(db: Session, request: ManualEntryRequest):
    entry = FoodEntry(
        name=request.name,
        grams=request.grams,
        kcal=request.kcal,
        protein=request.protein,
        fat=request.fat,
        carbs=request.carbs,
        meal_type=request.meal_type,
        source="manual",
    )

    return food_entries_repository.create_entry(db, entry)


def get_day(db: Session, selected_date: date):
    entries = food_entries_repository.get_entries_for_date(db, selected_date)

    return {
        "entries": entries,
        "totals": calculate_totals(entries),
    }


def edit_entry(db: Session, entry_id: int, request: UpdateEntryRequest):
    entry = food_entries_repository.get_entry_by_id(db, entry_id)

    if not entry:
        return None

    return food_entries_repository.update_entry(
        db,
        entry,
        request.model_dump(),
    )


def remove_entry(db: Session, entry_id: int):
    entry = food_entries_repository.get_entry_by_id(db, entry_id)

    if not entry:
        return False

    food_entries_repository.delete_entry(db, entry)
    return True