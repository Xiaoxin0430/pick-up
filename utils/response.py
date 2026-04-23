from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


# 封装通用的成功响应格式
def success_response(message:str = "success", data=None):
    content = {
        "code": 200,
        "message": message,
        "data": data
    }
    return JSONResponse(content=jsonable_encoder(content))