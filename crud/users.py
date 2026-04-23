# 根据用户名查询数据库
import uuid
from datetime import timedelta, datetime

from fastapi import HTTPException
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from models.users import User, UserToken
from schemas.users import UserRequest, UserUpdateRequest, UserPassword
from utils import security
from utils.security import verify_password, get_hash_password


# 通过用户名查询用户是否已经注册
async def get_user_by_username(db: AsyncSession, username: str):
    stmt = await db.execute(select(User).where(User.username == username))
    result = stmt.scalar_one_or_none()
    return result

# 创建用户
async def create_user(db: AsyncSession, user_data: UserRequest):
    # 对密码加密处理
    hashed_password = security.get_hash_password(user_data.password)
    # 将用户输入的用户名与加密后的密码传入User对象
    user = User(username=user_data.username,password=hashed_password)
    # 上传数据库
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

# 生成token
async def create_token(db: AsyncSession, user_id: int):
    # 生成token
    token =str(uuid.uuid4())
    # 并设置过期时间
    expires_at = datetime.now() + timedelta(days=7)
    # 查询数据库当前用户是否有token,有则更新，无则添加
    query = select(UserToken).where(UserToken.user_id == user_id)
    result = await db.execute(query)
    user_token = result.scalar_one_or_none()

    if user_token:
        user_token.token = token
        user_token.expires_at = expires_at
    else:
        user_token = UserToken(user_id=user_id, token=token,expires_at=expires_at)
        db.add(user_token)
    return token

# 验证用户名和密码
async def authenticate_user(db: AsyncSession, user_data: UserRequest):
    user = await get_user_by_username(db, user_data.username)
    if not user:
        return None
    if not security.verify_password(user_data.password, user.password):
        return None

    return user

# 根据token查用户
async def get_user_by_token(db: AsyncSession, token: str):
    stmt = select(UserToken).where(UserToken.token == token)
    result = await db.execute(stmt)
    db_token = result.scalar_one_or_none()
    if not db_token or db_token.expires_at < datetime.now():
        return None
    stmt = select(User).where(User.id == db_token.user_id)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    return  user

# 更新用户信息
async def update_user(db: AsyncSession, username: str, user_data: UserUpdateRequest):
    query = update(User).where(User.username == username).values(**user_data.model_dump(
        exclude_unset=True,
        exclude_none = True
    ))
    result = await db.execute(query)
    await db.commit()

    if result.rowcount == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="用户不存在")

    # 获取更新后的用户信息
    update_user= await get_user_by_username(db,username)
    return update_user

# 更新用户密码
async def update_password(db: AsyncSession, username: str, user_data: UserPassword):
    # 验证旧密码
    query = select(User).where(User.username == username)
    result = await db.execute(query)
    user = result.scalar_one_or_none()

    auth_old = verify_password(user_data.oldPassword, user.password)
    if not auth_old:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="旧密码错误")
    # 更新密码
    query = update(User).where(User.username == username).values(password=get_hash_password(user_data.newPassword))
    result = await db.execute(query)
    await db.commit()
    if result.rowcount == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="用户不存在")
    # 获取更新后的用户信息
    update_user = await get_user_by_username(db, username)
    return update_user