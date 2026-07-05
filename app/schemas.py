from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TextEntryRequest(BaseModel):
    text: str
    meal_type: str = "snack"

class BarcodeRequest(BaseModel):
    barcode: str
    grams: float = 100
    meal_type: str = "snack"

class ManualEntryRequest(BaseModel):
    name: str
    grams: float
    kcal: float
    protein: float = 0
    fat: float = 0
    carbs: float = 0
    meal_type: str = "snack"

class UpdateEntryRequest(BaseModel):
    name: Optional[str] = None
    grams: Optional[float] = None
    kcal: Optional[float] = None
    protein: Optional[float] = None
    fat: Optional[float] = None
    carbs: Optional[float] = None
    meal_type: Optional[str] = None

class FoodEntryResponse(BaseModel):
    id: int
    name: str
    grams: float
    kcal: float
    protein: float
    fat: float
    carbs: float
    meal_type: str
    source: str
    created_at: datetime

    class Config:
        from_attributes = True