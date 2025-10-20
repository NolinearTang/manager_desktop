from sqlalchemy import Column, String, Text, DateTime, Integer
from sqlalchemy.sql import func
from backend.app.core.database import Base

class TagSystem(Base):
    __tablename__ = "tag_systems"
    id = Column(Integer, primary_key=True)
    system_name = Column(String(100), nullable=False, unique=True)
    system_code = Column(String(50), nullable=False, unique=True)
    system_type = Column(String(50), nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
