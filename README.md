# 拾页随笔后端系统

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688)
![MySQL](https://img.shields.io/badge/MySQL-8.0%2B-4479A1)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-Async-red)
![License](https://img.shields.io/badge/License-MIT-green)

基于 FastAPI 构建的随笔后端服务，提供用户注册登录、随笔分类与详情、收藏、浏览历史、AI 聊天等接口能力。项目使用 MySQL 作为主数据库，SQLAlchemy 异步会话访问数据，并通过 OpenAI 兼容接口接入通义千问模型。

## 目录

- [项目特性](#项目特性)
- [技术栈](#技术栈)
- [项目结构](#项目结构)
- [快速开始](#快速开始)
- [环境变量](#环境变量)
- [数据库](#数据库)
- [API 概览](#api-概览)
- [认证说明](#认证说明)
- [打包部署](#打包部署)
- [开发说明](#开发说明)

## 项目特性

- 用户系统：支持注册、登录、获取用户信息、更新资料、修改密码。
- 随笔服务：支持随笔分类、分页列表、详情查看、阅读量累加和相关随笔推荐。
- 用户行为：支持随笔收藏、取消收藏、收藏列表、浏览历史记录。
- AI 聊天：基于 OpenAI Python SDK 的兼容接口调用 DashScope / 通义千问模型。
- 统一响应：成功响应统一返回 `code`、`message`、`data`。
- 异步数据库：基于 `sqlalchemy.ext.asyncio` 和 `aiomysql` 访问 MySQL。
- Windows 打包：提供 PyInstaller 配置，可生成本地可执行服务程序。

## 技术栈

| 类型 | 技术 |
| --- | --- |
| Web 框架 | FastAPI |
| ASGI 服务 | Uvicorn |
| 数据库 | MySQL |
| ORM | SQLAlchemy Async |
| 数据库驱动 | aiomysql |
| 数据校验 | Pydantic |
| 鉴权 | Bearer Token，Token 存储于 `user_token` 表 |
| 密码加密 | passlib bcrypt |
| 缓存 | Redis，当前主要用于随笔分类缓存 |
| AI SDK | OpenAI Python SDK 兼容接口 |
| 打包 | PyInstaller |

## 项目结构

```text
toutiao_backend/
├── cache/                         # 缓存封装
│   └── note_cache.py
├── config/                        # 配置模块
│   ├── cache_conf.py              # Redis 配置
│   └── db_config.py               # MySQL 异步连接配置
├── crud/                          # 数据访问层
│   ├── favorite.py
│   ├── history.py
│   ├── note.py
│   └── users.py
├── llm/                           # 大模型调用
│   └── llm_client.py
├── models/                        # SQLAlchemy 模型
│   ├── favorite.py
│   ├── history.py
│   ├── note.py
│   └── users.py
├── routers/                       # API 路由
│   ├── ai.py
│   ├── favorite.py
│   ├── history.py
│   ├── note.py
│   └── users.py
├── schemas/                       # Pydantic Schema
│   ├── ai.py
│   ├── base.py
│   ├── favorite.py
│   ├── history.py
│   └── users.py
├── static/
│   └── .env                       # 本地环境变量
├── tools/                         # 工具脚本
├── utils/                         # 通用工具、鉴权、响应和异常处理
├── 项目物料/
│   ├── 01-接口规范文档/
│   ├── 02-数据库sql文件/
│   │   └── database.sql
│   └── 03-前端项目代码/
├── build.spec                     # PyInstaller 打包配置
├── build_exe.py                   # 一键打包脚本
├── create_shortcut.py             # Windows 快捷方式脚本
├── main.py                        # FastAPI 应用入口
├── start_server.py                # 本地启动脚本
└── test_main.http                 # HTTP 测试文件
```

## 快速开始

### 1. 准备环境

请先安装以下运行环境：

- Python 3.10+
- MySQL 8.0+
- Redis，可选；用于分类缓存

### 2. 创建虚拟环境

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
```

### 3. 安装依赖

当前项目根目录未看到独立的 `requirements.txt`，可以先按运行所需依赖安装：

```powershell
pip install fastapi "uvicorn[standard]" sqlalchemy aiomysql pydantic python-dotenv "passlib[bcrypt]" openai redis
```

如果后续补充了 `requirements.txt`，推荐改用：

```powershell
pip install -r requirements.txt
```

### 4. 初始化数据库

先确认 MySQL 服务已启动，然后导入数据库脚本：

```powershell
mysql -u root -p < "项目物料\02-数据库sql文件\database.sql"
```

如果 PowerShell 环境不支持该重定向写法，可以使用：

```powershell
cmd /c "mysql -u root -p < 项目物料\02-数据库sql文件\database.sql"
```

### 5. 配置环境变量

编辑 [static/.env](D:/PyCharm/PycharmProjects/toutiao_backend/static/.env)，填写数据库连接和 AI 服务配置。示例见 [环境变量](#环境变量)。

### 6. 启动服务

开发模式：

```powershell
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

也可以使用项目自带启动脚本：

```powershell
python start_server.py
```

启动后访问：

- API 文档：http://127.0.0.1:8000/docs
- ReDoc 文档：http://127.0.0.1:8000/redoc
- 健康检查：http://127.0.0.1:8000/

## 环境变量

项目通过 [config/db_config.py](D:/PyCharm/PycharmProjects/toutiao_backend/config/db_config.py) 和 [llm/llm_client.py](D:/PyCharm/PycharmProjects/toutiao_backend/llm/llm_client.py) 读取 [static/.env](D:/PyCharm/PycharmProjects/toutiao_backend/static/.env)。

```env
# MySQL 异步连接地址
ASYNC_DATABASE_URL=mysql+aiomysql://root:your_password@127.0.0.1:3306/note_app?charset=utf8mb4

# DashScope / OpenAI 兼容接口
LLM_API_KEY=your_api_key
LLM_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
```

说明：

- `ASYNC_DATABASE_URL` 是必填项，应用启动和数据库操作都依赖该配置。
- `LLM_API_KEY` 和 `LLM_BASE_URL` 用于 `/api/ai/chat` 接口。
- 当前模型名称在 [llm/llm_client.py](D:/PyCharm/PycharmProjects/toutiao_backend/llm/llm_client.py) 中配置为 `qwen3-max`。
- 不建议将真实数据库密码或 API Key 提交到公开仓库。

## 数据库

数据库脚本位于 [项目物料/02-数据库sql文件/database.sql](D:/PyCharm/PycharmProjects/toutiao_backend/项目物料/02-数据库sql文件/database.sql)，包含建库、建表和初始数据。

核心表如下：

| 表名 | 说明 |
| --- | --- |
| `user` | 用户信息表 |
| `user_token` | 用户登录 Token 表 |
| `note_category` | 随笔分类表 |
| `note` | 随笔内容表 |
| `related_note` | 相关随笔关系表 |
| `favorite` | 用户收藏表 |
| `history` | 用户浏览历史表 |
| `ai_chat` | AI 聊天记录表 |

默认数据库名为 `note_app`，字符集为 `utf8mb4`。

## API 概览

服务启动后可以通过 Swagger UI 查看完整交互式文档：

```text
http://127.0.0.1:8000/docs
```

### 通用响应格式

```json
{
  "code": 200,
  "message": "success",
  "data": {}
}
```

### 用户接口

基础路径：`/api/user`

| 方法 | 路径 | 说明 | 认证 |
| --- | --- | --- | --- |
| `POST` | `/register` | 用户注册 | 否 |
| `POST` | `/login` | 用户登录 | 否 |
| `GET` | `/info` | 获取当前用户信息 | 是 |
| `PUT` | `/update` | 更新用户资料 | 是 |
| `PUT` | `/password` | 修改密码 | 是 |

注册示例：

```bash
curl -X POST http://127.0.0.1:8000/api/user/register \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"123456"}'
```

登录示例：

```bash
curl -X POST http://127.0.0.1:8000/api/user/login \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"123456"}'
```

### 随笔接口

基础路径：`/api/note`

| 方法 | 路径 | 说明 | 认证 |
| --- | --- | --- | --- |
| `GET` | `/categories` | 获取随笔分类 | 否 |
| `GET` | `/list` | 获取随笔列表 | 否 |
| `GET` | `/detail` | 获取随笔详情 | 否 |

随笔列表参数：

| 参数 | 说明 |
| --- | --- |
| `categoryId` | 分类 ID，必填 |
| `page` | 页码，默认 `1` |
| `page_Size` | 每页数量，默认 `10`，最大 `100` |

示例：

```bash
curl "http://127.0.0.1:8000/api/note/list?categoryId=1&page=1&page_Size=10"
```

随笔详情：

```bash
curl "http://127.0.0.1:8000/api/note/detail?id=1"
```

### 收藏接口

基础路径：`/api/favorite`

| 方法 | 路径 | 说明 | 认证 |
| --- | --- | --- | --- |
| `GET` | `/check` | 检查是否已收藏 | 是 |
| `POST` | `/add` | 添加收藏 | 是 |
| `DELETE` | `/remove` | 取消收藏 | 是 |
| `GET` | `/list` | 获取收藏列表 | 是 |

添加收藏：

```bash
curl -X POST http://127.0.0.1:8000/api/favorite/add \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"noteId":1}'
```

取消收藏：

```bash
curl -X DELETE "http://127.0.0.1:8000/api/favorite/remove?noteId=1" \
  -H "Authorization: Bearer <token>"
```

收藏列表：

```bash
curl "http://127.0.0.1:8000/api/favorite/list?page=1&pageSize=10" \
  -H "Authorization: Bearer <token>"
```

### 历史记录接口

基础路径：`/api/history`

| 方法 | 路径 | 说明 | 认证 |
| --- | --- | --- | --- |
| `POST` | `/add` | 添加浏览历史 | 是 |
| `GET` | `/list` | 获取浏览历史列表 | 是 |
| `DELETE` | `/delete/{history_id}` | 删除单条浏览历史 | 是 |

添加历史：

```bash
curl -X POST http://127.0.0.1:8000/api/history/add \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"noteId":1}'
```

历史列表：

```bash
curl "http://127.0.0.1:8000/api/history/list?page=1&page_size=10" \
  -H "Authorization: Bearer <token>"
```

### AI 聊天接口

基础路径：`/api/ai`

| 方法 | 路径 | 说明 | 认证 |
| --- | --- | --- | --- |
| `POST` | `/chat` | AI 聊天 | 是 |

示例：

```bash
curl -X POST http://127.0.0.1:8000/api/ai/chat \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"message":"请总结今天的科技随笔"}'
```

## 认证说明

登录或注册成功后，接口会返回 `token`。需要认证的接口必须在请求头中携带：

```http
Authorization: Bearer <token>
```

当前 Token 机制说明：

- Token 使用 UUID 生成。
- Token 存储在 `user_token` 表中。
- Token 默认有效期为 7 天。
- 密码使用 bcrypt 哈希后存储，不保存明文密码。

## 打包部署

### 本地运行

生产环境可以使用：

```powershell
uvicorn main:app --host 0.0.0.0 --port 8000
```

如果需要多进程部署，可以结合 Gunicorn、Nginx 或其他进程管理工具，Windows 本地环境则可以直接使用 `start_server.py`。

### 打包为 Windows 可执行文件

安装打包依赖：

```powershell
pip install pyinstaller
```

执行打包：

```powershell
python build_exe.py
```

打包完成后，产物默认位于：

```text
dist/ToutiaoNoteServer/ToutiaoNoteServer.exe
```

## 开发说明

新增接口时建议按以下分层组织代码：

1. 在 `models/` 中定义 SQLAlchemy 模型。
2. 在 `schemas/` 中定义 Pydantic 请求和响应模型。
3. 在 `crud/` 中封装数据库访问逻辑。
4. 在 `routers/` 中定义 API 路由。
5. 在 `main.py` 中注册新的路由模块。

常用开发约定：

- 异步数据库操作使用 `async` / `await`。
- 成功响应优先使用 `utils.response.success_response`。
- 需要登录的接口使用 `utils.auth.get_current_user`。
- 数据库连接配置统一放在 `static/.env`。
- 敏感信息不要提交到公开仓库。

## 常见问题

### 数据库连接失败

请检查：

- MySQL 服务是否已启动。
- `static/.env` 中的 `ASYNC_DATABASE_URL` 是否正确。
- `note_app` 数据库和表结构是否已经导入。
- 数据库账号是否拥有对应权限。

### AI 聊天接口失败

请检查：

- `LLM_API_KEY` 是否有效。
- `LLM_BASE_URL` 是否填写为 OpenAI 兼容接口地址。
- 本地网络是否可以访问模型服务。
- `llm/llm_client.py` 中的模型名称是否可用。

### 接口返回 401

请检查：

- 请求头是否包含 `Authorization`。
- 请求头格式是否为 `Bearer <token>`。
- Token 是否已经过期。
- 用户是否重新登录获取了新的 Token。

## License

本项目可按 MIT License 使用。如仓库后续补充了 `LICENSE` 文件，请以该文件为准。
