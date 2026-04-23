from models.favorite import Favorite
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,delete,func
from fastapi import HTTPException
from models.note import Note

#检查收藏状态
async def check_favorite(db: AsyncSession, note_id: int, user_id: int,):
    stmt = select(Favorite).where(Favorite.note_id== note_id, Favorite.user_id == user_id)
    result = await db.execute(stmt)
    is_favorite = result.scalars().first()
    return is_favorite is not None

# 收藏随笔
async def add_favorite_note(db:AsyncSession, note_id: int, user_id: int):
    favorite_note = Favorite(user_id = user_id, note_id=note_id)
    db.add(favorite_note)
    await db.commit()
    return favorite_note

# 删除随笔
async def remove_favorite_note(db:AsyncSession, note_id: int, user_id: int):
    stmt = delete(Favorite).where(Favorite.note_id== note_id, Favorite.user_id == user_id)
    result = await db.execute(stmt)
    await db.commit()
    if result.rowcount > 0:
        return True

# 获取收藏列表
async def get_favorite_note(
        db:AsyncSession, page: int, page_size: int,user_id: int
):
    # 获取收藏总数
    stmt = select(func.count()).where(Favorite.user_id == user_id)
    count = await db.execute(stmt)
    total = count.scalar_one()

    # 获取收藏列表
    skip = (page - 1) * page_size
    stmt = (select(Note,Favorite.created_at.label("favorite_time"),Favorite.id.label("favorite_id"))
            .join(Favorite,Note.id == Favorite.note_id)
            .where(Favorite.user_id == user_id)
            .order_by(Favorite.created_at.desc())
            .offset(skip)
            .limit(page_size))
    result = await db.execute(stmt)
    rows = result.all()
    return rows,total
