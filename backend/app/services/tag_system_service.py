from sqlalchemy.orm import Session
from typing import List, Optional
from backend.app.models import TagSystem
from backend.app.core.schemas import TagSystemCreate, TagSystemUpdate

class TagSystemService:
    def __init__(self, db: Session):
        self.db = db

    def get_by_code(self, system_code: str) -> Optional[TagSystem]:
        return self.db.query(TagSystem).filter(TagSystem.system_code == system_code).first()

    def get_all(self) -> List[TagSystem]:
        return self.db.query(TagSystem).all()

    def create(self, system_create: TagSystemCreate) -> TagSystem:
        if self.get_by_code(system_create.system_code):
            raise ValueError(f"System with code {system_create.system_code} already exists.")
        db_system = TagSystem(**system_create.dict())
        self.db.add(db_system)
        self.db.commit()
        self.db.refresh(db_system)
        return db_system

    def update(self, system_code: str, system_update: TagSystemUpdate) -> Optional[TagSystem]:
        db_system = self.get_by_code(system_code)
        if not db_system:
            return None
        update_data = system_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_system, field, value)
        self.db.commit()
        self.db.refresh(db_system)
        return db_system

    def delete(self, system_code: str) -> bool:
        db_system = self.get_by_code(system_code)
        if not db_system:
            return False
        self.db.delete(db_system)
        self.db.commit()
        return True
