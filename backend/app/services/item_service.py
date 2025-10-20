from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from backend.app.models import Item, ItemSynonym
from backend.app.core.schemas import ItemCreate, ItemUpdate

class ItemService:
    def __init__(self, db: Session):
        self.db = db

    def get_by_code(self, item_code: str, with_synonyms: bool = False) -> Optional[Item]:
        query = self.db.query(Item)
        if with_synonyms:
            query = query.options(joinedload(Item.synonyms))
        return query.filter(Item.item_code == item_code).first()

    def get_by_label(self, label_code: str) -> List[Item]:
        return self.db.query(Item).filter(Item.label_code == label_code).all()

    def get_children(self, parent_item_code: str) -> List[Item]:
        return self.db.query(Item).filter(Item.parent_item_code == parent_item_code).all()

    def create(self, item_create: ItemCreate) -> Item:
        if self.get_by_code(item_create.item_code):
            raise ValueError(f"Item with code {item_create.item_code} already exists.")
        
        item_dict = item_create.dict()
        synonyms_list = item_dict.pop('synonyms', [])
        db_item = Item(**item_dict)

        if synonyms_list:
            db_item.synonyms = [ItemSynonym(synonym=s) for s in synonyms_list]

        self.db.add(db_item)
        self.db.commit()
        self.db.refresh(db_item)
        return db_item

    def update(self, item_code: str, item_update: ItemUpdate) -> Optional[Item]:
        db_item = self.get_by_code(item_code)
        if not db_item:
            return None
        
        update_data = item_update.dict(exclude_unset=True)
        synonyms_list = update_data.pop('synonyms', None)

        for field, value in update_data.items():
            setattr(db_item, field, value)
            
        if synonyms_list is not None:
            db_item.synonyms = [ItemSynonym(synonym=s) for s in synonyms_list]

        self.db.commit()
        self.db.refresh(db_item)
        return db_item

    def delete(self, item_code: str) -> bool:
        db_item = self.get_by_code(item_code)
        if not db_item:
            return False
        
        db_item.is_active = False
        self.db.commit()
        return True

    def extract_entities_from_text(self, text: str) -> List[dict]:
        """
        Extracts entities from text by matching against item names and synonyms.
        """
        # For performance, it's better to query only relevant item types (e.g., products, specs)
        # For now, we query all items.
        all_items = self.db.query(Item).options(joinedload(Item.synonyms)).filter(Item.is_active == True).all()
        found_entities = []
        text_lower = text.lower()

        for item in all_items:
            # Check item name
            item_name_lower = item.item_name.lower()
            if item_name_lower in text_lower:
                start_pos = text_lower.find(item_name_lower)
                found_entities.append({
                    "entity_type": item.label_code, # Use label_code as entity_type
                    "entity_value": item.item_name,
                    "start_pos": start_pos,
                    "end_pos": start_pos + len(item.item_name)
                })

            # Check synonyms
            for synonym in item.synonyms:
                synonym_lower = synonym.synonym.lower()
                if synonym_lower in text_lower:
                    start_pos = text_lower.find(synonym_lower)
                    found_entities.append({
                        "entity_type": item.label_code,
                        "entity_value": synonym.synonym, # Report the synonym that was found
                        "start_pos": start_pos,
                        "end_pos": start_pos + len(synonym.synonym)
                    })
        
        # Remove duplicates if an item and its synonym are both found
        # A more robust implementation would handle overlapping entities
        # For now, we return all findings.
        return found_entities
