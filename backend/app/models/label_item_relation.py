"""
标签数据项关联模型
"""
from sqlalchemy import Column, Integer, Boolean, DateTime, Enum, ForeignKey, DECIMAL
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from backend.app.core.database import Base

class LabelItemRelation(Base):
    """标签体系关联表"""
    __tablename__ = "label_item_relation"
    
    id = Column(Integer, primary_key=True, autoincrement=True, index=True, comment="主键ID")
    label_id = Column(Integer, ForeignKey('label_system.id'), nullable=False, comment="标签ID")
    item_id = Column(Integer, ForeignKey('item_data.id'), nullable=False, comment="数据项ID")
    relation_type = Column(Enum('belongs_to', 'synonym', 'related'), nullable=False, default='belongs_to', comment="关联类型")
    weight = Column(DECIMAL(3, 2), default=1.00, comment="权重")
    is_active = Column(Boolean, nullable=False, default=True, comment="是否启用")
    created_at = Column(DateTime, default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), comment="更新时间")
    
    # 关联关系
    label = relationship("LabelSystem", back_populates="label_item_relations")
    item = relationship("ItemData", back_populates="label_item_relations")
    
    def __repr__(self):
        return f"<LabelItemRelation(id={self.id}, label_id={self.label_id}, item_id={self.item_id})>"