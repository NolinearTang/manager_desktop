"""
标签体系管理系统 - 主应用入口
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn

from backend.app.core.config import settings
from backend.app.api import labels, rules, entity_tags, intent_recognition, items

# 创建FastAPI应用实例
app = FastAPI(
    title="标签体系管理系统",
    description="基于意图识别的智能标签体系管理平台",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# 配置CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 静态文件服务
app.mount("/static", StaticFiles(directory="web"), name="static")

# 注册路由
app.include_router(labels.router, prefix="/api/v1/labels", tags=["标签管理"])
app.include_router(rules.router, prefix="/api/v1/rules", tags=["规则管理"])
app.include_router(entity_tags.router, prefix="/api/v1/entity-tags", tags=["实体标签管理"])
app.include_router(intent_recognition.router, prefix="/api/v1/intent-recognition", tags=["意图识别"])
app.include_router(items.router, prefix="/api/v1/items", tags=["数据项管理"])

@app.get("/")
async def root():
    """根路径，返回API信息"""
    return {
        "message": "标签体系管理系统 API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health")
async def health_check():
    """健康检查接口"""
    return {"status": "healthy", "message": "服务运行正常"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
