"""
实体标签映射模型
"""
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from sqlalchemy.sql import func
from backend.app.core.database import Base

class EntityTagMapping(Base):
    """实体标签映射表"""
    __tablename__ = "entity_tag_mapping"
    
    id = Column(Integer, primary_key=True, autoincrement=True, index=True, comment="主键ID")
    entity_tag_name = Column(String(100), nullable=False, comment="实体标签名称")
    entity_value = Column(String(200), nullable=False, comment="实体值")
    entity_type = Column(String(50), comment="实体类型")
    description = Column(Text, comment="描述")
    is_active = Column(Boolean, nullable=False, default=True, comment="是否启用")
    created_at = Column(DateTime, default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), comment="更新时间")
    
    def __repr__(self):
        return f"<EntityTagMapping(id={self.id}, entity_tag_name='{self.entity_tag_name}', entity_value='{self.entity_value}')>"