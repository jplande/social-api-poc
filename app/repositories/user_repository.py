from typing import Optional
from sqlalchemy.orm import Session
from app.models.db_models import UserDB
from app.models.user import User


class UserRepository:
    """Repository pour gérer les utilisateurs avec PostgreSQL"""

    def __init__(self, db: Session):
        self.db = db

    def create(self, username: str, email: str, hashed_password: str) -> User:
        """Crée un nouvel utilisateur"""
        db_user = UserDB(
            username=username,
            email=email,
            hashed_password=hashed_password
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)

        return User(
            id=db_user.id,
            username=db_user.username,
            email=db_user.email,
            hashed_password=db_user.hashed_password,
            created_at=db_user.created_at
        )

    def find_by_email(self, email: str) -> Optional[User]:
        """Trouve un utilisateur par email"""
        db_user = self.db.query(UserDB).filter(UserDB.email == email).first()
        if not db_user:
            return None

        return User(
            id=db_user.id,
            username=db_user.username,
            email=db_user.email,
            hashed_password=db_user.hashed_password,
            created_at=db_user.created_at
        )

    def find_by_id(self, user_id: str) -> Optional[User]:
        """Trouve un utilisateur par ID"""
        db_user = self.db.query(UserDB).filter(UserDB.id == user_id).first()
        if not db_user:
            return None

        return User(
            id=db_user.id,
            username=db_user.username,
            email=db_user.email,
            hashed_password=db_user.hashed_password,
            created_at=db_user.created_at
        )

    def email_exists(self, email: str) -> bool:
        """Vérifie si un email existe"""
        return self.db.query(UserDB).filter(UserDB.email == email).first() is not None