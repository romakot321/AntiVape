from redis import Redis

from db.create import Settings

redis_connection = Redis(host=Settings().redis_host, charset="utf-8",
                         decode_responses=True)
