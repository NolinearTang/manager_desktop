from sqlalchemy.orm import Session
from typing import List, Optional
from backend.app.models import Label
from backend.app.core.schemas import LabelCreate, LabelUpdate

class LabelService:
    def __init__(self, db: Session):
        self.db = db

    def get_by_code(self, label_code: str) -> Optional[Label]:
        return self.db.query(Label).filter(Label.label_code == label_code).first()

    def get_by_system(self, system_code: str) -> List[Label]:
        return self.db.query(Label).filter(Label.system_code == system_code).all()

    def get_children(self, parent_label_code: str) -> List[Label]:
        return self.db.query(Label).filter(Label.parent_label_code == parent_label_code).all()

    def create(self, label_create: LabelCreate) -> Label:
        if self.get_by_code(label_create.label_code):
            raise ValueError(f"Label with code {label_create.label_code} already exists.")
        db_label = Label(**label_create.dict())
        self.db.add(db_label)
        self.db.commit()
        self.db.refresh(db_label)
        return db_label

    def update(self, label_code: str, label_update: LabelUpdate) -> Optional[Label]:
        db_label = self.get_by_code(label_code)
        if not db_label:
            return None
        update_data = label_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_label, field, value)
        self.db.commit()
        self.db.refresh(db_label)
        return db_label

    def delete(self, label_code: str) -> bool:
        db_label = self.get_by_code(label_code)
        if not db_label:
            return False
        self.db.delete(db_label)
        self.db.commit()
        return True

    def get_label_tree(self, system_code: str) -> List[dict]:
        """根据 system_code 在内存中构建标签树"""
        all_labels_in_system = self.get_by_system(system_code)
        
        labels_by_code = {label.label_code: label for label in all_labels_in_system}
        children_map = {}
        root_labels = []

        for label in all_labels_in_system:
            label_dict = {
                "id": label.id,
                "label_name": label.label_name,
                "label_code": label.label_code,
                "parent_label_code": label.parent_label_code,
                "system_code": label.system_code,
                "level": label.level,
                "description": label.description,
                "children": []
            }
            
            if label.parent_label_code:
                if label.parent_label_code not in children_map:
                    children_map[label.parent_label_code] = []
                children_map[label.parent_label_code].append(label_dict)
            else:
                root_labels.append(label_dict)

        def attach_children(node):
            if node["label_code"] in children_map:
                # Sort children, e.g., by name
                node["children"] = sorted(children_map[node["label_code"]], key=lambda x: x["label_name"])
                for child in node["children"]:
                    attach_children(child)

        for root_node in root_labels:
            attach_children(root_node)
            
        return sorted(root_labels, key=lambda x: x["label_name"])
