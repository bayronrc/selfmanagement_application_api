from fastapi import HTTPException,status
import httpx
from jose import jwt, JWTError
from app.core.config import settings

async def get_jwks():
    """Obtiene las clasbes publicas de clerk las cuales verifican el JWT"""
    async with httpx.AsyncClient() as client:
        res = await client.get(
            f"https://{settings.CLERK_FRONTEND_API}/.well-know/jwks.json"
        )
        return res.json()
async def verify_clerk_token(token: str):
    try:
        jwks = await get_jwks()
        payload = jwt.decode(
            token,
            jwks,
            algorithms=["RS256"],
            options={"verify_aud":False}
        )
        return payload
    except JWTError:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Invalid Token or Token has expired")
