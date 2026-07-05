from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from app.database import Base

class FoodEntry(Base):
    __tablename__ = "food_entries"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)
    grams = Column(Float, nullable=False)

    kcal = Column(Float, nullable=False)
    protein = Column(Float, nullable=False, default=0)
    fat = Column(Float, nullable=False, default=0)
    carbs = Column(Float, nullable=False, default=0)

    meal_type = Column(String, nullable=False, default="snack")
    source = Column(String, nullable=False, default="manual")

    created_at = Column(DateTime, default=datetime.utcnow)