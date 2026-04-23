from fastapi.encoders import jsonable_encoder
from sqlalchemy import select, func, update
from sqlalchemy.ext.asyncio import AsyncSession

from cache.note_cache import get_cache_categoried, set_cache_categoried
from models.note import note_category,Note

# 获取随笔分类
async def get_categoried(db:AsyncSession, skip: int = 0, limit: int = 100):
    # 先查缓存
    cache_categories = get_cache_categoried()
    if cache_categories is None:
        return cache_categories

    result = await db.execute(select(note_category).offset(skip).limit(limit))
    categories = result.scalars().all()

    # 写入缓存
    if categories:
        categories = jsonable_encoder(categories)
        await set_cache_categoried(categories)

    return categories


# 获取随笔列表
async def get_list(db:AsyncSession,category_id:int,page_size: int=10,skip:int=0):
    stmt = await db.execute(select(Note).where(Note.category_id == category_id).offset(skip).limit(page_size))
    note = stmt.scalars().all()
    return note

# 获取随笔列表总数
async def get_note_count(db:AsyncSession,category_id:int):
    stmt = select(func.count(Note.id)).where(Note.category_id == category_id)
    result = await db.execute(stmt)
    total = result.scalar_one()
    return total

# 获取随笔详情
async def get_detail(db:AsyncSession,note_id:int):
    stmt = select(Note).where(Note.id == note_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

# 增加浏览量
async def increase_note_views(db: AsyncSession, note_id: int):
    stmt = update(Note).where(Note.id == note_id).values(views=Note.views + 1)
    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount > 0

# 获取相关随笔
async def get_related_note(db: AsyncSession, note_id: int, category_id: int, limit: int = 5):
    stmt = (
        select(Note)
        .where(
            Note.id != note_id,
            Note.category_id == category_id,
        )
        .order_by(
            Note.views.desc(),
            Note.publish_time.desc(),
        )
        .limit(limit)
    )
    result = await db.execute(stmt)
    return result.scalars().all()