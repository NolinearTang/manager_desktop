from sqlalchemy import Column, String, Text, DateTime, Integer, INT, ForeignKey
from sqlalchemy.sql import func
from backend.app.core.database import Base

class Label(Base):
    __tablename__ = "labels"
    id = Column(Integer, primary_key=True)
    label_name = Column(String(100), nullable=False)
    label_code = Column(String(50), nullable=False, unique=True)
    parent_label_code = Column(String(50), ForeignKey("labels.label_code"))
    system_code = Column(String(50), ForeignKey("tag_systems.system_code"), nullable=False)
    level = Column(INT, nullable=False, default=1)
    description = Column(Text)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
