import redis.asyncio as redis

redis_client = redis.StrictRedis(host="localhost", port=6379, db=0)

if __name__ == "__main__":
    import asyncio

    async def main():
        await redis_client.publish("test", "test")

    asyncio.run(main())
