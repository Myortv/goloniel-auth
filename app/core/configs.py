from typing import Optional, List

from datetime import timedelta

from os.path import dirname, abspath, join

import aiohttp
from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl, validator

from cryptography.hazmat.primitives import serialization

from plugins.token import TokenManager


BASE_DIR = dirname(dirname(dirname(abspath(__file__))))


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = 'Goloniel Auth'
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = ["http://localhost"]
    DOCS_URL: str = '/docs'

    POSTGRES_DB: str
    POSTGRES_PASSWORD: str
    POSTGRES_USER: str
    POSTGRES_HOST: Optional[str] = 'localhost'

    refresh_token_url: str = 'api/v1/token/refresh'
    # email_url: str = 'http://?/v1/user/closed/get-by-email'
    # save_url: str = 'http://?/v1/user/closed'
    # change_pass: str = 'http://?/v1/user/closed/password-change'

    refresh_token_expires: timedelta = timedelta(weeks=1)
    REFRESH_TOKEN_HOURS: int
    access_token_expires: timedelta = timedelta(minutes=30)
    ACCESS_TOKEN_MINUTES: int

    PRIVATE_JWT_KEY: Optional[str] = None
    PUBLIC_JWT_KEY: Optional[str] = None
    JWT_ALGORITHM: str = 'RS256'
    PEM_PASS: str

    API_JWT_KEY: Optional[str] = None
    API_JWT_AGORITHM: str = 'HS256'
    api_token: Optional[str] = None

    AIOHTTP_SESSION: Optional[aiohttp.ClientSession] = None

    RABBITMQ_HOST: Optional[str] = 'localhost'
    RABBITMQ_PORT: Optional[int] = 5672
    RABBITMQ_USERNAME: Optional[str] = 'guest'
    RABBITMQ_PASSWORD: Optional[str] = 'guest'

    DISCORD_AUTH_URL: str = 'https://discord.com/api/oauth2/authorize?client_id=1122200855014285432&redirect_uri=http%3A%2F%2Flocalhost%3A8000%2Fapi%2Fv1%2Fintegrations%2Fdiscord%2Ftoken-callback&response_type=code&scope=identify'
    DISCORD_CLIENT_ID: str = None
    DISCORD_CLIENT_SECRET: str = None

    DISCORD_CALLBACK_URL: str = 'http://localhost:8000/api/v1/integrations/discord/token-callback'

    @property
    def aiohttp_session(self):
        if not self.AIOHTTP_SESSION:
            self.AIOHTTP_SESSION = aiohttp.ClientSession()
        return self.AIOHTTP_SESSION

    def actualize_time(self):
        if self.REFRESH_TOKEN_HOURS:
            self.refresh_token_expires = timedelta(
                hours=self.REFRESH_TOKEN_HOURS,
            )
        if self.ACCESS_TOKEN_MINUTES:
            self.access_token_expires = timedelta(
                minutes=self.ACCESS_TOKEN_MINUTES,
            )

    def load_public_key(self):
        if not self.PUBLIC_JWT_KEY:
            with open(join(BASE_DIR, 'public_key.pem'), 'rb') as key_file:
                public_key = serialization.load_pem_public_key(
                    key_file.read(),
                )
                self.PUBLIC_JWT_KEY = public_key
        return self.PUBLIC_JWT_KEY

    def load_privat_key(self):
        if not self.PRIVATE_JWT_KEY:
            with open(join(BASE_DIR, 'private_key.pem'), 'rb') as key_file:
                private_key = serialization.load_pem_private_key(
                    key_file.read(),
                    password=bytes(self.PEM_PASS, 'utf-8'),
                )
                self.PRIVATE_JWT_KEY = private_key
        return self.PRIVATE_JWT_KEY

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(
        cls,
        v: str | List[str]
    ) -> List[str] | str:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)


settings = Settings()
settings.actualize_time()
settings.load_public_key()
settings.load_privat_key()

tags_metadata = [
    {
        "name": "Token",
        "description": ". . .",
    },
    {
        "name": "User",
        "description": ". . .",
    },
    {
        "name": "Integrations",
        "description": ". . .",
    },
]


token_manager = TokenManager(
    settings.PRIVATE_JWT_KEY,
    settings.PUBLIC_JWT_KEY,
    settings.JWT_ALGORITHM,
)
