from typing import List, Optional, Tuple
from app.models.post import Post
import uuid
from datetime import datetime

class PostRepository:
    """Repository pour gérer les posts (mock en mémoire)"""
    
    def __init__(self):
        self._posts: List[Post] = []
    
    def create(self, user_id: str, content: str) -> Post:
        """Crée un nouveau post"""
        post = Post(
            id=str(uuid.uuid4()),
            user_id=user_id,
            content=content
        )
        self._posts.insert(0, post)  # Plus récent en premier
        return post
    
    def find_all_paginated(
        self, 
        limit: int = 10, 
        cursor: Optional[str] = None
    ) -> Tuple[List[Post], Optional[str], bool]:
        """
        Retourne (posts, next_cursor, has_more)
        Cursor = created_at timestamp ISO pour éviter les doublons
        """
        # Trier par date décroissante
        sorted_posts = sorted(self._posts, key=lambda p: p.created_at, reverse=True)

        # Filtrer par cursor si présent ET non vide
        if cursor and cursor.strip():
            try:
                cursor_date = datetime.fromisoformat(cursor)
                sorted_posts = [p for p in sorted_posts if p.created_at < cursor_date]
            except (ValueError, TypeError):
                pass  # Cursor invalide, ignorer
        
        # Pagination
        page_posts = sorted_posts[:limit + 1]
        has_more = len(page_posts) > limit
        
        if has_more:
            page_posts = page_posts[:limit]
            next_cursor = page_posts[-1].created_at.isoformat()
        else:
            next_cursor = None
        
        return page_posts, next_cursor, has_more
    
    def find_by_id(self, post_id: str) -> Optional[Post]:
        """Trouve un post par ID"""
        return next((p for p in self._posts if p.id == post_id), None)
    
    def toggle_like(self, post_id: str, user_id: str) -> bool:
        """
        Toggle le like sur un post
        Retourne True si like ajouté, False si retiré
        """
        post = self.find_by_id(post_id)
        if not post:
            return False
        
        if user_id in post.likes:
            post.likes.remove(user_id)
            return False
        else:
            post.likes.append(user_id)
            return True

# Singleton pour le POC
post_repository = PostRepository()
