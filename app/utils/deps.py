from typing import Annotated

from fastapi import Header, Depends
from fastapi.security import OAuth2PasswordBearer

from app.core.configs import token_manager, settings


# oauth_scheme = OAuth2PasswordBearer('/token/refresh')
oauth_scheme = OAuth2PasswordBearer(settings.refresh_token_url)


async def identify_request(token: str = Depends(oauth_scheme)):
    if token:
        return token_manager.get_content(token)
