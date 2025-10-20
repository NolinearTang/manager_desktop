from sqlalchemy import Column, String, Text, DateTime, Integer, BOOLEAN, ForeignKey
from sqlalchemy.sql import func
from backend.app.core.database import Base

class IntentRule(Base):
    __tablename__ = "intent_rules"
    id = Column(Integer, primary_key=True)
    rule_code = Column(String(50), nullable=False, unique=True)
    rule_type = Column(String(50), nullable=False)
    rule_entity = Column(Text, nullable=False)
    label_code = Column(String(50), ForeignKey("labels.label_code", ondelete="CASCADE"), nullable=False)
    is_active = Column(BOOLEAN, nullable=False, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
