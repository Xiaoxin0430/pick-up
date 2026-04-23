from fastapi import FastAPI
from routers import note,users,ai,favorite,history
from fastapi.middleware.cors import CORSMiddleware
from utils.exception_handlers import register_exception_handlers

app = FastAPI()
register_exception_handlers(app)
# 跨域中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],#允许的源
    allow_credentials=True,#允许携带cookie
    allow_methods=["*"],#允许的方法
    allow_headers=["*"]#允许的请求头
)
@app.get("/")
async def root():
    return {"message": "Hello World"}

# 挂载路由分类
app.include_router(note.router)
app.include_router(users.router)
app.include_router(ai.router)
app.include_router(favorite.router)
app.include_router(history.router)