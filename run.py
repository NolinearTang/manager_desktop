import sys
import os
import uvicorn

def main():
    backend_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "backend")

    print("🚀 准备启动 FastAPI 服务...")
    
    uvicorn.run(
        "backend.app.main:app", 
        host="0.0.0.0", 
        port=8000,
        reload=True,
        reload_dirs=[backend_path]
    )

if __name__ == "__main__":
    main()
