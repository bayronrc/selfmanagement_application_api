
import jwt
from fastapi import Depends, HTTPException, status
from jwt import PyJWKClient

from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.models import user
from app.models.user import User
from app.services.clerk_service import fetch_clerk_user
from app.services.user_service import create_user_in_db, get_user_by_clerk_id
from app.core.config import settings


security = HTTPBearer()

jwks_client = PyJWKClient(settings.CLERK_JWKS_URL)

async def verify_clerk_token(
        credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Verificar el JWT de clerk y retorna el clerk_id
    """
    token = credentials.credentials
    try:
        signin_key = jwks_client.get_signing_key_from_jwt(token)
        payload = jwt.decode(
            token,
            signin_key.key,
            algorithms=["RS256"],
            options={"verify_aud": False},
        )
        clerk_id = payload.get("sub")
        if not clerk_id :
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token invalido: no contiene 'sub'"
            )
        return clerk_id
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token Expirado"
        )
    except jwt.InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token invalido : {str(e)}"
        )
async def get_current_user(
        clerk_id: str = Depends(verify_clerk_token),
        db: AsyncSession = Depends(get_db),
):
    user = await get_user_by_clerk_id(db,clerk_id)
    if not user:
        clerk_data = await fetch_clerk_user(clerk_id)
        user = await create_user_in_db(db, clerk_data)
    return user
