"""
数据项管理服务
"""
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from typing import List, Optional
from backend.app.models.item_data import ItemData
from backend.app.core.schemas import ItemDataCreate, ItemDataUpdate, PaginationParams
from backend.app.core.schemas import PaginatedResponse

class ItemService:
    """数据项管理服务类"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_items(
        self,
        item_name: Optional[str] = None,
        item_type: Optional[str] = None,
        label_id: Optional[int] = None,
        pagination: PaginationParams = None
    ) -> PaginatedResponse:
        """获取数据项列表"""
        query = self.db.query(ItemData)
        
        # 应用过滤条件
        if item_name:
            query = query.filter(ItemData.item_name.contains(item_name))
        if item_type:
            query = query.filter(ItemData.item_type == item_type)
        if label_id:
            # 通过关联表过滤
            query = query.join(ItemData.label_item_relations).filter(
                ItemData.label_item_relations.any(label_id=label_id)
            )
        
        # 只返回启用的数据项
        query = query.filter(ItemData.is_active == True)
        
        # 排序
        query = query.order_by(ItemData.item_name)
        
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
    
    def get_item_by_id(self, item_id: int) -> Optional[ItemData]:
        """根据ID获取数据项"""
        return self.db.query(ItemData).filter(ItemData.id == item_id).first()
    
    def create_item(self, item_data: ItemDataCreate) -> ItemData:
        """创建数据项"""
        # 检查数据项编码是否已存在
        if item_data.item_code:
            existing_item = self.db.query(ItemData).filter(
                ItemData.item_code == item_data.item_code
            ).first()
            if existing_item:
                raise ValueError(f"数据项编码 {item_data.item_code} 已存在")
        
        # 创建新数据项
        db_item = ItemData(**item_data.dict())
        self.db.add(db_item)
        self.db.commit()
        self.db.refresh(db_item)
        return db_item
    
    def update_item(self, item_id: int, item_data: ItemDataUpdate) -> Optional[ItemData]:
        """更新数据项"""
        db_item = self.get_item_by_id(item_id)
        if not db_item:
            return None
        
        # 检查数据项编码是否冲突
        if item_data.item_code and item_data.item_code != db_item.item_code:
            existing_item = self.db.query(ItemData).filter(
                ItemData.item_code == item_data.item_code
            ).first()
            if existing_item:
                raise ValueError(f"数据项编码 {item_data.item_code} 已存在")
        
        # 更新数据项
        update_data = item_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_item, field, value)
        
        self.db.commit()
        self.db.refresh(db_item)
        return db_item
    
    def delete_item(self, item_id: int) -> bool:
        """删除数据项（软删除）"""
        db_item = self.get_item_by_id(item_id)
        if not db_item:
            return False
        
        # 软删除：设置为不启用
        db_item.is_active = False
        self.db.commit()
        return True