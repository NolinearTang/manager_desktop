"""
规则管理模型
"""
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Enum, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from backend.app.core.database import Base

class RuleManagement(Base):
    """规则管理表"""
    __tablename__ = "rule_management"
    
    id = Column(Integer, primary_key=True, autoincrement=True, index=True, comment="主键ID")
    rule_name = Column(String(200), nullable=False, comment="规则名称")
    rule_category = Column(Enum('expression', 'sentence', 'keyword'), nullable=False, comment="规则类别")
    rule_expression = Column(Text, nullable=False, comment="规则表达式")
    rule_sentence = Column(Text, comment="规则表达句")
    keywords = Column(Text, comment="关键词，逗号分隔")
    target_label_id = Column(Integer, ForeignKey('label_system.id'), nullable=False, comment="目标标签ID")
    priority = Column(Integer, default=0, comment="优先级")
    is_active = Column(Boolean, nullable=False, default=True, comment="是否启用")
    created_at = Column(DateTime, default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), comment="更新时间")
    
    # 关联关系
    target_label = relationship("LabelSystem", back_populates="rules")
    
    def __repr__(self):
        return f"<RuleManagement(id={self.id}, rule_name='{self.rule_name}', rule_category='{self.rule_category}')>"