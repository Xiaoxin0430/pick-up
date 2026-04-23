from pydantic import BaseModel,ConfigDict, Field
from typing import Optional


class UserRequest(BaseModel):
    username: str
    password: str

# user_info对应的类，分为基础类型+info类型
class UserInfoBase(BaseModel):
    # 用户信息基础类型
    nickname: Optional[str] = Field(None, max_length=50, description="昵称")
    avatar: Optional[str] = Field(None, max_length=255, description="头像URL")
    gender: Optional[str] = Field(None, max_length=10, description="性别")
    bio: Optional[str] = Field(None, max_length=500, description="个人简介")

class UserInfoResponse(UserInfoBase):
    id: int
    username: str

    # 加上模型类配置，这样有的响应不需要token可以直接调用UserInfoResponse类，避免重复定义一个新的模型类
    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True
    )

# success_response中data数据类型
class UserAuthResponse(BaseModel):
    token: str
    user_info: UserInfoResponse = Field(...,alias="userInfo")

    # 模型类配置
    model_config = ConfigDict(
        populate_by_name=True, #alias字段名兼容
        from_attributes=True #自动从模型类中获取属性
    )

# 更新用户信息的模型类
class UserUpdateRequest(BaseModel):
    nickname: Optional[str] = Field(None, max_length=50, description="昵称")
    avatar: Optional[str] = Field(None, max_length=255, description="头像URL")
    gender: Optional[str] = Field(None, max_length=10, description="性别")
    bio: Optional[str] = Field(None, max_length=500, description="个人简介")
    phone:str=None

# 更新用户密码模型类
class UserPassword(BaseModel):
    oldPassword: str
    newPassword: str

