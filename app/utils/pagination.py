from typing import Optional
from datetime import datetime

def create_cursor(timestamp: datetime) -> str:
    """Crée un cursor depuis un timestamp"""
    return timestamp.isoformat()

def parse_cursor(cursor: str) -> Optional[datetime]:
    """Parse un cursor en timestamp"""
    try:
        return datetime.fromisoformat(cursor)
    except (ValueError, TypeError):
        return None
