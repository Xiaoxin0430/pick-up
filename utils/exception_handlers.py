from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from utils.exception import http_exception_handler, integrity_error_handler, sqlalchemy_error_handler, general_exception_handler
def register_exception_handlers(app):
    # 注册全局异常处理器.子类在前，父类在后
    app.add_exception_handler(HTTPException, http_exception_handler)#业务
    app.add_exception_handler(IntegrityError, integrity_error_handler)#数据完整性
    app.add_exception_handler(SQLAlchemyError, sqlalchemy_error_handler)#数据库错误
    app.add_exception_handler(Exception, general_exception_handler)#通用异常处理器