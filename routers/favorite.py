from os import remove

from fastapi import APIRouter, Depends,Query
from sqlalchemy import nulls_last

from models.users import User
from config.db_config import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from utils.auth import get_current_user
from crud.favorite import check_favorite, add_favorite_note, remove_favorite_note, get_favorite_note
from schemas.favorite import FavoriteCheckResponse, FavoriteAddRequest, FavoriteListResponse
from utils.response import success_response
router = APIRouter(prefix="/api/favorite", tags=["favorite"])

# 检查随笔收藏状态
# 检查用户token 获取随笔id 检查（查询数据库 ）
@router.get("/check")
async def check_favorite_status(
    note_id: int = Query(..., alias="noteId"),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    is_favorite = await check_favorite(db,note_id, user.id)
    return success_response("检查收藏状态成功", data = FavoriteCheckResponse(isFavorite=is_favorite))
    
# 添加收藏
#检查用户token 数据库新增
@router.post("/add")
async def add_favorite(
    data:FavoriteAddRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    favorite_note = await add_favorite_note(db,data.note_id,user.id)
    return success_response("收藏成功",data = favorite_note)

# 取消收藏
##检查用户token 数据库删除
@router.delete("/remove")
async def delete_favorite(
    note_id: int = Query(..., alias="noteId"),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    remove_note = await remove_favorite_note(db,note_id,user.id)
    return success_response("取消收藏成功")

# 获取收藏列表
@router.get("/list")
async def get_favorite(
    page: int = Query(1,ge=1),
    page_size: int = Query(10,ge=1,le=100,alias="pageSize"),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    rows, total = await get_favorite_note(db, page, page_size, user.id)
    favorite_list = [
        {
            **note.__dict__,
            "favorite_time": favorite_time,
            "favorite_id": favorite_id
        }
        for note, favorite_time, favorite_id in rows
    ]
    has_more = total > page * page_size
    data = FavoriteListResponse(list=favorite_list, total=total, has_more=has_more)
    return success_response("获取收藏列表成功",data=data)