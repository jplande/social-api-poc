from fastapi import APIRouter, HTTPException, status
from app.schemas.auth import (
    UserRegisterRequest, 
    UserLoginRequest, 
    TokenResponse, 
    UserResponse
)
from app.repositories.user_repository import user_repository
from app.utils.security import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(request: UserRegisterRequest):
    """Inscription d'un nouvel utilisateur"""
    
    # Vérifier si l'email existe déjà
    if user_repository.email_exists(request.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Créer l'utilisateur avec mot de passe hashé
    hashed_pwd = hash_password(request.password)
    user = user_repository.create(
        username=request.username,
        email=request.email,
        hashed_password=hashed_pwd
    )
    
    return UserResponse(
        id=user.id,
        username=user.username,
        email=user.email
    )

@router.post("/login", response_model=TokenResponse)
def login(request: UserLoginRequest):
    """Connexion et génération du JWT token"""
    
    # Trouver l'utilisateur
    user = user_repository.find_by_email(request.email)
    
    # Vérifier les credentials
    if not user or not verify_password(request.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    # Générer le JWT
    access_token = create_access_token(data={"sub": user.id})
    
    return TokenResponse(access_token=access_token)
