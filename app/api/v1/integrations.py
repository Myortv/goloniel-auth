from fastapi import APIRouter, Depends, HTTPException

from app.core.configs import settings

from app.controllers import token as token_controller
from app.controllers import user as user_controller

from app.requests import discord as requests

from app.utils.deps import identify_request
from app.utils.recovery_token import generate_secret


api = APIRouter()


@api.get("/discord/auth-link")
async def get_redirect_link(
    identity: dict = Depends(identify_request),
):
    state = await token_controller.create_discord_state(
        generate_secret(),
        identity['sub'],
    )
    url = (
        f'{settings.DISCORD_AUTH_URL}'
        f'&state={state.state.get_secret_value()}'
    )
    return url


@api.get("/discord/token-callback")
async def recieve_token(
    code: str,
    state: str,
):
    discord_state = await token_controller.get_discord_state(
        state,
    )
    if discord_state:
        response = await requests.get_discord_token(code)
        discord_profile = await requests.get_discord_user(response)
        response = await user_controller.update_discord_id(
            discord_state.user_account_id,
            str(discord_profile.id),
        )
        await token_controller.delete_discord_state(
            state
        )
        return response
    else:
        raise HTTPException(500, 'State is not valid')
