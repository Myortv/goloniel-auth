from aio_pika import ExchangeType

from fastapi import FastAPI

from starlette.middleware.cors import CORSMiddleware

from prometheus_fastapi_instrumentator import Instrumentator


from app.core.configs import settings, tags_metadata

from plugins.controllers import DatabaseManager
from plugins.rabbit import RabbitManager


app = FastAPI(
    title=settings.PROJECT_NAME,
    version='0.0.1',
    docs_url=settings.DOCS_URL,
    openapi_tags=tags_metadata,
    openapi_url=f'{settings.API_V1_STR}/openapi.json',
)

if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        # allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


from app.api.v1 import (
    token,
    user,
    recover_account,
    integrations
)


app.include_router(
    token.api,
    prefix=settings.API_V1_STR + '/token',
    tags=["Token"]
)

app.include_router(
    user.api,
    prefix=settings.API_V1_STR + '/user',
    tags=["User"]
)

app.include_router(
    recover_account.api,
    prefix=settings.API_V1_STR + '/user-recover',
    tags=["UserRecover"]
)
app.include_router(
    integrations.api,
    prefix=settings.API_V1_STR + '/integrations',
    tags=["Integrations"]
)

instrumentator = Instrumentator().instrument(app)


@app.on_event('startup')
async def startup():
    await DatabaseManager.start(
        settings.POSTGRES_DB,
        settings.POSTGRES_USER,
        settings.POSTGRES_PASSWORD,
        settings.POSTGRES_HOST,
    )

    await RabbitManager.start(
        settings.RABBITMQ_HOST,
        settings.RABBITMQ_PORT,
        settings.RABBITMQ_USER,
        settings.RABBITMQ_PASSWORD,
    )
    instrumentator.expose(app, include_in_schema=True, should_gzip=True)


@app.on_event('shutdown')
async def shutdown():
    await DatabaseManager.stop()
    await settings.aiohttp_session.close()
