"""
实体标签管理API
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from backend.app.core.database import get_db
from backend.app.core.schemas import (
    EntityTagCreate, EntityTagUpdate, EntityTagResponse, 
    ResponseModel, PaginationParams
)
from backend.app.services.entity_tag_service import EntityTagService

router = APIRouter()

@router.get("/", response_model=ResponseModel)
async def get_entity_tags(
    entity_tag_name: Optional[str] = Query(None, description="实体标签名称"),
    entity_type: Optional[str] = Query(None, description="实体类型"),
    page: int = Query(1, ge=1, description="页码"),
    size: int = Query(20, ge=1, le=100, description="每页数量"),
    db: Session = Depends(get_db)
):
    """获取实体标签列表"""
    try:
        entity_service = EntityTagService(db)
        pagination = PaginationParams(page=page, size=size)
        result = entity_service.get_entities(
            entity_tag_name=entity_tag_name,
            entity_type=entity_type,
            pagination=pagination
        )
        return ResponseModel(data=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{entity_id}", response_model=ResponseModel)
async def get_entity_tag(
    entity_id: int,
    db: Session = Depends(get_db)
):
    """根据ID获取实体标签"""
    try:
        entity_service = EntityTagService(db)
        entity = entity_service.get_entity_by_id(entity_id)
        if not entity:
            raise HTTPException(status_code=404, detail="实体标签不存在")
        return ResponseModel(data=entity)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/", response_model=ResponseModel)
async def create_entity_tag(
    entity_data: EntityTagCreate,
    db: Session = Depends(get_db)
):
    """创建实体标签"""
    try:
        entity_service = EntityTagService(db)
        entity = entity_service.create_entity(entity_data)
        return ResponseModel(data=entity, message="实体标签创建成功")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{entity_id}", response_model=ResponseModel)
async def update_entity_tag(
    entity_id: int,
    entity_data: EntityTagUpdate,
    db: Session = Depends(get_db)
):
    """更新实体标签"""
    try:
        entity_service = EntityTagService(db)
        entity = entity_service.update_entity(entity_id, entity_data)
        if not entity:
            raise HTTPException(status_code=404, detail="实体标签不存在")
        return ResponseModel(data=entity, message="实体标签更新成功")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{entity_id}", response_model=ResponseModel)
async def delete_entity_tag(
    entity_id: int,
    db: Session = Depends(get_db)
):
    """删除实体标签"""
    try:
        entity_service = EntityTagService(db)
        success = entity_service.delete_entity(entity_id)
        if not success:
            raise HTTPException(status_code=404, detail="实体标签不存在")
        return ResponseModel(message="实体标签删除成功")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/tag-names/list", response_model=ResponseModel)
async def get_entity_tag_names(
    db: Session = Depends(get_db)
):
    """获取所有实体标签名称"""
    try:
        entity_service = EntityTagService(db)
        tag_names = entity_service.get_entity_tag_names()
        return ResponseModel(data=tag_names)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/tag/{tag_name}/entities", response_model=ResponseModel)
async def get_entities_by_tag_name(
    tag_name: str,
    db: Session = Depends(get_db)
):
    """根据实体标签名称获取实体列表"""
    try:
        entity_service = EntityTagService(db)
        entities = entity_service.get_entities_by_tag_name(tag_name)
        # 转换为字典格式
        entities_data = []
        for entity in entities:
            entities_data.append({
                "id": entity.id,
                "entity_tag_name": entity.entity_tag_name,
                "entity_value": entity.entity_value,
                "entity_type": entity.entity_type,
                "description": entity.description,
                "is_active": entity.is_active,
                "created_at": entity.created_at,
                "updated_at": entity.updated_at
            })
        return ResponseModel(data=entities_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))