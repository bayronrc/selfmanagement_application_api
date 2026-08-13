from starlette import status

from app.core.database import Base


class UploadRipsOld(Base):
    user_id: int
    uploaded_by: int
    status: str
    created_at: str
    updated_at: str
