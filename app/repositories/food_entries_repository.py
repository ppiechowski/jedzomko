from datetime import datetime, date, time
from sqlalchemy.orm import Session

from app.models import FoodEntry


def create_entry(db: Session, entry: FoodEntry) -> FoodEntry:
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


def get_entry_by_id(db: Session, entry_id: int) -> FoodEntry | None:
    return db.query(FoodEntry).filter(FoodEntry.id == entry_id).first()


def get_entries_for_date(db: Session, selected_date: date):
    start = datetime.combine(selected_date, time.min)
    end = datetime.combine(selected_date, time.max)

    return (
        db.query(FoodEntry)
        .filter(FoodEntry.created_at >= start)
        .filter(FoodEntry.created_at <= end)
        .order_by(FoodEntry.created_at.desc())
        .all()
    )


def delete_entry(db: Session, entry: FoodEntry) -> None:
    db.delete(entry)
    db.commit()


def update_entry(db: Session, entry: FoodEntry, data: dict) -> FoodEntry:
    for key, value in data.items():
        if value is not None:
            setattr(entry, key, value)

    db.commit()
    db.refresh(entry)
    return entry