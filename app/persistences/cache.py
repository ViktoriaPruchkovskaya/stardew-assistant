from redis import Redis


class Cache:
    def __init__(self, password: str):
        self.redis: Redis = Redis(host="localhost", port=6379, decode_responses=True, password=password)

    def push(self, key: str, values: list[str]):
        self.redis.rpush(key, *values)

    def get_list(self, key, start: int, end: int):
        return self.redis.lrange(key, start, end)

    def set(self, key: str, val: str):
        self.redis.set(key, val, ex=3600)

    def get(self, key: str) -> str:
        return self.redis.get(key)
