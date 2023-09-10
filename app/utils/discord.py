from aiohttp import ClientSession

from app.schemas.response import DiscordTokenResponse

from app.core.configs import settings


async def get_discord_token(
    code: str
):
    session: ClientSession = settings.aiohttp_session
    response = await session.post(
        'https://discord.com/api/v11/oauth2/token',
        data = {
            'client_id': settings.DISCORD_CLIENT_ID,
            'client_secret': settings.DISCORD_CLIENT_SECRET,
            'grant_type': 'authrization_code',
            'code': code,
            'redirect_uri': settings.DISCORD_CALLBACK_URL,
        },
        headers= {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
    )
    return DiscordTokenResponse(**(await response.json()))