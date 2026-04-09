from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import auth, ingredients, recipes, chat

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Chef - Evde Ne Var?",
    description="Evindeki malzemelere göre AI destekli tarif önerisi al",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(ingredients.router)
app.include_router(recipes.router)
app.include_router(chat.router)


@app.get("/")
def root():
    return {
        "message": "AI Chef API hoş geldiniz!",
        "docs": "/docs",
        "version": "1.0.0",
    }


@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "AI Chef"}
