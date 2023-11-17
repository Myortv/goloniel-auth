import logging

from fastapi import APIRouter, Depends, Request
from fastapi import HTTPException

from fastapi.security import OAuth2PasswordRequestForm

from app.core.configs import settings, token_manager

from app.controllers import token as token_controller

from app.controllers import user as user_controller

from app.schemas.token import SecretToken

from app.utils.password import compare_passwords
from app.utils.deps import identify_request

from plugins.token import BadJwtException


api = APIRouter()


@api.post('/refresh')
async def get_refresh_token(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    """ return both access and refresh token """
    user = await user_controller.sys_get_by_username(
        form_data.username,
    )
    if not user:
        raise HTTPException(404)
    if not compare_passwords(
        user.password.get_secret_value(),
        form_data.password,
    ):
        raise HTTPException(401, 'Bad password')
    refresh_token = token_manager.encode(
        {'sub': user.id, 'role': user.role},
        settings.refresh_token_expires,
    )
    meta = {
        "user-agent": request.headers.get('User-Agent'),
    }
    if not await token_controller.save_refresh_token(
        refresh_token,
        user.id,
        meta,
    ):
        raise HTTPException(507)
    access_token = token_manager.encode(
        {'sub': user.id, 'role': user.role},
        settings.access_token_expires,
    )
    result = {
        'access_token': access_token,
        'refresh_token': refresh_token,
    }
    return result


@api.post('/access')
async def get_access_token(refresh_token: SecretToken):
    """ takes refresh token, returns access token """
    try:
        payload = token_manager.get_content(
            refresh_token.token.get_secret_value()
        )
        print(payload)
        return {
            'access_token': token_manager.encode(
                data=payload,
                expires_delta=settings.access_token_expires,
            )
        }
    except BadJwtException:
        raise HTTPException(status_code=400, detail='Bad Token')


@api.delete('/close')
async def close_refresh_token(refresh_token: SecretToken):
    """ close token """
    if token := await token_controller.close_token(
        refresh_token.token.get_secret_value(),
    ):
        return token
    else:
        raise HTTPException(404, 'Refresh token not found')


@api.get('/')
async def list_alive_refresh_tokens(
    identity: dict = Depends(identify_request)
):
    """ list tokens """
    if result := await token_controller.list(
        identity['sub']
    ):
        return result
    else:
        raise HTTPException(404)
