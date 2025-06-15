import json
from typing import Any

import redis.asyncio as redis

from settings import auth_settings, redis_settings
from utils.json_encoder import CustomJSONEncoder

redis_client = redis.StrictRedis(
    host=redis_settings.host,
    port=redis_settings.port,
    db=redis_settings.db,
    decode_responses=True,
)


def generate_cache_name(prefix: str, **kwargs) -> str:
    """Generate a cache name based on the prefix and the kwargs.

    Args:
        prefix: The prefix of the cache key.
        **kwargs: The kwargs to be used to generate the cache name.

    Returns:
        The cache name.

    """
    hash_string = ":".join(f"{key}={value}" for key, value in sorted(kwargs.items()))
    return f"{prefix}:{hash_string}"


async def set_verify_code(identifier: str, code: str) -> None:
    """Set the code to the redis client.

    Args:
        identifier: The identifier.
        code: The code.

    """
    await redis_client.setex(
        name=identifier, time=auth_settings.verify_code_ttl, value=code
    )


async def get_verify_code(identifier: str) -> str | None:
    """Get the code from the redis client.

    Args:
        identifier: The identifier.

    Returns:
        The code.

    """
    return await redis_client.get(name=identifier)


async def get_cache(name: str) -> Any | None:
    """Get the cache data from the redis client.

    Args:
        name: The name of the cache.

    Returns:
        The cache data.

    """
    data = await redis_client.get(name=name)
    return json.loads(data) if data else None


async def set_cache(
    name: str, value: Any, time: int = redis_settings.cache_ttl
) -> None:
    """Set the cache data to the redis client.

    Args:
        name: The name of the cache.
        value: The value to be set to the cache.
        time: The time to live of the cache.

    """
    await redis_client.setex(
        name=name, time=time, value=json.dumps(value, cls=CustomJSONEncoder)
    )


async def publish_to_channel(channel: str, message: str) -> None:
    """Publish a message to a channel.

    Args:
        channel: The channel.
        message: The message.

    """
    await redis_client.publish(channel=channel, message=message)
