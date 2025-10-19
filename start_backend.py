#!/usr/bin/env python3
"""
标签体系管理系统后端启动脚本
"""
import os
import sys
import subprocess
from pathlib import Path

def main():
    """启动后端服务"""
    # 获取项目根目录
    project_root = Path(__file__).parent
    backend_dir = project_root / "backend"
    
    # 检查后端目录是否存在
    if not backend_dir.exists():
        print("❌ 后端目录不存在")
        return 1
    
    # 检查Python环境
    try:
        import uvicorn
        import fastapi
        print("✅ Python依赖已安装")
    except ImportError:
        print("📦 安装Python依赖...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "backend/requirements.txt"], check=True)

    # 启动服务
    print("🚀 启动标签体系管理系统后端服务...")
    print("📍 服务地址: http://localhost:8000")
    print("📚 API文档: http://localhost:8000/docs")
    print("🛑 按 Ctrl+C 停止服务")
    
    try:
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "backend.app.main:app", 
            "--reload", 
            "--host", "0.0.0.0", 
            "--port", "8000"
        ])
    except KeyboardInterrupt:
        print("\n👋 服务已停止")
        return 0
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
