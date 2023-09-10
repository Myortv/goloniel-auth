from aiohttp import ClientSession

from app.schemas.response import DiscordTokenResponse, DiscordUserResponse

from app.core.configs import settings


async def get_discord_token(
    code: str
) -> DiscordTokenResponse:
    session: ClientSession = settings.aiohttp_session
    response = await session.post(
        'https://discord.com/api/v10/oauth2/token',
        data={
            'client_id': settings.DISCORD_CLIENT_ID,
            'client_secret': settings.DISCORD_CLIENT_SECRET,
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': settings.DISCORD_CALLBACK_URL,
        },
        headers={
            'Content-Type': 'application/x-www-form-urlencoded',
        },
    )
    if response.status == 200:
        return DiscordTokenResponse(**(await response.json()))


async def get_discord_user(
    response: DiscordTokenResponse,
) -> DiscordUserResponse:
    session: ClientSession = settings.aiohttp_session
    response = await session.get(
        'https://discord.com/api/v10/users/@me',
        headers={
            "Authorization": f"Bearer {response.access_token}",
        },
    )
    if response.status == 200:
        return DiscordUserResponse(**(await response.json()))
