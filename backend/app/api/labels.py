"""
标签管理API
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from backend.app.core.database import get_db
from backend.app.core.schemas import (
    LabelCreate, LabelUpdate, LabelResponse, 
    ResponseModel, PaginationParams, ItemDataListResponse, ItemDataCreate,
    LabelPageResponse
)
from backend.app.services.label_service import LabelService

router = APIRouter()

@router.get("/", response_model=LabelPageResponse)
async def get_labels(
    parent_code: Optional[str] = Query(None, description="父级标签编码"),
    label_type: Optional[str] = Query(None, description="标签类型"),
    level: Optional[int] = Query(None, description="标签层级"),
    page: int = Query(1, ge=1, description="页码"),
    size: int = Query(20, ge=1, le=100, description="每页数量"),
    db: Session = Depends(get_db)
):
    """获取标签列表"""
    try:
        label_service = LabelService(db)
        pagination = PaginationParams(page=page, size=size)
        result = label_service.get_labels(
            parent_code=parent_code,
            label_type=label_type,
            level=level,
            pagination=pagination
        )
        return ResponseModel(data=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/tree", response_model=ResponseModel)
async def get_label_tree(
    root_code: Optional[str] = Query(None, description="根标签编码"),
    label_type: Optional[str] = Query(None, description="标签类型 (intent 或 entity)"),
    db: Session = Depends(get_db)
):
    """获取标签树结构"""
    try:
        label_service = LabelService(db)
        tree = label_service.get_label_tree(root_code=root_code, label_type=label_type)
        return ResponseModel(data=tree)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{label_id}", response_model=ResponseModel)
async def get_label(
    label_id: int,
    db: Session = Depends(get_db)
):
    """根据ID获取标签"""
    try:
        label_service = LabelService(db)
        label = label_service.get_label_by_id(label_id)
        if not label:
            raise HTTPException(status_code=404, detail="标签不存在")
        return ResponseModel(data=label)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/", response_model=ResponseModel)
async def create_label(
    label_data: LabelCreate,
    db: Session = Depends(get_db)
):
    """创建标签"""
    try:
        label_service = LabelService(db)
        label = label_service.create_label(label_data)
        return ResponseModel(data=label, message="标签创建成功")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{label_id}", response_model=ResponseModel)
async def update_label(
    label_id: int,
    label_data: LabelUpdate,
    db: Session = Depends(get_db)
):
    """更新标签"""
    try:
        label_service = LabelService(db)
        label = label_service.update_label(label_id, label_data)
        if not label:
            raise HTTPException(status_code=404, detail="标签不存在")
        return ResponseModel(data=label, message="标签更新成功")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{label_id}", response_model=ResponseModel)
async def delete_label(
    label_id: int,
    db: Session = Depends(get_db)
):
    """删除标签"""
    try:
        label_service = LabelService(db)
        success = label_service.delete_label(label_id)
        if not success:
            raise HTTPException(status_code=404, detail="标签不存在")
        return ResponseModel(message="标签删除成功")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{label_code}/children", response_model=ResponseModel)
async def get_children_labels(
    label_code: str,
    db: Session = Depends(get_db)
):
    """获取子标签列表"""
    try:
        label_service = LabelService(db)
        children = label_service.get_children_labels(label_code)
        return ResponseModel(data=children)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@router.get("/{label_code}/items", response_model=ItemDataListResponse)
async def get_items_for_label(
    label_code: str,
    db: Session = Depends(get_db)
):
    """根据标签编码获取其下的所有实体（Items）"""
    try:
        label_service = LabelService(db)
        items = label_service.get_items_by_label_code(label_code)
        return ResponseModel(data=items)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{label_code}/items", response_model=ResponseModel)
async def add_item_to_label(
    label_code: str,
    item_data: ItemDataCreate,
    db: Session = Depends(get_db)
):
    """向指定标签添加一个新的数据项"""
    try:
        label_service = LabelService(db)
        new_item = label_service.add_item_to_label(label_code, item_data)
        return ResponseModel(data=new_item, message="实体创建并关联成功")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
