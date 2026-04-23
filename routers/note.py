

from fastapi import APIRouter, Depends, Query, HTTPException
from crud.note import get_categoried,get_list,get_note_count,get_detail,increase_note_views,get_related_note
from config.db_config import get_db
from sqlalchemy.ext.asyncio import AsyncSession
# 创建路由实例
router = APIRouter(prefix="/api/note", tags=["note"])

# 获取随笔分类
@router.get("/categories")
async def get_note_categories(skip: int = 0, limit: int = 100,db:AsyncSession = Depends(get_db)):
    # 先在缓存中获取

    # 获取数据库内的随笔分类数据---定义模型类---封装查询数据的方法
    categories = await get_categoried(db,skip, limit)
    return {
        "code": 200,
        "message": "success",
        "data": categories
    }

# 获取随笔列表
@router.get("/list")
async def get_note_list(category_id: int=Query(...,alias="categoryId"),page: int=1,page_size:int=Query(default=10,le=100,alias="page_Size"),db:AsyncSession = Depends(get_db)):
    skip = (page - 1) * page_size
    list = await get_list(db,category_id,page_size,skip)
    total = await get_note_count(db,category_id)
    has_more = (skip + len(list)) < total
    return {
        "code": 200,
        "message": "success",
        "data": {
            "list": list,
            "total": total,
            "hasMore": has_more
        }
}

# 获取随笔详情
@router.get("/detail")
async def get_note_detail(note_id: int=Query(...,alias="id"),db:AsyncSession = Depends(get_db)):
    # 获取随笔数据
    note_detail = await get_detail(db,note_id)
    if not note_detail:
        raise HTTPException(status_code=404, detail="随笔不存在")
    # 浏览量加一
    views_res = await increase_note_views(db,note_detail.id)
    if not views_res:
        raise HTTPException(status_code=404,detail="浏览量更新失败")
    # 相关随笔
    related_note = await get_related_note(db,note_detail.id,note_detail.category_id)
    return {
          "code": 200,
          "message": "success",
          "data": {
            "id": note_detail.id,
            "title": note_detail.title,
            "content": note_detail.content,
            "image": note_detail.image,
            "author": note_detail.author,
            "publishTime": note_detail.publish_time,
            "categoryId": note_detail.category_id,
            "views": note_detail.views,
            "relatedNote": [
                {
                    "id": n.id,
                    "title": n.title,
                    "image": n.image,
                } for n in related_note
            ]
    }
}


