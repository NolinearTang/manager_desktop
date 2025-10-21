from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend.app.core.database import get_db
from backend.app.services.label_service import LabelService
from backend.app.core.schemas import LabelCreate, LabelUpdate, LabelResponse, ResponseModel

router = APIRouter()

@router.post("/", response_model=LabelResponse)
def create_label(label: LabelCreate, db: Session = Depends(get_db)):
    service = LabelService(db)
    try:
        return service.create(label)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/by_system/{system_code}", response_model=List[LabelResponse])
def get_labels_by_system(system_code: str, db: Session = Depends(get_db)):
    service = LabelService(db)
    return service.get_by_system(system_code)

@router.get("/children_of/{parent_label_code}", response_model=List[LabelResponse])
def get_label_children(parent_label_code: str, db: Session = Depends(get_db)):
    service = LabelService(db)
    return service.get_children(parent_label_code)

@router.get("/tree", response_model=ResponseModel)
def get_label_tree_endpoint(label_type: str, db: Session = Depends(get_db)):
    """获取指定类型的标签树"""
    # Map the old label_type to the new system_code for frontend compatibility
    system_code_map = {
        "entity": "product_entity_system",
        "intent": "intent_system"
    }
    system_code = system_code_map.get(label_type)
    if not system_code:
        raise HTTPException(status_code=400, detail=f"Invalid label_type: {label_type}. Must be 'entity' or 'intent'.")
        
    service = LabelService(db)
    tree_data = service.get_label_tree(system_code)
    return ResponseModel(data=tree_data)

@router.get("/{label_code}", response_model=LabelResponse)
def get_label(label_code: str, db: Session = Depends(get_db)):
    service = LabelService(db)
    db_label = service.get_by_code(label_code)
    if db_label is None:
        raise HTTPException(status_code=404, detail="Label not found")
    return db_label

@router.put("/{label_code}", response_model=LabelResponse)
def update_label(label_code: str, label: LabelUpdate, db: Session = Depends(get_db)):
    service = LabelService(db)
    db_label = service.update(label_code, label)
    if db_label is None:
        raise HTTPException(status_code=404, detail="Label not found")
    return db_label

@router.delete("/{label_code}", status_code=204)
def delete_label(label_code: str, db: Session = Depends(get_db)):
    service = LabelService(db)
    if not service.delete(label_code):
        raise HTTPException(status_code=404, detail="Label not found")
    return {"ok": True}
