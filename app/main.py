from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, posts

app = FastAPI(
    title="Social API POC",
    version="1.0.0",
    description="API REST pour réseau social - POC 3 jours",
    # Ajout pour supporter le Gateway Gravitee
    root_path="/social-api",
    servers=[
        {"url": "http://localhost:8000", "description": "Direct"},
        {"url": "http://localhost:8082/social-api", "description": "Via Gravitee Gateway"}
    ]
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(auth.router)
app.include_router(posts.router)

@app.get("/")
def root():
    return {
        "message": "Social API POC",
        "status": "running",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}