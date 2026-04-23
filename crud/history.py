from sqlalchemy import select, func, delete
from sqlalchemy.ext.asyncio import AsyncSession


from models.history import History
from models.note import Note


# 添加浏览历史
async def add_history_note(db:AsyncSession,note_id,user_id):
    history_note = History(note_id = note_id, user_id = user_id)
    db.add(history_note)
    await db.commit()
    return history_note

# 获取浏览历史
async def get_history_note(
        db:AsyncSession,page: int,page_size: int,user_id: int
):
    # 计算浏览历史总数
    stmt = select(func.count()).where(History.user_id == user_id)
    count = await db.execute(stmt)
    total = count.scalar_one()

    # 获取浏览历史
    skip = (page - 1) * page_size
    stmt = (select(Note, History.view_time.label("view_time"), History.id.label("history_id"))
            .join(History, Note.id == History.note_id)
            .where(History.user_id == user_id)
            .order_by(History.view_time.desc())
            .offset(skip)
            .limit(page_size))
    result = await db.execute(stmt)
    rows = result.all()
    return rows, total

# 删除单条浏览历史
async def remove_history_note(db:AsyncSession,history_id,user_id):
    stmt = delete(History).where(History.user_id == user_id,History.note_id == history_id)
    result = await db.execute(stmt)
    await db.commit()
    if result.rowcount > 0:
        return True