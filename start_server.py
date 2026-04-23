"""
拾页随笔后端系统 - 启动脚本
双击此文件即可启动服务
"""
import sys
import os
import webbrowser
import socket
from pathlib import Path

# 添加当前目录到路径
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

# 导入 FastAPI 应用
from main import app
import uvicorn

def is_port_available(port):
    """检查端口是否可用"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(('0.0.0.0', port))
            return True
        except socket.error:
            return False

def open_browser():
    """延迟打开浏览器"""
    import time
    time.sleep(2)
    webbrowser.open('http://localhost:8000/docs')

def main():
    """主函数"""
    print("=" * 60)
    print("🚀 拾页随笔后端系统启动中...")
    print("=" * 60)
    print()
    
    # 检查端口
    port = 8000
    if not is_port_available(port):
        print(f"❌ 错误：端口 {port} 已被占用！")
        print("请关闭其他使用该端口的程序，或修改启动端口。")
        input("\n按回车键退出...")
        return
    
    # 检查数据库配置
    env_file = current_dir / "static" / ".env"
    if not env_file.exists():
        print(f"⚠️  警告：未找到配置文件 {env_file}")
        print("请确保数据库配置正确！")
        print()
    
    print("✅ 服务配置信息:")
    print(f"   📍 地址：http://localhost:{port}")
    print(f"   📚 API 文档：http://localhost:{port}/docs")
    print(f"   🏠 首页：http://localhost:{port}")
    print()
    print("💡 提示:")
    print("   - 按 Ctrl+C 可停止服务")
    print("   - 窗口可最小化到任务栏")
    print()
    print("=" * 60)
    print()
    
    # 延迟打开浏览器
    import threading
    browser_thread = threading.Thread(target=open_browser, daemon=True)
    browser_thread.start()
    
    try:
        # 启动服务
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=port,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n\n✅ 服务已停止")
    except Exception as e:
        print(f"\n❌ 错误：{e}")
        input("\n按回车键退出...")

if __name__ == "__main__":
    main()
