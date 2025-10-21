from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend.app.core.database import get_db
from backend.app.services.item_service import ItemService
from backend.app.core.schemas import ItemCreate, ItemUpdate, ItemResponse, ResponseModel

router = APIRouter()

@router.post("/", response_model=ItemResponse)
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    service = ItemService(db)
    try:
        return service.create(item)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/by_label/{label_code}", response_model=ResponseModel)
def get_items_by_label(label_code: str, db: Session = Depends(get_db)):
    service = ItemService(db)
    items = service.get_by_label(label_code)
    # 转换为字典格式
    items_data = []
    for item in items:
        items_data.append({
            "id": item.id,
            "item_name": item.item_name,
            "item_code": item.item_code,
            "parent_item_code": item.parent_item_code,
            "label_code": item.label_code,
            "description": item.description,
            "is_active": item.is_active,
            "created_at": item.created_at,
            "updated_at": item.updated_at,
            "synonyms": [{"id": s.id, "synonym": s.synonym, "item_code": s.item_code} for s in item.synonyms]
        })
    return ResponseModel(data=items_data)

@router.get("/children_of/{parent_item_code}", response_model=List[ItemResponse])
def get_item_children(parent_item_code: str, db: Session = Depends(get_db)):
    service = ItemService(db)
    return service.get_children(parent_item_code)

@router.get("/{item_code}", response_model=ItemResponse)
def get_item(item_code: str, db: Session = Depends(get_db)):
    service = ItemService(db)
    db_item = service.get_by_code(item_code, with_synonyms=True)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

@router.put("/{item_code}", response_model=ItemResponse)
def update_item(item_code: str, item: ItemUpdate, db: Session = Depends(get_db)):
    service = ItemService(db)
    db_item = service.update(item_code, item)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

@router.delete("/{item_code}", status_code=204)
def delete_item(item_code: str, db: Session = Depends(get_db)):
    service = ItemService(db)
    if not service.delete(item_code):
        raise HTTPException(status_code=404, detail="Item not found")
    return {"ok": True}
