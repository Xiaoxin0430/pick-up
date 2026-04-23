from fastapi import APIRouter, Depends

from schemas.ai import ChatRequest
from llm import llm_client
from utils.auth import get_current_user
from utils.response import success_response

router = APIRouter(prefix="/api/ai",tags=["ai"])

# AI聊天接口
@router.post("/chat")
async def ai_chat(message: ChatRequest,current_user = Depends(get_current_user)):
    # 验证用户token 接收用户输入message 调用第三方大模型api 返回ai
    response = llm_client.think(message.message)
    return success_response("获取成功",response)