"""
创建桌面快捷方式
运行此脚本会在桌面创建"拾页随笔后端"的快捷方式
"""
import os
import sys
from pathlib import Path

def create_shortcut():
    """创建桌面快捷方式"""
    try:
        # 尝试导入必要的库
        import winshell
        from win32com.client import Dispatch
    except ImportError:
        print("❌ 需要安装 winshell 和 pywin32")
        print("正在安装...")
        os.system(f"{sys.executable} -m pip install winshell pywin32")
        print("✅ 安装完成，请重新运行此脚本")
        input("\n按回车键退出...")
        return
    
    # 获取桌面路径
    desktop = winshell.desktop()
    
    # 获取项目路径
    project_dir = Path(__file__).parent
    exe_path = project_dir / "dist" / "ToutiaoNoteServer" / "ToutiaoNoteServer.exe"
    
    # 检查 exe 是否存在
    if not exe_path.exists():
        print(f"❌ 未找到可执行文件：{exe_path}")
        print("请先运行打包脚本 build_exe.py")
        input("\n按回车键退出...")
        return
    
    # 创建快捷方式
    shortcut_name = "拾页随笔后端.lnk"
    shortcut_path = os.path.join(desktop, shortcut_name)
    
    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(shortcut_path)
    
    # 设置快捷方式属性
    shortcut.TargetPath = str(exe_path)
    shortcut.WorkingDirectory = str(project_dir / "dist" / "ToutiaoNoteServer")
    shortcut.Description = "拾页随笔后端服务 - 双击启动 API 服务"
    
    # 保存快捷方式
    shortcut.save()
    
    print("=" * 60)
    print("✅ 桌面快捷方式创建成功！")
    print("=" * 60)
    print(f"\n📍 快捷方式位置:")
    print(f"   {shortcut_path}")
    print(f"\n💡 使用方法:")
    print(f"   1. 返回桌面")
    print(f"   2. 双击 '拾页随笔后端' 图标")
    print(f"   3. 服务会自动启动并打开浏览器")
    print("\n" + "=" * 60)
    
    input("\n按回车键退出...")

if __name__ == "__main__":
    create_shortcut()
