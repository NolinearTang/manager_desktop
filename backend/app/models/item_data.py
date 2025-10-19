"""
数据项模型
"""
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.app.core.database import Base

class ItemData(Base):
    """数据信息表"""
    __tablename__ = "item_data"
    
    id = Column(Integer, primary_key=True, autoincrement=True, index=True, comment="主键ID")
    item_name = Column(String(200), nullable=False, comment="数据项名称")
    item_synonym = Column(Text, comment="同义词，JSON格式存储")
    item_code = Column(String(100), comment="数据项编码")
    item_type = Column(String(50), comment="数据项类型")
    description = Column(Text, comment="数据项描述")
    item_metadata = Column(JSON, comment="元数据，JSON格式存储")
    is_active = Column(Boolean, nullable=False, default=True, comment="是否启用")
    created_at = Column(DateTime, default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), comment="更新时间")
    
    # 关联关系
    label_item_relations = relationship("LabelItemRelation", back_populates="item", lazy="dynamic")
    
    def __repr__(self):
        return f"<ItemData(id={self.id}, item_name='{self.item_name}', item_type='{self.item_type}')>"