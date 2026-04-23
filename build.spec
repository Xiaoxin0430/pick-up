# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# 收集所有需要的数据文件
datas = [
    ('static', 'static'),
    ('.venv/Lib/site-packages/dotenv', 'dotenv'),
]

# 添加所有子包
hiddenimports = [
    'fastapi',
    'fastapi.middleware.cors',
    'uvicorn',
    'sqlalchemy',
    'sqlalchemy.ext.asyncio',
    'pydantic',
    'aiomysql',
    'dotenv',
    'routers.note',
    'routers.users',
    'routers.ai',
    'routers.favorite',
    'routers.history',
    'models.note',
    'models.users',
    'models.favorite',
    'models.history',
    'crud.note',
    'crud.users',
    'crud.favorite',
    'crud.history',
    'schemas.users',
    'schemas.favorite',
    'schemas.history',
    'schemas.ai',
    'utils.auth',
    'utils.security',
    'utils.response',
    'utils.exception_handlers',
    'config.db_config',
    'llm.llm_client',
]

a = Analysis(
    ['start_server.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='ToutiaoNoteServer',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='ToutiaoNoteServer',
)
