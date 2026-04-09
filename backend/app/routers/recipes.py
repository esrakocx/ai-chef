from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import User, Recipe, RecipeIngredient, Favorite, Ingredient
from app.schemas import RecipeRequest, RecipeResponse
from app.utils.auth_utils import get_current_user
from app.services.gemini_service import generate_recipes

router = APIRouter(prefix="/api/recipes", tags=["Tarifler"])


@router.post("/generate")
def generate_recipe(
    request: RecipeRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = generate_recipes(
        ingredients=request.ingredients,
        preferences=request.preferences,
        cuisine=request.cuisine,
        max_time=request.max_time,
        servings=request.servings,
    )

    saved_recipes = []
    if "recipes" in result:
        for recipe_data in result["recipes"]:
            recipe = Recipe(
                title=recipe_data.get("title", ""),
                description=recipe_data.get("description", ""),
                instructions=recipe_data.get("instructions", ""),
                prep_time=recipe_data.get("prep_time"),
                cook_time=recipe_data.get("cook_time"),
                difficulty=recipe_data.get("difficulty"),
                servings=recipe_data.get("servings"),
                calories_estimate=recipe_data.get("calories_estimate"),
                created_by_ai=True,
            )
            db.add(recipe)
            db.commit()
            db.refresh(recipe)

            for ing in recipe_data.get("ingredients", []):
                ri = RecipeIngredient(
                    recipe_id=recipe.id,
                    ingredient_name=ing.get("name", ""),
                    quantity=ing.get("quantity", ""),
                    is_optional=ing.get("is_optional", False),
                    is_missing=ing.get("is_missing", False),
                )
                db.add(ri)

            db.commit()
            saved_recipes.append(recipe.id)

    result["saved_recipe_ids"] = saved_recipes
    return result


@router.post("/generate-from-pantry")
def generate_from_pantry(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    ingredients = (
        db.query(Ingredient)
        .filter(Ingredient.user_id == current_user.id)
        .all()
    )

    if not ingredients:
        raise HTTPException(
            status_code=400, detail="Önce malzeme eklemelisiniz"
        )

    ingredient_names = [i.ingredient_name for i in ingredients]
    result = generate_recipes(ingredients=ingredient_names)
    return result


@router.get("/{recipe_id}", response_model=RecipeResponse)
def get_recipe(recipe_id: int, db: Session = Depends(get_db)):
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Tarif bulunamadı")
    return recipe


@router.post("/{recipe_id}/favorite")
def toggle_favorite(
    recipe_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    existing = (
        db.query(Favorite)
        .filter(
            Favorite.user_id == current_user.id,
            Favorite.recipe_id == recipe_id,
        )
        .first()
    )

    if existing:
        db.delete(existing)
        db.commit()
        return {"message": "Favorilerden çıkarıldı", "is_favorite": False}
    else:
        fav = Favorite(user_id=current_user.id, recipe_id=recipe_id)
        db.add(fav)
        db.commit()
        return {"message": "Favorilere eklendi", "is_favorite": True}


@router.get("/favorites/list", response_model=List[RecipeResponse])
def get_favorites(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    favorites = (
        db.query(Recipe)
        .join(Favorite)
        .filter(Favorite.user_id == current_user.id)
        .all()
    )
    return favorites
