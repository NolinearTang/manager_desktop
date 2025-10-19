"""
实体标签管理服务
"""
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from typing import List, Optional
from backend.app.models.entity_tag_mapping import EntityTagMapping
from backend.app.core.schemas import EntityTagCreate, EntityTagUpdate, PaginationParams
from backend.app.core.schemas import PaginatedResponse

class EntityTagService:
    """实体标签管理服务类"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_entities(
        self,
        entity_tag_name: Optional[str] = None,
        entity_type: Optional[str] = None,
        pagination: PaginationParams = None
    ) -> PaginatedResponse:
        """获取实体标签列表"""
        query = self.db.query(EntityTagMapping)
        
        # 应用过滤条件
        if entity_tag_name:
            query = query.filter(EntityTagMapping.entity_tag_name == entity_tag_name)
        if entity_type:
            query = query.filter(EntityTagMapping.entity_type == entity_type)
        
        # 只返回启用的实体标签
        query = query.filter(EntityTagMapping.is_active == True)
        
        # 排序
        query = query.order_by(EntityTagMapping.entity_tag_name, EntityTagMapping.entity_value)
        
        # 分页
        if pagination:
            total = query.count()
            items = query.offset((pagination.page - 1) * pagination.size).limit(pagination.size).all()
            pages = (total + pagination.size - 1) // pagination.size
            
            return PaginatedResponse(
                items=[{
                    "id": item.id,
                    "entity_tag_name": item.entity_tag_name,
                    "entity_value": item.entity_value,
                    "entity_type": item.entity_type,
                    "description": item.description,
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
                    "entity_tag_name": item.entity_tag_name,
                    "entity_value": item.entity_value,
                    "entity_type": item.entity_type,
                    "description": item.description,
                    "is_active": item.is_active,
                    "created_at": item.created_at,
                    "updated_at": item.updated_at
                } for item in items],
                total=len(items),
                page=1,
                size=len(items),
                pages=1
            )
    
    def get_entity_by_id(self, entity_id: int) -> Optional[EntityTagMapping]:
        """根据ID获取实体标签"""
        return self.db.query(EntityTagMapping).filter(EntityTagMapping.id == entity_id).first()
    
    def get_entities_by_tag_name(self, entity_tag_name: str) -> List[EntityTagMapping]:
        """根据实体标签名称获取实体列表"""
        return self.db.query(EntityTagMapping).filter(
            and_(
                EntityTagMapping.entity_tag_name == entity_tag_name,
                EntityTagMapping.is_active == True
            )
        ).all()
    
    def create_entity(self, entity_data: EntityTagCreate) -> EntityTagMapping:
        """创建实体标签"""
        # 检查实体标签是否已存在
        existing_entity = self.db.query(EntityTagMapping).filter(
            and_(
                EntityTagMapping.entity_tag_name == entity_data.entity_tag_name,
                EntityTagMapping.entity_value == entity_data.entity_value
            )
        ).first()
        
        if existing_entity:
            raise ValueError(f"实体标签 {entity_data.entity_tag_name}:{entity_data.entity_value} 已存在")
        
        # 创建新实体标签
        db_entity = EntityTagMapping(**entity_data.dict())
        self.db.add(db_entity)
        self.db.commit()
        self.db.refresh(db_entity)
        return db_entity
    
    def update_entity(self, entity_id: int, entity_data: EntityTagUpdate) -> Optional[EntityTagMapping]:
        """更新实体标签"""
        db_entity = self.get_entity_by_id(entity_id)
        if not db_entity:
            return None
        
        # 检查实体标签是否冲突
        if entity_data.entity_tag_name and entity_data.entity_value:
            existing_entity = self.db.query(EntityTagMapping).filter(
                and_(
                    EntityTagMapping.entity_tag_name == entity_data.entity_tag_name,
                    EntityTagMapping.entity_value == entity_data.entity_value,
                    EntityTagMapping.id != entity_id
                )
            ).first()
            
            if existing_entity:
                raise ValueError(f"实体标签 {entity_data.entity_tag_name}:{entity_data.entity_value} 已存在")
        
        # 更新实体标签
        update_data = entity_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_entity, field, value)
        
        self.db.commit()
        self.db.refresh(db_entity)
        return db_entity
    
    def delete_entity(self, entity_id: int) -> bool:
        """删除实体标签（软删除）"""
        db_entity = self.get_entity_by_id(entity_id)
        if not db_entity:
            return False
        
        # 软删除：设置为不启用
        db_entity.is_active = False
        self.db.commit()
        return True
    
    def get_entity_tag_names(self) -> List[str]:
        """获取所有实体标签名称"""
        result = self.db.query(EntityTagMapping.entity_tag_name).filter(
            EntityTagMapping.is_active == True
        ).distinct().all()
        return [row[0] for row in result]
    
    def extract_entities_from_text(self, text: str) -> List[dict]:
        """从文本中提取实体"""
        import re
        
        extracted_entities = []
        entities = self.db.query(EntityTagMapping).filter(
            EntityTagMapping.is_active == True
        ).all()
        
        for entity in entities:
            # 检查实体值是否在文本中
            if entity.entity_value.lower() in text.lower():
                # 找到实体在文本中的位置
                start_pos = text.lower().find(entity.entity_value.lower())
                if start_pos != -1:
                    end_pos = start_pos + len(entity.entity_value)
                    extracted_entities.append({
                        "entity_type": entity.entity_tag_name,
                        "entity_value": entity.entity_value,
                        "start_pos": start_pos,
                        "end_pos": end_pos,
                        "confidence": 1.0
                    })
        
        return extracted_entities