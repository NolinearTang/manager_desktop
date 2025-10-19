"""
规则管理API
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from backend.app.core.database import get_db
from backend.app.core.schemas import (
    RuleCreate, RuleUpdate, RuleResponse, 
    ResponseModel, PaginationParams
)
from backend.app.services.rule_service import RuleService

router = APIRouter()

@router.get("/", response_model=ResponseModel)
async def get_rules(
    label_id: Optional[int] = Query(None, description="标签ID"),
    rule_category: Optional[str] = Query(None, description="规则类别"),
    is_active: Optional[bool] = Query(None, description="是否启用"),
    page: int = Query(1, ge=1, description="页码"),
    size: int = Query(20, ge=1, le=100, description="每页数量"),
    db: Session = Depends(get_db)
):
    """获取规则列表"""
    try:
        rule_service = RuleService(db)
        pagination = PaginationParams(page=page, size=size)
        result = rule_service.get_rules(
            label_id=label_id,
            rule_category=rule_category,
            is_active=is_active,
            pagination=pagination
        )
        return ResponseModel(data=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{rule_id}", response_model=ResponseModel)
async def get_rule(
    rule_id: int,
    db: Session = Depends(get_db)
):
    """根据ID获取规则"""
    try:
        rule_service = RuleService(db)
        rule = rule_service.get_rule_by_id(rule_id)
        if not rule:
            raise HTTPException(status_code=404, detail="规则不存在")
        return ResponseModel(data=rule)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/", response_model=ResponseModel)
async def create_rule(
    rule_data: RuleCreate,
    db: Session = Depends(get_db)
):
    """创建规则"""
    try:
        rule_service = RuleService(db)
        rule = rule_service.create_rule(rule_data)
        return ResponseModel(data=rule, message="规则创建成功")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{rule_id}", response_model=ResponseModel)
async def update_rule(
    rule_id: int,
    rule_data: RuleUpdate,
    db: Session = Depends(get_db)
):
    """更新规则"""
    try:
        rule_service = RuleService(db)
        rule = rule_service.update_rule(rule_id, rule_data)
        if not rule:
            raise HTTPException(status_code=404, detail="规则不存在")
        return ResponseModel(data=rule, message="规则更新成功")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{rule_id}", response_model=ResponseModel)
async def delete_rule(
    rule_id: int,
    db: Session = Depends(get_db)
):
    """删除规则"""
    try:
        rule_service = RuleService(db)
        success = rule_service.delete_rule(rule_id)
        if not success:
            raise HTTPException(status_code=404, detail="规则不存在")
        return ResponseModel(message="规则删除成功")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/by_label_code/{label_code}", response_model=ResponseModel)
async def get_rules_by_label_code(
    label_code: str,
    db: Session = Depends(get_db)
):
    """根据标签编码获取规则"""
    try:
        rule_service = RuleService(db)
        rules = rule_service.get_rules_by_label_code(label_code)
        # 转换为字典格式
        rules_data = []
        for rule in rules:
            rules_data.append({
                "id": rule.id,
                "rule_name": rule.rule_name,
                "rule_category": rule.rule_category,
                "rule_expression": rule.rule_expression,
                "rule_sentence": rule.rule_sentence,
                "keywords": rule.keywords,
                "target_label_id": rule.target_label_id,
                "priority": rule.priority,
                "is_active": rule.is_active,
                "created_at": rule.created_at,
                "updated_at": rule.updated_at
            })
        return ResponseModel(data=rules_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))