from sqlalchemy import Column, String, Text, DateTime, Integer, BOOLEAN, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.app.core.database import Base

class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True)
    item_name = Column(String(200), nullable=False)
    item_code = Column(String(100), nullable=False, unique=True)
    parent_item_code = Column(String(100), ForeignKey("items.item_code"))
    label_code = Column(String(50), ForeignKey("labels.label_code"), nullable=False)
    description = Column(Text)
    is_active = Column(BOOLEAN, nullable=False, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    synonyms = relationship("ItemSynonym", back_populates="item", cascade="all, delete-orphan")
