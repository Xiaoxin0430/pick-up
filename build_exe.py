"""
一键打包脚本 - 生成可执行文件
运行此脚本后，会在 dist 目录生成 ToutiaoNoteServer.exe
"""
import os
import sys
import subprocess
from pathlib import Path

def check_environment():
    """检查环境"""
    print("🔍 检查环境...")
    
    # 检查 Python 版本
    python_version = sys.version_info
    if python_version.major < 3 or python_version.minor < 10:
        print("⚠️  警告：建议使用 Python 3.10 或更高版本")
    
    # 检查虚拟环境
    venv_path = Path(__file__).parent / ".venv"
    if not venv_path.exists():
        print("❌ 错误：未找到虚拟环境 .venv")
        print("请先创建虚拟环境并安装依赖")
        print("命令：python -m venv .venv")
        return False
    
    # 检查 PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller 版本：{PyInstaller.__version__}")
    except ImportError:
        print("❌ 未安装 PyInstaller")
        print("正在安装...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✅ PyInstaller 安装完成")
    
    return True

def install_dependencies():
    """确保所有依赖已安装"""
    print("\n📦 检查依赖包...")
    requirements_path = Path(__file__).parent / "requirements.txt"
    
    if requirements_path.exists():
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", str(requirements_path)
        ])
    else:
        # 如果没有 requirements.txt，安装必要的包
        packages = [
            'fastapi', 'uvicorn', 'sqlalchemy', 'aiomysql',
            'pydantic', 'python-dotenv'
        ]
        for pkg in packages:
            try:
                __import__(pkg)
            except ImportError:
                print(f"  安装 {pkg}...")
                subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])
    
    print("✅ 依赖包检查完成")

def build_exe():
    """构建 exe 文件"""
    print("\n🔨 开始打包...")
    
    project_dir = Path(__file__).parent
    spec_file = project_dir / "build.spec"
    
    # 切换到项目目录
    os.chdir(project_dir)
    
    # 执行 PyInstaller
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--clean",  # 清除临时文件
        str(spec_file)
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print("\n" + "=" * 60)
        print("✅ 打包完成！")
        print("=" * 60)
        
        # 显示生成的文件位置
        dist_dir = project_dir / "dist" / "ToutiaoNoteServer"
        if dist_dir.exists():
            exe_file = dist_dir / "ToutiaoNoteServer.exe"
            if exe_file.exists():
                print(f"\n📍 可执行文件位置:")
                print(f"   {exe_file}")
                print(f"\n💡 提示:")
                print(f"   - 可以将整个 dist/ToutiaoNoteServer 文件夹复制到桌面")
                print(f"   - 运行 ToutiaoNoteServer.exe 即可启动服务")
                print(f"   - 首次启动会自动打开浏览器访问 API 文档")
        else:
            # 如果是单文件模式
            exe_file = project_dir / "dist" / "ToutiaoNoteServer.exe"
            if exe_file.exists():
                print(f"\n📍 可执行文件位置:")
                print(f"   {exe_file}")
                print(f"\n💡 提示:")
                print(f"   - 可以将此 exe 文件复制到桌面")
                print(f"   - 双击即可运行")
        
        print("\n" + "=" * 60)
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ 打包失败：{e}")
        print("\n请检查:")
        print("  1. 所有依赖是否已安装")
        print("  2. build.spec 配置是否正确")
        print("  3. 是否有文件权限问题")
        return False
    
    return True

def create_desktop_shortcut():
    """创建桌面快捷方式（可选）"""
    print("\n🔗 是否创建桌面快捷方式？")
    response = input("输入 y 创建快捷方式，其他键跳过：")
    
    if response.lower() == 'y':
        try:
            import winshell
            from win32com.client import Dispatch
            
            desktop = winshell.desktop()
            project_dir = Path(__file__).parent
            exe_path = str(project_dir / "dist" / "ToutiaoNoteServer" / "ToutiaoNoteServer.exe")
            shortcut_path = os.path.join(desktop, "拾页随笔后端.lnk")
            
            shell = Dispatch('WScript.Shell')
            shortcut = shell.CreateShortCut(shortcut_path)
            shortcut.TargetPath = exe_path
            shortcut.WorkingDirectory = str(project_dir / "dist" / "ToutiaoNoteServer")
            shortcut.save()
            
            print("✅ 桌面快捷方式创建成功！")
        except ImportError:
            print("⚠️  需要安装 winshell 和 pywin32:")
            print("   pip install winshell pywin32")
        except Exception as e:
            print(f"⚠️  创建快捷方式失败：{e}")

def main():
    """主函数"""
    print("=" * 60)
    print("📦 拾页随笔后端系统 - 打包工具")
    print("=" * 60)
    print()
    
    # 检查环境
    if not check_environment():
        return
    
    # 安装依赖
    install_dependencies()
    
    # 构建 exe
    if build_exe():
        # 询问是否创建快捷方式
        create_desktop_shortcut()
        
        print("\n🎉 所有操作完成！")
        print("\n下一步:")
        print("  1. 打开文件资源管理器")
        print("  2. 导航到 dist/ToutiaoNoteServer 目录")
        print("  3. 双击 ToutiaoNoteServer.exe 启动服务")
        print("  4. 浏览器会自动打开 API 文档页面")
    
    input("\n按回车键退出...")

if __name__ == "__main__":
    main()
