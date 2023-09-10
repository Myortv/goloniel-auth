from datetime import datetime

from pydantic import BaseModel, SecretStr


class SecretToken(BaseModel):
    token: SecretStr


class JwtToken(BaseModel):
    token: str
    meta: dict
    user_account_id: int


class RecoveryToken(BaseModel):
    token: SecretStr
    expire_at: datetime
    user_account_id: int


class DiscordState(BaseModel):
    state: SecretStr
    user_account_id: int
    expire_at: datetime
