from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import User, Ingredient
from app.schemas import IngredientCreate, IngredientResponse, IngredientBulkCreate
from app.utils.auth_utils import get_current_user
from app.services.gemini_service import analyze_expiry_priority

router = APIRouter(prefix="/api/ingredients", tags=["Malzemeler"])


@router.post("/add", response_model=IngredientResponse)
def add_ingredient(
    ingredient: IngredientCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    new_ingredient = Ingredient(
        user_id=current_user.id,
        ingredient_name=ingredient.ingredient_name,
        quantity=ingredient.quantity,
        unit=ingredient.unit,
        expiry_date=ingredient.expiry_date,
    )
    db.add(new_ingredient)
    db.commit()
    db.refresh(new_ingredient)
    return new_ingredient


@router.post("/bulk-add", response_model=List[IngredientResponse])
def bulk_add_ingredients(
    data: IngredientBulkCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    added = []
    for name in data.ingredients:
        name = name.strip()
        if name:
            existing = (
                db.query(Ingredient)
                .filter(
                    Ingredient.user_id == current_user.id,
                    Ingredient.ingredient_name == name,
                )
                .first()
            )
            if not existing:
                new_ing = Ingredient(
                    user_id=current_user.id, ingredient_name=name
                )
                db.add(new_ing)
                db.commit()
                db.refresh(new_ing)
                added.append(new_ing)
    return added


@router.get("/my-ingredients", response_model=List[IngredientResponse])
def get_my_ingredients(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return (
        db.query(Ingredient)
        .filter(Ingredient.user_id == current_user.id)
        .all()
    )


@router.delete("/{ingredient_id}")
def delete_ingredient(
    ingredient_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    ingredient = (
        db.query(Ingredient)
        .filter(
            Ingredient.id == ingredient_id,
            Ingredient.user_id == current_user.id,
        )
        .first()
    )
    if not ingredient:
        raise HTTPException(status_code=404, detail="Malzeme bulunamadı")
    db.delete(ingredient)
    db.commit()
    return {"message": "Malzeme silindi"}


@router.delete("/clear-all/")
def clear_all_ingredients(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db.query(Ingredient).filter(Ingredient.user_id == current_user.id).delete()
    db.commit()
    return {"message": "Tüm malzemeler silindi"}


@router.get("/expiry-analysis")
def get_expiry_analysis(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    ingredients = (
        db.query(Ingredient)
        .filter(Ingredient.user_id == current_user.id)
        .all()
    )
    if not ingredients:
        return {"analysis": "Henüz malzeme eklememişsiniz."}

    ingredient_list = [
        {
            "name": i.ingredient_name,
            "quantity": i.quantity,
            "unit": i.unit,
            "expiry_date": str(i.expiry_date) if i.expiry_date else None,
        }
        for i in ingredients
    ]

    analysis = analyze_expiry_priority(ingredient_list)
    return {"analysis": analysis}
