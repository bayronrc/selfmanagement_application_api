


from sqlalchemy import DateTime, Enum, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class UserRole(str,Enum):
    USER: str = "user"
    ADMIN: str = "admin"
    SUPERADMIN: str = "superadmin"

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    clerk_id: Mapped[str] = mapped_column(String(255), unique=True, index=True,nullable=False)
    email: Mapped[str] = mapped_column(String(255),nullable=False)
    first_name: Mapped[str|None] = mapped_column(String(100))
    last_name: Mapped[str|None] = mapped_column(String(100))
    avatar_url: Mapped[str|None] = mapped_column(String(500))
    role: Mapped[str] = mapped_column(String(50), default=UserRole.USER)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(),onupdate=func.now())

    batches:Mapped[list["OrderBatch"]] = relationship( back_populates="user") # pyright: ignore[reportUndefinedVariable]
