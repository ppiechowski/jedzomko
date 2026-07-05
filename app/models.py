from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from datetime import datetime
from app.database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)

    barcode = Column(String, nullable=True, unique=True, index=True)
    name = Column(String, nullable=False, index=True)
    brand = Column(String, nullable=True)

    kcal_100g = Column(Float, nullable=False, default=0)
    protein_100g = Column(Float, nullable=False, default=0)
    fat_100g = Column(Float, nullable=False, default=0)
    carbs_100g = Column(Float, nullable=False, default=0)

    source = Column(String, nullable=False, default="manual")
    verified = Column(Boolean, nullable=False, default=False)
    confidence = Column(Float, nullable=False, default=0.0)

    created_at = Column(DateTime, default=datetime.utcnow)

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