from pydantic import BaseModel
from datetime import datetime
from typing import List

class Post(BaseModel):
    id: str
    user_id: str
    content: str
    created_at: datetime = None
    likes: List[str] = []  # Liste des user_id qui ont liké
    
    def __init__(self, **data):
        if 'created_at' not in data or data['created_at'] is None:
            data['created_at'] = datetime.utcnow()
        super().__init__(**data)
    
    @property
    def likes_count(self) -> int:
        return len(self.likes)
