from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class IngredientCreate(BaseModel):
    ingredient_name: str
    quantity: Optional[float] = None
    unit: Optional[str] = None
    expiry_date: Optional[datetime] = None


class IngredientResponse(BaseModel):
    id: int
    ingredient_name: str
    quantity: Optional[float]
    unit: Optional[str]
    expiry_date: Optional[datetime]
    added_at: datetime

    class Config:
        from_attributes = True


class IngredientBulkCreate(BaseModel):
    ingredients: List[str]


class RecipeIngredientResponse(BaseModel):
    ingredient_name: str
    quantity: Optional[str]
    is_optional: bool
    is_missing: bool

    class Config:
        from_attributes = True


class RecipeResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    instructions: Optional[str]
    prep_time: Optional[int]
    cook_time: Optional[int]
    difficulty: Optional[str]
    servings: Optional[int]
    calories_estimate: Optional[int]
    recipe_ingredients: List[RecipeIngredientResponse] = []

    class Config:
        from_attributes = True


class RecipeRequest(BaseModel):
    ingredients: List[str]
    preferences: Optional[List[str]] = []
    cuisine: Optional[str] = "Türk mutfağı"
    max_time: Optional[int] = None
    servings: Optional[int] = 2


class ChatRequest(BaseModel):
    message: str
    recipe_context: Optional[str] = None


class ChatResponse(BaseModel):
    response: str
    created_at: datetime

    class Config:
        from_attributes = True
