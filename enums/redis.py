from enum import StrEnum


class CachePrefixEnum(StrEnum):
    STATISTICS = "statistics:{user_id}"


class RedisChannelEnum(StrEnum):
    ORDER_STATUS_UPDATED = "order:status:{user_id}:{role}"
