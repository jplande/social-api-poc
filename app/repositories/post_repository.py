from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import desc
from datetime import datetime
from app.models.db_models import PostDB, UserDB
from app.models.post import Post


class PostRepository:
    """Repository pour gérer les posts avec PostgreSQL"""

    def __init__(self, db: Session):
        self.db = db

    def create(self, user_id: str, content: str) -> Post:
        """Crée un nouveau post"""
        db_post = PostDB(
            user_id=user_id,
            content=content
        )
        self.db.add(db_post)
        self.db.commit()
        self.db.refresh(db_post)

        return Post(
            id=db_post.id,
            user_id=db_post.user_id,
            content=db_post.content,
            created_at=db_post.created_at,
            likes=[user.id for user in db_post.liked_by]
        )

    def find_all_paginated(
            self,
            limit: int = 10,
            cursor: Optional[str] = None
    ) -> Tuple[List[Post], Optional[str], bool]:
        """
        Retourne (posts, next_cursor, has_more)
        Cursor = string encodant created_at + id (séparé par un |)
        """
        # Query de base triée par date décroissante puis par id croissant
        query = self.db.query(PostDB).order_by(
            desc(PostDB.created_at),
            PostDB.id
        )

        # Filtrer par cursor si présent
        if cursor is not None and cursor.strip() != "":
            try:
                cursor_created_at_str, cursor_id = cursor.split('|', 1)
                cursor_date = datetime.fromisoformat(cursor_created_at_str)

                # Filtrer pour obtenir les posts "avant" le curseur
                query = query.filter(
                    (PostDB.created_at < cursor_date) |
                    ((PostDB.created_at == cursor_date) & (PostDB.id < cursor_id))
                )
            except (ValueError, TypeError):
                pass  # Curseur invalide, ignorer

        # Récupérer limit + 1 pour savoir s'il y a plus de résultats
        db_posts = query.limit(limit + 1).all()

        has_more = len(db_posts) > limit

        if has_more:
            db_posts = db_posts[:limit]

        # Convertir en modèles Pydantic
        posts = []
        for db_post in db_posts:
            posts.append(Post(
                id=db_post.id,
                user_id=db_post.user_id,
                content=db_post.content,
                created_at=db_post.created_at,
                likes=[user.id for user in db_post.liked_by]
            ))

        # Calculer next_cursor
        if len(posts) > 0:
            last_post = posts[-1]
            next_cursor = f"{last_post.created_at.isoformat()}|{last_post.id}"
        else:
            next_cursor = None

        return posts, next_cursor, has_more

    def find_by_id(self, post_id: str) -> Optional[Post]:
        """Trouve un post par ID"""
        db_post = self.db.query(PostDB).filter(PostDB.id == post_id).first()
        if not db_post:
            return None

        return Post(
            id=db_post.id,
            user_id=db_post.user_id,
            content=db_post.content,
            created_at=db_post.created_at,
            likes=[user.id for user in db_post.liked_by]
        )

    def toggle_like(self, post_id: str, user_id: str) -> bool:
        """
        Toggle le like sur un post
        Retourne True si like ajouté, False si retiré
        """
        db_post = self.db.query(PostDB).filter(PostDB.id == post_id).first()
        if not db_post:
            return False

        db_user = self.db.query(UserDB).filter(UserDB.id == user_id).first()
        if not db_user:
            return False

        # Vérifier si l'utilisateur a déjà liké
        if db_user in db_post.liked_by:
            # Unlike
            db_post.liked_by.remove(db_user)
            self.db.commit()
            return False
        else:
            # Like
            db_post.liked_by.append(db_user)
            self.db.commit()
            return True