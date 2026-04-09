import httpx
import json
import re
from typing import List, Optional
from app.config import get_settings

settings = get_settings()

API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL_NAME = "google/gemini-2.0-flash-001"


def _call_ai(prompt: str) -> str:
    headers = {
        "Authorization": f"Bearer {settings.openrouter_api_key}",
        "Content-Type": "application/json",
    }
    data = {
        "model": MODEL_NAME,
        "messages": [{"role": "user", "content": prompt}],
    }
    response = httpx.post(API_URL, headers=headers, json=data, timeout=60)
    response.raise_for_status()
    result = response.json()
    return result["choices"][0]["message"]["content"]


def generate_recipes(
    ingredients: List[str],
    preferences: List[str] = [],
    cuisine: str = "Türk mutfağı",
    max_time: Optional[int] = None,
    servings: int = 2,
) -> dict:
    ingredients_text = ", ".join(ingredients)
    preferences_text = ", ".join(preferences) if preferences else "yok"
    time_text = f"maksimum {max_time} dakika" if max_time else "süre sınırı yok"

    prompt = f"""Sen profesyonel bir aşçı ve yemek danışmanısın.

Kullanıcının elindeki malzemeler: {ingredients_text}
Tercihler: {preferences_text}
Mutfak türü: {cuisine}
Süre kısıtı: {time_text}
Porsiyon sayısı: {servings}

Bu malzemelerle yapılabilecek TAM OLARAK 3 tarif öner.

Kurallar:
1. Sadece verilen malzemeleri kullan
2. Tuz, biber, yağ, su zaten var
3. Eksik malzemeleri belirt
4. Kolaydan zora sırala

SADECE JSON formatında yanıt ver:

{{
    "recipes": [
        {{
            "title": "Tarif Adı",
            "description": "Kısa açıklama",
            "prep_time": 10,
            "cook_time": 15,
            "difficulty": "Kolay",
            "servings": {servings},
            "calories_estimate": 350,
            "ingredients": [
                {{"name": "malzeme", "quantity": "miktar", "is_optional": false, "is_missing": false}}
            ],
            "instructions": "Adım 1: ...\\nAdım 2: ...",
            "tips": "Püf noktası"
        }}
    ],
    "general_tips": "Genel öneri",
    "waste_warning": "Bozulma uyarısı"
}}"""

    try:
        text = _call_ai(prompt)
        text = re.sub(r'```json\s*', '', text)
        text = re.sub(r'```\s*', '', text)
        text = text.strip()
        return json.loads(text)
    except Exception as e:
        print(f"AI Hatası: {e}")
        return {
            "recipes": [],
            "general_tips": f"Hata: {str(e)}",
            "waste_warning": "",
        }


def chat_with_chef(
    message: str,
    recipe_context: Optional[str] = None,
    chat_history: List[dict] = [],
) -> str:
    context = ""
    if recipe_context:
        context = f"\nAktif tarif: {recipe_context}\n"

    history_text = ""
    for h in chat_history[-5:]:
        history_text += f"Kullanıcı: {h['prompt']}\nAsistan: {h['response']}\n"

    prompt = f"""Sen "AI Chef" adında samimi bir mutfak asistanısın. Türkçe konuş.
{context}
Önceki konuşma:
{history_text}
Kullanıcının mesajı: {message}"""

    try:
        return _call_ai(prompt)
    except Exception as e:
        return "Üzgünüm, şu anda yanıt veremedim. Tekrar dene."


def analyze_expiry_priority(ingredients: List[dict]) -> str:
    ingredients_text = json.dumps(ingredients, ensure_ascii=False)
    prompt = f"""Bu malzemelerin hangisi önce kullanılmalı? Bozulma sırasına göre sırala.
Malzemeler: {ingredients_text}
Kısa ve net Türkçe yanıt ver."""

    try:
        return _call_ai(prompt)
    except Exception as e:
        return f"Analiz yapılamadı: {str(e)}"
