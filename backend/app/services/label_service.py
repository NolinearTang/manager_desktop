"""
标签管理服务
"""
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from typing import List, Optional
from backend.app.models.label_system import LabelSystem
from backend.app.models.item_data import ItemData
from backend.app.models.label_item_relation import LabelItemRelation
from backend.app.core.schemas import LabelCreate, LabelUpdate, PaginationParams, ItemDataCreate
from backend.app.core.schemas import PaginatedResponse

class LabelService:
    """标签管理服务类"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_labels(
        self, 
        parent_code: Optional[str] = None,
        label_type: Optional[str] = None,
        level: Optional[int] = None,
        pagination: PaginationParams = None
    ) -> PaginatedResponse:
        """获取标签列表"""
        query = self.db.query(LabelSystem)
        
        # 应用过滤条件
        if parent_code:
            query = query.filter(LabelSystem.parent_label_code == parent_code)
        if label_type:
            query = query.filter(LabelSystem.label_type == label_type)
        if level:
            query = query.filter(LabelSystem.level == level)
        
        # 只返回启用的标签
        query = query.filter(LabelSystem.is_active == True)
        
        # 排序
        query = query.order_by(LabelSystem.sort_order, LabelSystem.created_at)
        
        # 分页
        if pagination:
            total = query.count()
            items = query.offset((pagination.page - 1) * pagination.size).limit(pagination.size).all()
            pages = (total + pagination.size - 1) // pagination.size
            
            return PaginatedResponse(
                items=items,
                total=total,
                page=pagination.page,
                size=pagination.size,
                pages=pages
            )
        else:
            items = query.all()
            return PaginatedResponse(
                items=items,
                total=len(items),
                page=1,
                size=len(items),
                pages=1
            )
    
    def get_label_by_id(self, label_id: int) -> Optional[LabelSystem]:
        """根据ID获取标签"""
        return self.db.query(LabelSystem).filter(LabelSystem.id == label_id).first()
    
    def get_label_by_code(self, label_code: str) -> Optional[LabelSystem]:
        """根据编码获取标签"""
        return self.db.query(LabelSystem).filter(LabelSystem.label_code == label_code).first()
    
    def create_label(self, label_data: LabelCreate) -> LabelSystem:
        """创建标签"""
        # 检查标签编码是否已存在
        existing_label = self.get_label_by_code(label_data.label_code)
        if existing_label:
            raise ValueError(f"标签编码 {label_data.label_code} 已存在")
        
        # 创建新标签
        db_label = LabelSystem(**label_data.dict())
        self.db.add(db_label)
        self.db.commit()
        self.db.refresh(db_label)
        return db_label
    
    def update_label(self, label_id: int, label_data: LabelUpdate) -> Optional[LabelSystem]:
        """更新标签"""
        db_label = self.get_label_by_id(label_id)
        if not db_label:
            return None
        
        # 检查标签编码是否冲突
        if label_data.label_code and label_data.label_code != db_label.label_code:
            existing_label = self.get_label_by_code(label_data.label_code)
            if existing_label:
                raise ValueError(f"标签编码 {label_data.label_code} 已存在")
        
        # 更新标签
        update_data = label_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_label, field, value)
        
        self.db.commit()
        self.db.refresh(db_label)
        return db_label
    
    def delete_label(self, label_id: int) -> bool:
        """删除标签（软删除）"""
        db_label = self.get_label_by_id(label_id)
        if not db_label:
            return False
        
        # 软删除：设置为不启用
        db_label.is_active = False
        self.db.commit()
        return True
    
    def get_children_labels(self, parent_code: str) -> List[LabelSystem]:
        """获取子标签列表"""
        return self.db.query(LabelSystem).filter(
            and_(
                LabelSystem.parent_label_code == parent_code,
                LabelSystem.is_active == True
            )
        ).order_by(LabelSystem.sort_order).all()
    
    def get_label_tree(self, root_code: Optional[str] = None, label_type: Optional[str] = None) -> List[dict]:
        """获取标签树结构"""
        
        # Base query
        query = self.db.query(LabelSystem).filter(LabelSystem.is_active == True)
        
        # Filter by label_type if provided
        if label_type:
            query = query.filter(LabelSystem.label_type == label_type)

        # Filter for root labels
        if root_code:
            root_labels_query = query.filter(LabelSystem.parent_label_code == root_code)
        else:
            root_labels_query = query.filter(LabelSystem.parent_label_code.is_(None))
        
        root_labels = root_labels_query.order_by(LabelSystem.sort_order).all()
        
        def build_tree(labels):
            result = []
            for label in labels:
                # When getting children, we should respect the original label_type filter
                children_query = self.db.query(LabelSystem).filter(
                    and_(
                        LabelSystem.parent_label_code == label.label_code,
                        LabelSystem.is_active == True
                    )
                )
                if label_type:
                    children_query = children_query.filter(LabelSystem.label_type == label_type)
                
                children = children_query.order_by(LabelSystem.sort_order).all()

                label_dict = {
                    "id": label.id,
                    "label_name": label.label_name,
                    "label_code": label.label_code,
                    "parent_label_name": label.parent_label_name,
                    "parent_label_code": label.parent_label_code,
                    "label_type": label.label_type,
                    "level": label.level,
                    "description": label.description,
                    "is_active": label.is_active,
                    "sort_order": label.sort_order,
                    "children": build_tree(children) if children else []
                }
                result.append(label_dict)
            return result
        
        return build_tree(root_labels)

    def get_items_by_label_code(self, label_code: str) -> List[ItemData]:
        """根据标签编码获取关联的数据项列表"""
        items = self.db.query(ItemData).join(
            LabelItemRelation
        ).join(
            LabelSystem
        ).filter(
            LabelSystem.label_code == label_code,
            ItemData.is_active == True
        ).all()
        return items

    def add_item_to_label(self, label_code: str, item_data: ItemDataCreate) -> ItemData:
        """向指定标签添加一个新的数据项"""
        # 查找标签
        label = self.get_label_by_code(label_code)
        if not label:
            raise ValueError(f"标签编码 '{label_code}' 不存在")

        # 创建数据项
        # 检查数据项编码是否已存在
        if item_data.item_code:
            existing_item = self.db.query(ItemData).filter(
                ItemData.item_code == item_data.item_code
            ).first()
            if existing_item:
                raise ValueError(f"数据项编码 {item_data.item_code} 已存在")
        
        new_item = ItemData(**item_data.dict())
        self.db.add(new_item)
        self.db.flush()  # Flush to get the new_item.id

        # 创建关联关系
        relation = LabelItemRelation(
            label_id=label.id,
            item_id=new_item.id,
            relation_type='belongs_to'
        )
        self.db.add(relation)
        
        self.db.commit()
        self.db.refresh(new_item)
        return new_item
