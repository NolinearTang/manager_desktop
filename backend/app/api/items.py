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
    # Service层已经返回了包含parent_item_name的字典列表
    items_data = service.get_by_label(label_code)
    # 确保同义词格式正确，使用逗号连接
    for item in items_data:
        # 将同义词列表转换为逗号连接的字符串
        if item.get("synonyms"):
            item["synonyms_text"] = ", ".join(item["synonyms"])
        else:
            item["synonyms_text"] = ""
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
