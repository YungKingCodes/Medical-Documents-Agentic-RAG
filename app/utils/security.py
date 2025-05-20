from fastapi import Header, HTTPException, Security
from fastapi.security.api_key import APIKeyHeader

from app.core.config import settings

# API Key header definition
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

async def get_api_key(api_key: str = Security(api_key_header)):
    """Validate API key from request header."""
    if not api_key:
        raise HTTPException(
            status_code=401,
            detail="API Key header is missing"
        )
    if api_key != settings.API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Invalid API Key"
        )
    return api_key 