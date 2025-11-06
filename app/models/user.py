from pydantic import BaseModel, EmailStr
from datetime import datetime

class User(BaseModel):
    id: str
    username: str
    email: EmailStr
    hashed_password: str
    created_at: datetime = None
    
    def __init__(self, **data):
        if 'created_at' not in data or data['created_at'] is None:
            data['created_at'] = datetime.utcnow()
        super().__init__(**data)
