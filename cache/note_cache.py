from typing import List, Dict, Any

from config.cache_conf import get_json_cache, set_cache

CATEGORIES_KEY = "note:categories"

# 获取随笔分类缓存
async def get_cache_categoried():
    return await get_json_cache(CATEGORIES_KEY)

# 设置随笔分类缓存
async def set_cache_categoried(data:List[Dict[str, Any]], expire:int=3600):
    return await set_cache(CATEGORIES_KEY, data,expire)