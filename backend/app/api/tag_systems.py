from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend.app.core.database import get_db
from backend.app.services.tag_system_service import TagSystemService
from backend.app.core.schemas import TagSystemCreate, TagSystemUpdate, TagSystemResponse

router = APIRouter()

@router.post("/", response_model=TagSystemResponse)
def create_tag_system(system: TagSystemCreate, db: Session = Depends(get_db)):
    service = TagSystemService(db)
    try:
        return service.create(system)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[TagSystemResponse])
def get_all_tag_systems(db: Session = Depends(get_db)):
    service = TagSystemService(db)
    return service.get_all()

@router.get("/{system_code}", response_model=TagSystemResponse)
def get_tag_system(system_code: str, db: Session = Depends(get_db)):
    service = TagSystemService(db)
    db_system = service.get_by_code(system_code)
    if db_system is None:
        raise HTTPException(status_code=404, detail="TagSystem not found")
    return db_system

@router.put("/{system_code}", response_model=TagSystemResponse)
def update_tag_system(system_code: str, system: TagSystemUpdate, db: Session = Depends(get_db)):
    service = TagSystemService(db)
    db_system = service.update(system_code, system)
    if db_system is None:
        raise HTTPException(status_code=404, detail="TagSystem not found")
    return db_system

@router.delete("/{system_code}", status_code=204)
def delete_tag_system(system_code: str, db: Session = Depends(get_db)):
    service = TagSystemService(db)
    if not service.delete(system_code):
        raise HTTPException(status_code=404, detail="TagSystem not found")
    return {"ok": True}
