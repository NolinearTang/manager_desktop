"""
数据项管理API
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from backend.app.core.database import get_db
from backend.app.core.schemas import (
    ItemDataCreate, ItemDataUpdate, ItemDataResponse, 
    ResponseModel, PaginationParams
)
from backend.app.services.item_service import ItemService

router = APIRouter()

@router.get("/", response_model=ResponseModel)
async def get_items(
    item_name: Optional[str] = Query(None, description="数据项名称"),
    item_type: Optional[str] = Query(None, description="数据项类型"),
    label_id: Optional[int] = Query(None, description="关联标签ID"),
    page: int = Query(1, ge=1, description="页码"),
    size: int = Query(20, ge=1, le=100, description="每页数量"),
    db: Session = Depends(get_db)
):
    """获取数据项列表"""
    try:
        item_service = ItemService(db)
        pagination = PaginationParams(page=page, size=size)
        result = item_service.get_items(
            item_name=item_name,
            item_type=item_type,
            label_id=label_id,
            pagination=pagination
        )
        return ResponseModel(data=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{item_id}", response_model=ResponseModel)
async def get_item(
    item_id: int,
    db: Session = Depends(get_db)
):
    """根据ID获取数据项"""
    try:
        item_service = ItemService(db)
        item = item_service.get_item_by_id(item_id)
        if not item:
            raise HTTPException(status_code=404, detail="数据项不存在")
        return ResponseModel(data=item)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/", response_model=ResponseModel)
async def create_item(
    item_data: ItemDataCreate,
    db: Session = Depends(get_db)
):
    """创建数据项"""
    try:
        item_service = ItemService(db)
        item = item_service.create_item(item_data)
        return ResponseModel(data=item, message="数据项创建成功")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{item_id}", response_model=ResponseModel)
async def update_item(
    item_id: int,
    item_data: ItemDataUpdate,
    db: Session = Depends(get_db)
):
    """更新数据项"""
    try:
        item_service = ItemService(db)
        item = item_service.update_item(item_id, item_data)
        if not item:
            raise HTTPException(status_code=404, detail="数据项不存在")
        return ResponseModel(data=item, message="数据项更新成功")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{item_id}", response_model=ResponseModel)
async def delete_item(
    item_id: int,
    db: Session = Depends(get_db)
):
    """删除数据项"""
    try:
        item_service = ItemService(db)
        success = item_service.delete_item(item_id)
        if not success:
            raise HTTPException(status_code=404, detail="数据项不存在")
        return ResponseModel(message="数据项删除成功")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))