from typing import Literal

from pydantic import BaseModel, Field


class ParsedFood(BaseModel):
    name: str
    grams: float | None = None
    quantity: float | None = None
    unit: str | None = None


class AIResponse(BaseModel):
    intent: Literal[
        "add_food",
        "delete_food",
        "edit_food",
        "question",
        "unknown",
    ]

    foods: list[ParsedFood] = Field(default_factory=list)