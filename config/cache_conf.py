import json
from typing import Any

import redis.asyncio as redis

# 创建redis的连接对象
redis_client = redis.Redis(
    host='localhost',
    port=6379,
    db=0,
    decode_responses=True
)

# 封装设置缓存与读取缓存

# 读取缓存
async def get_cache(key:str):
    try:
        return await redis_client.get(key)
    except Exception as e:
        print(f"获取缓存失败{e}")
        return None
# 读取列表
async def get_json_cache(key:str):
    try:
        data = await redis_client.get(key)
        if data:
            return json.loads(data)
        return None
    except Exception as e:
        print(f"获取json缓存失败{e}")
        return None

# 设置缓存
async def set_cache(key:str, value: Any, expire:int=3600):
    try:
        if isinstance(value, (list, dict)):
            value = json.dumps(value, ensure_ascii=False)
        await redis_client.setex(key, expire, value)
        return True
    except Exception as e:
        print(f"缓存设置失败{e}")
        return False
