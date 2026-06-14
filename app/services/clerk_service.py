import httpx
from app.core.config import settings

async def fetch_clerk_user(clerk_id:str):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{settings.BACKEND_API_CLERK_URL}/users/{clerk_id}",
            headers={
                "Authorization": f"Bearer {settings.CLERK_SECRET_KEY}",
                "Content-Type":"Application/json"
            }
        )
        response.raise_for_status()
        return response.json()

def extract_primary_email(clerk_data: dict):
    email_addresses =clerk_data.get("email_addresses",[])
    primary_id = clerk_data.get("primary_email_address_id")
    for email_obj in email_addresses:
        if email_obj["id"] == primary_id:
            return email_obj["email_address"]
    return email_addresses[0]["email_address"] if email_addresses else ""
