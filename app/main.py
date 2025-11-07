from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, posts
from app.database import init_db

app = FastAPI(
    title="Social API POC",
    version="1.0.0",
    description="API REST pour réseau social - POC avec PostgreSQL"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialiser la base de données au démarrage
@app.on_event("startup")
def on_startup():
    """Créer les tables au démarrage si elles n'existent pas"""
    init_db()

# Routes
app.include_router(auth.router)
app.include_router(posts.router)

@app.get("/")
def root():
    return {
        "message": "Social API POC",
        "status": "running",
        "version": "1.0.0",
        "database": "PostgreSQL",
        "docs": "/docs"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "database": "connected"}