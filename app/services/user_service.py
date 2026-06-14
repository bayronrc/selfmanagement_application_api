from numpy import where
from sqlalchemy import select

from app.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.clerk_service import extract_primary_email

async def get_user_by_clerk_id(db: AsyncSession, clerk_id: str):
    result = await db.execute(
        select(User).where(User.clerk_id == clerk_id)
        )
    return result.scalar_one_or_none()

async def create_user_in_db(db: AsyncSession, clerk_data: dict):
    new_user = User(
        clerk_id = clerk_data["id"],
        email=extract_primary_email(clerk_data),
        first_name = clerk_data.get("first_name"),
        last_name = clerk_data.get("last_name"),
        avatar_url=clerk_data.get("image_url")
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user
