from sqlalchemy import Column, String, DateTime, Table, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from app.database import Base

def generate_uuid():
    """Génère un UUID v4 sous forme de string"""
    return str(uuid.uuid4())

# Table d'association pour les likes (Many-to-Many)
post_likes = Table(
    'post_likes',
    Base.metadata,
    Column('user_id', String, ForeignKey('users.id'), primary_key=True),
    Column('post_id', String, ForeignKey('posts.id'), primary_key=True),
    Column('created_at', DateTime, default=datetime.utcnow)
)

class UserDB(Base):
    """Modèle SQLAlchemy pour les utilisateurs"""
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    username = Column(String(50), nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relations
    posts = relationship("PostDB", back_populates="author", cascade="all, delete-orphan")
    liked_posts = relationship("PostDB", secondary=post_likes, back_populates="liked_by")

class PostDB(Base):
    """Modèle SQLAlchemy pour les posts"""
    __tablename__ = "posts"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey('users.id'), nullable=False, index=True)
    content = Column(String(500), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    
    # Relations
    author = relationship("UserDB", back_populates="posts")
    liked_by = relationship("UserDB", secondary=post_likes, back_populates="liked_posts")
    
    @property
    def likes_count(self) -> int:
        """Retourne le nombre de likes"""
        return len(self.liked_by)
