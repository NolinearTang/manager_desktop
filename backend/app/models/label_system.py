"""
标签体系模型
"""
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from backend.app.core.database import Base

class LabelSystem(Base):
    """标签体系表"""
    __tablename__ = "label_system"
    
    id = Column(Integer, primary_key=True, autoincrement=True, index=True, comment="主键ID")
    label_name = Column(String(100), nullable=False, comment="标签名称")
    label_code = Column(String(50), nullable=False, unique=True, comment="标签编码")
    parent_label_name = Column(String(100), comment="父级标签名称")
    parent_label_code = Column(String(50), comment="父级标签编码")
    label_type = Column(Enum('intent', 'entity', 'category'), nullable=False, default='intent', comment="标签类型")
    level = Column(Integer, nullable=False, default=1, comment="标签层级")
    description = Column(Text, comment="标签描述")
    is_active = Column(Boolean, nullable=False, default=True, comment="是否启用")
    sort_order = Column(Integer, default=0, comment="排序顺序")
    created_at = Column(DateTime, default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), comment="更新时间")
    
    # 关联关系
    rules = relationship("RuleManagement", back_populates="target_label", lazy="dynamic")
    label_item_relations = relationship("LabelItemRelation", back_populates="label", lazy="dynamic")
    
    def __repr__(self):
        return f"<LabelSystem(id={self.id}, label_name='{self.label_name}', label_code='{self.label_code}')>"