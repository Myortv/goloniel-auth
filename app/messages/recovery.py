from ujson import dumps

import aio_pika
from aio_pika import Channel, Exchange, ExchangeType

from app.schemas.user import UserInDBProtected
from app.schemas.token import RecoveryToken

from plugins.rabbit import RabbitManager


@RabbitManager.acquire_channel('user_events', ExchangeType.DIRECT)
async def emit_recovery_event(
    user: UserInDBProtected,
    token: RecoveryToken,
    channel: Channel = None,
    exchange: Exchange = None,
) -> bool:
    message = {
        'token': token.token.get_secret_value(),
    }
    message.update(user.model_dump())
    message = await exchange.publish(
        aio_pika.Message(dumps(message).encode()),
        routing_key='recovery'
    )
    if message:
        return True
    return False
