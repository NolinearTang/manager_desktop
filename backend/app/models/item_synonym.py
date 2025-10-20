from sqlalchemy import Column, String, DateTime, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.app.core.database import Base

class ItemSynonym(Base):
    __tablename__ = "item_synonyms"
    id = Column(Integer, primary_key=True)
    item_code = Column(String(100), ForeignKey("items.item_code", ondelete="CASCADE"), nullable=False)
    synonym = Column(String(200), nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    item = relationship("Item", back_populates="synonyms")
