from fastapi import APIRouter, Depends,Query
from sqlalchemy.ext.asyncio import AsyncSession

from config.db_config import get_db
from crud.history import add_history_note, get_history_note, remove_history_note
from models.users import User
from schemas.history import HistoryAddRequest, HistoryListResponse
from utils.auth import get_current_user
from utils.response import success_response

HistoryAddRequest
router = APIRouter(prefix="/api/history",tags=["history"])


# 添加浏览历史
# 获取随笔id 根据随笔id添加到history表 返回这条随笔
@router.post("/add")
async def add_history(
        data:HistoryAddRequest,
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    history_note = await add_history_note(db,data.note_id,user.id)
    return success_response(message="success",data=history_note)

# 获取浏览历史
@router.get("/list")
async def list_history(
        page: int = Query(1, ge=1),
        page_size: int = Query(10, ge=1, he=100),
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    rows, total = await get_history_note(db, page, page_size, user.id)
    history_list = [
        {
            **note.__dict__,
            "history_time": favorite_time,
            "history_id": favorite_id
        }
        for note, favorite_time, favorite_id in rows
    ]
    has_more = total > page * page_size
    data = HistoryListResponse(list=history_list, total=total, has_more=has_more)
    return success_response(message="获取收藏列表成功",data=data)

# 删除单条浏览历史
@router.delete("/delete/{history_id}")
async def remove_history(
        history_id: int,
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    data = await remove_history_note(db, history_id, user.id)
    return success_response(message="删除成功")