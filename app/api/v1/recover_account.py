from typing import Optional

from fastapi import APIRouter
from fastapi import HTTPException

import logging


from app.controllers.user import get_by_username, set_password
from app.controllers import token as token_controller

from app.messages import recovery as message_recovery

from app.schemas.user import (
    UserUpdateProtected,
    UserInDBProtected,
)
from app.schemas.token import SecretToken
from app.schemas.password import Password

from app.utils.recovery_token import generate_secret


api = APIRouter()


@api.get('/password/send-recovery-token/')
async def recover_account(
    username: str,
    email: Optional[str] = None,
):
    """
       Emit message with user and recovery token
    """
    if user := await get_by_username(username):
        token = await token_controller.save_recovery_token(
            generate_secret(),
            user.id,
        )
        await message_recovery.emit_recovery_event(
            user,
            token,
        )
        return {'result': 'Ok'}
    else:
        raise HTTPException(404)


@api.post('/password/reset/')
async def reset_password(
    token: SecretToken,
    password: Password,
):
    """
        reset password if temporary token is valid
    """
    if recovery_token := await token_controller.get_recovery_token(
        token,
    ):
        if await set_password(
            recovery_token.user_account_id,
            password,
        ):
            return {'result': 'Ok'}
        else:
            raise HTTPException(422)
    else:
        raise HTTPException(404, 'Token not found or expired')
