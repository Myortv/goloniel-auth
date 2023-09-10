from pydantic import BaseModel, SecretStr


class DiscordTokenResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    refresh_token: str
    scope: str


class DiscordUserResponse(BaseModel):
    id: int
    username: str
