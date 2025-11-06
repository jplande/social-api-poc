from typing import Optional, Dict
from app.models.user import User
import uuid

class UserRepository:
    """Repository pour gérer les utilisateurs (mock en mémoire)"""
    
    def __init__(self):
        self._users: Dict[str, User] = {}
        self._email_index: Dict[str, str] = {}  # email -> user_id
    
    def create(self, username: str, email: str, hashed_password: str) -> User:
        """Crée un nouvel utilisateur"""
        user_id = str(uuid.uuid4())
        user = User(
            id=user_id,
            username=username,
            email=email,
            hashed_password=hashed_password
        )
        self._users[user_id] = user
        self._email_index[email] = user_id
        return user
    
    def find_by_email(self, email: str) -> Optional[User]:
        """Trouve un utilisateur par email"""
        user_id = self._email_index.get(email)
        return self._users.get(user_id) if user_id else None
    
    def find_by_id(self, user_id: str) -> Optional[User]:
        """Trouve un utilisateur par ID"""
        return self._users.get(user_id)
    
    def email_exists(self, email: str) -> bool:
        """Vérifie si un email existe"""
        return email in self._email_index

# Singleton pour le POC
user_repository = UserRepository()
