"""
规则管理服务
"""
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from typing import List, Optional
from backend.app.models.rule_management import RuleManagement
from backend.app.core.schemas import RuleCreate, RuleUpdate, PaginationParams
from backend.app.core.schemas import PaginatedResponse

class RuleService:
    """规则管理服务类"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_rules(
        self,
        label_id: Optional[int] = None,
        rule_category: Optional[str] = None,
        is_active: Optional[bool] = None,
        pagination: PaginationParams = None
    ) -> PaginatedResponse:
        """获取规则列表"""
        query = self.db.query(RuleManagement)
        
        # 应用过滤条件
        if label_id:
            query = query.filter(RuleManagement.target_label_id == label_id)
        if rule_category:
            query = query.filter(RuleManagement.rule_category == rule_category)
        if is_active is not None:
            query = query.filter(RuleManagement.is_active == is_active)
        
        # 排序
        query = query.order_by(RuleManagement.priority.desc(), RuleManagement.created_at)
        
        # 分页
        if pagination:
            total = query.count()
            items = query.offset((pagination.page - 1) * pagination.size).limit(pagination.size).all()
            pages = (total + pagination.size - 1) // pagination.size
            
            return PaginatedResponse(
                items=[{
                    "id": item.id,
                    "rule_name": item.rule_name,
                    "rule_category": item.rule_category,
                    "rule_expression": item.rule_expression,
                    "rule_sentence": item.rule_sentence,
                    "keywords": item.keywords,
                    "target_label_id": item.target_label_id,
                    "priority": item.priority,
                    "is_active": item.is_active,
                    "created_at": item.created_at,
                    "updated_at": item.updated_at
                } for item in items],
                total=total,
                page=pagination.page,
                size=pagination.size,
                pages=pages
            )
        else:
            items = query.all()
            return PaginatedResponse(
                items=[{
                    "id": item.id,
                    "rule_name": item.rule_name,
                    "rule_category": item.rule_category,
                    "rule_expression": item.rule_expression,
                    "rule_sentence": item.rule_sentence,
                    "keywords": item.keywords,
                    "target_label_id": item.target_label_id,
                    "priority": item.priority,
                    "is_active": item.is_active,
                    "created_at": item.created_at,
                    "updated_at": item.updated_at
                } for item in items],
                total=len(items),
                page=1,
                size=len(items),
                pages=1
            )
    
    def get_rule_by_id(self, rule_id: int) -> Optional[RuleManagement]:
        """根据ID获取规则"""
        return self.db.query(RuleManagement).filter(RuleManagement.id == rule_id).first()
    
    def create_rule(self, rule_data: RuleCreate) -> RuleManagement:
        """创建规则"""
        # 验证目标标签是否存在
        from backend.app.services.label_service import LabelService
        label_service = LabelService(self.db)
        target_label = label_service.get_label_by_id(rule_data.target_label_id)
        if not target_label:
            raise ValueError(f"目标标签ID {rule_data.target_label_id} 不存在")
        
        # 创建新规则
        db_rule = RuleManagement(**rule_data.dict())
        self.db.add(db_rule)
        self.db.commit()
        self.db.refresh(db_rule)
        return db_rule
    
    def update_rule(self, rule_id: int, rule_data: RuleUpdate) -> Optional[RuleManagement]:
        """更新规则"""
        db_rule = self.get_rule_by_id(rule_id)
        if not db_rule:
            return None
        
        # 验证目标标签是否存在
        if rule_data.target_label_id:
            from backend.app.services.label_service import LabelService
            label_service = LabelService(self.db)
            target_label = label_service.get_label_by_id(rule_data.target_label_id)
            if not target_label:
                raise ValueError(f"目标标签ID {rule_data.target_label_id} 不存在")
        
        # 更新规则
        update_data = rule_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_rule, field, value)
        
        self.db.commit()
        self.db.refresh(db_rule)
        return db_rule
    
    def delete_rule(self, rule_id: int) -> bool:
        """删除规则"""
        db_rule = self.get_rule_by_id(rule_id)
        if not db_rule:
            return False
        
        self.db.delete(db_rule)
        self.db.commit()
        return True
    
    def get_rules_by_label_code(self, label_code: str) -> List[RuleManagement]:
        """根据标签编码获取规则"""
        from backend.app.models.label_system import LabelSystem
        return self.db.query(RuleManagement).join(
            LabelSystem, RuleManagement.target_label_id == LabelSystem.id
        ).filter(
            and_(
                LabelSystem.label_code == label_code,
                RuleManagement.is_active == True
            )
        ).order_by(RuleManagement.priority.desc()).all()
    
    def match_rules(self, text: str, label_code: Optional[str] = None) -> List[dict]:
        """匹配规则"""
        import re
        from backend.app.services.entity_tag_service import EntityTagService
        
        # 获取规则
        if label_code:
            rules = self.get_rules_by_label_code(label_code)
        else:
            rules = self.db.query(RuleManagement).filter(
                RuleManagement.is_active == True
            ).all()
        
        matched_rules = []
        entity_service = EntityTagService(self.db)
        
        for rule in rules:
            confidence = 0.0
            matched_expression = ""
            
            if rule.rule_category == "expression":
                # 表达式匹配：处理实体标签引用
                expression = rule.rule_expression
                # 提取实体标签引用 {实体标签名}
                entity_refs = re.findall(r'\{([^}]+)\}', expression)
                
                if entity_refs:
                    # 检查是否匹配实体标签
                    for entity_ref in entity_refs:
                        entities = entity_service.get_entities_by_tag_name(entity_ref)
                        for entity in entities:
                            if entity.entity_value.lower() in text.lower():
                                confidence = 0.9
                                matched_expression = expression.replace(f"{{{entity_ref}}}", entity.entity_value)
                                break
                        if confidence > 0:
                            break
                else:
                    # 直接文本匹配
                    if rule.rule_expression.lower() in text.lower():
                        confidence = 0.8
                        matched_expression = rule.rule_expression
            
            elif rule.rule_category == "sentence":
                # 表达句匹配
                if rule.rule_sentence and rule.rule_sentence.lower() in text.lower():
                    confidence = 0.7
                    matched_expression = rule.rule_sentence
            
            elif rule.rule_category == "keyword":
                # 关键词匹配
                if rule.keywords:
                    keywords = [kw.strip() for kw in rule.keywords.split(',')]
                    matched_keywords = [kw for kw in keywords if kw.lower() in text.lower()]
                    if matched_keywords:
                        confidence = 0.6
                        matched_expression = ', '.join(matched_keywords)
            
            if confidence > 0:
                matched_rules.append({
                    "rule_id": rule.id,
                    "rule_name": rule.rule_name,
                    "rule_category": rule.rule_category,
                    "matched_expression": matched_expression,
                    "confidence": confidence
                })
        
        # 按置信度排序
        matched_rules.sort(key=lambda x: x["confidence"], reverse=True)
        return matched_rules