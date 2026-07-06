
from datetime import datetime

from pydantic import BaseModel

from app.models.user import UserRole


class UserCreate(BaseModel):
    id: int
    clerk_id: str
    email: str
    first_name: str | None
    last_name: str | None
    avatar_url: str | None
    role: str
    created_at: datetime

    model_config = {'from_attributes': True}
