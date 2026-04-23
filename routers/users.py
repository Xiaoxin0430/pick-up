
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from config.db_config import get_db
from crud.users import get_user_by_username, create_user, create_token, authenticate_user, update_user, update_password
from schemas.users import UserRequest, UserAuthResponse, UserInfoResponse, UserInfoBase, UserUpdateRequest, UserPassword
from utils.auth import get_current_user
from utils.response import success_response

router = APIRouter(prefix="/api/user", tags=["users"])

# 用户注册
@router.post("/register")
async def register(user_data: UserRequest,db: AsyncSession = Depends(get_db)):
    # 验证用户是否存在
    existing_user = await get_user_by_username(db, user_data.username)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="用户已注册")
    # 创建用户
    user = await create_user(db, user_data)
    # 生成token
    token = await create_token(db, user.id)
    # return {
    #     "code": 200,
    #     "message": "注册成功",
    #     "data": {
    #         "token": token,
    #         "userInfo": {
    #         "id": user.id,
    #         "username": user.username,
    #         "bio": user.bio,
    #         "avatar": user.avatar,
    #     }
    #   }
    # }
    response_data = UserAuthResponse(token=token,user_info=UserInfoResponse.from_orm(user))
    return success_response(data=response_data)

# 用户登录
@router.post("/login")
async def login(user_data: UserRequest, db: AsyncSession = Depends(get_db)):
    # 验证用户:是否未注册,密码是否正确
    user = await authenticate_user(db, user_data)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="用户名或密码错误")
    # 生成token
    token = await create_token(db, user.id)
    response_data = UserAuthResponse(token=token, user_info=UserInfoResponse.from_orm(user))
    return success_response("登录成功",data=response_data)

# 获取用户信息
@router.get("/info")
async def user_info(db: AsyncSession = Depends(get_db),current_user = Depends(get_current_user)):
    # 查token查用户,
    response_data = UserInfoResponse.from_orm(current_user)
    return success_response("获取用户信息成功",data=response_data)

# 修改用户信息：验证Token 更新（用户输入数据  put提交   请求体参数   定义pydantic模型类）  响应结果
@router.put("/update")
# 参数：用户输入的，验证token的，db
async def update_user_info(user_data:UserUpdateRequest, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    # 通过token获取当前用户
    user = await update_user(db,current_user.username,user_data)
    return success_response("更新信息成功",data=UserInfoResponse.from_orm(user))

# 修改用户密码：检查token 更新密码（用户输入密码 put提交 请求体参数 定义pydantic模型类） 响应结果
@router.put("/password")
async def change_password(user_data:UserPassword, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    user = await update_password(db,current_user.username,user_data)
    return success_response("更新密码成功",data=UserInfoResponse.from_orm(user))