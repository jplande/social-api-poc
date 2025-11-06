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
        Cursor = string encodant created_at + id (séparé par un |)
        """
        print(f"find_all_paginated called with cursor={cursor}")
        # Trier par date décroissante puis par id croissant (pour stabilité)
        sorted_posts = sorted(
            self._posts,
            key=lambda p: (p.created_at, p.id),
            reverse=True
        )

        if cursor is not None and cursor.strip() != "":
            try:
                cursor_created_at_str, cursor_id = cursor.split('|', 1)
                cursor_date = datetime.fromisoformat(cursor_created_at_str)
                # Filtrer posts pour retourner uniquement ceux "avant" le curseur
                # Soit la date est antérieure, soit la date est égale mais l'id est inférieur
                sorted_posts = [
                    p for p in sorted_posts if
                    (p.created_at < cursor_date) or
                    (p.created_at == cursor_date and p.id < cursor_id)
                ]
            except (ValueError, TypeError):
                pass  # Curseur invalide, ignorer

        # Pagination
        page_posts = sorted_posts[:limit + 1]

        has_more = len(page_posts) > limit

        if has_more:
            page_posts = page_posts[:limit]
            last_post = page_posts[-1]
            next_cursor = f"{last_post.created_at.isoformat()}|{last_post.id}"
        else:
            # Correction ici : si on a des posts, on renvoie tout de même un next_cursor valide
            if len(page_posts) > 0:
                last_post = page_posts[-1]
                next_cursor = f"{last_post.created_at.isoformat()}|{last_post.id}"
            else:
                next_cursor = None

        print(f"Returning {len(page_posts)} posts")
        print(f"next_cursor={next_cursor}")
        print(f"Posts: {[(p.id, p.created_at.isoformat()) for p in page_posts]}")
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
