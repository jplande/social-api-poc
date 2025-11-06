from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import Optional
from app.schemas.post import PostCreateRequest, PostResponse, PostListResponse
from app.repositories.post_repository import post_repository
from app.repositories.user_repository import user_repository
from app.middlewares.auth_middleware import get_current_user_id

router = APIRouter(prefix="/api/posts", tags=["Posts"])

@router.post("", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
def create_post(
    request: PostCreateRequest,
    current_user_id: str = Depends(get_current_user_id)
):
    """Créer un nouveau post (authentification requise)"""
    
    user = user_repository.find_by_id(current_user_id)
    post = post_repository.create(current_user_id, request.content)
    
    return PostResponse(
        id=post.id,
        user_id=post.user_id,
        username=user.username,
        content=post.content,
        likes_count=post.likes_count,
        is_liked_by_me=False,
        created_at=post.created_at
    )

@router.get("", response_model=PostListResponse)
def get_posts(
    limit: int = Query(10, ge=1, le=50, description="Nombre de posts par page"),
    cursor: Optional[str] = Query(None, description="Cursor pour la pagination"),
    current_user_id: str = Depends(get_current_user_id)
):
    """
    Récupérer la liste des posts avec pagination cursor-based
    (authentification requise)
    """
    
    posts, next_cursor, has_more = post_repository.find_all_paginated(limit, cursor)
    
    # Mapper vers PostResponse
    posts_response = []
    for post in posts:
        user = user_repository.find_by_id(post.user_id)
        posts_response.append(PostResponse(
            id=post.id,
            user_id=post.user_id,
            username=user.username if user else "Unknown",
            content=post.content,
            likes_count=post.likes_count,
            is_liked_by_me=current_user_id in post.likes,
            created_at=post.created_at
        ))
    
    return PostListResponse(
        posts=posts_response,
        next_cursor=next_cursor,
        has_more=has_more
    )

@router.post("/{post_id}/like", status_code=status.HTTP_200_OK)
def toggle_like(
    post_id: str,
    current_user_id: str = Depends(get_current_user_id)
):
    """Toggle le like sur un post (authentification requise)"""
    
    post = post_repository.find_by_id(post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    
    liked = post_repository.toggle_like(post_id, current_user_id)
    
    return {
        "post_id": post_id,
        "liked": liked,
        "likes_count": post.likes_count
    }
