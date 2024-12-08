from typing import Optional
from fastapi.security import OAuth2PasswordBearer
from fastapi import Request

class OptionalOauth2Scheme(OAuth2PasswordBearer):
    async def __call__(self, request: Request) -> Optional[str]:
        try:
            return await super().__call__(request)
        except Exception:
            return None
