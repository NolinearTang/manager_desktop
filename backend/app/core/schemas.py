"""
Pydantic 数据模式定义
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class LabelType(str, Enum):
    """标签类型枚举"""
    INTENT = "intent"
    ENTITY = "entity"
    CATEGORY = "category"

class RuleCategory(str, Enum):
    """规则类别枚举"""
    EXPRESSION = "expression"
    SENTENCE = "sentence"
    KEYWORD = "keyword"

class RelationType(str, Enum):
    """关联类型枚举"""
    BELONGS_TO = "belongs_to"
    SYNONYM = "synonym"
    RELATED = "related"

# 标签体系相关模式
class LabelBase(BaseModel):
    """标签基础模式"""
    label_name: str = Field(..., description="标签名称")
    label_code: str = Field(..., description="标签编码")
    parent_label_name: Optional[str] = Field(None, description="父级标签名称")
    parent_label_code: Optional[str] = Field(None, description="父级标签编码")
    label_type: LabelType = Field(LabelType.INTENT, description="标签类型")
    level: int = Field(1, description="标签层级")
    description: Optional[str] = Field(None, description="标签描述")
    is_active: bool = Field(True, description="是否启用")
    sort_order: int = Field(0, description="排序顺序")

class LabelCreate(LabelBase):
    """创建标签模式"""
    pass

class LabelUpdate(BaseModel):
    """更新标签模式"""
    label_name: Optional[str] = None
    label_code: Optional[str] = None
    parent_label_name: Optional[str] = None
    parent_label_code: Optional[str] = None
    label_type: Optional[LabelType] = None
    level: Optional[int] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None
    sort_order: Optional[int] = None

class LabelResponse(LabelBase):
    """标签响应模式"""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# 规则管理相关模式
class RuleBase(BaseModel):
    """规则基础模式"""
    rule_name: str = Field(..., description="规则名称")
    rule_category: RuleCategory = Field(..., description="规则类别")
    rule_expression: str = Field(..., description="规则表达式")
    rule_sentence: Optional[str] = Field(None, description="规则表达句")
    keywords: Optional[str] = Field(None, description="关键词")
    target_label_id: int = Field(..., description="目标标签ID")
    priority: int = Field(0, description="优先级")
    is_active: bool = Field(True, description="是否启用")

class RuleCreate(RuleBase):
    """创建规则模式"""
    pass

class RuleUpdate(BaseModel):
    """更新规则模式"""
    rule_name: Optional[str] = None
    rule_category: Optional[RuleCategory] = None
    rule_expression: Optional[str] = None
    rule_sentence: Optional[str] = None
    keywords: Optional[str] = None
    target_label_id: Optional[int] = None
    priority: Optional[int] = None
    is_active: Optional[bool] = None

class RuleResponse(RuleBase):
    """规则响应模式"""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# 实体标签相关模式
class EntityTagBase(BaseModel):
    """实体标签基础模式"""
    entity_tag_name: str = Field(..., description="实体标签名称")
    entity_value: str = Field(..., description="实体值")
    entity_type: Optional[str] = Field(None, description="实体类型")
    description: Optional[str] = Field(None, description="描述")
    is_active: bool = Field(True, description="是否启用")

class EntityTagCreate(EntityTagBase):
    """创建实体标签模式"""
    pass

class EntityTagUpdate(BaseModel):
    """更新实体标签模式"""
    entity_tag_name: Optional[str] = None
    entity_value: Optional[str] = None
    entity_type: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None

class EntityTagResponse(EntityTagBase):
    """实体标签响应模式"""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# 数据项相关模式
class ItemDataBase(BaseModel):
    """数据项基础模式"""
    item_name: str = Field(..., description="数据项名称")
    item_synonym: Optional[str] = Field(None, description="同义词")
    item_code: Optional[str] = Field(None, description="数据项编码")
    item_type: Optional[str] = Field(None, description="数据项类型")
    description: Optional[str] = Field(None, description="数据项描述")
    metadata: Optional[Dict[str, Any]] = Field(None, description="元数据")
    is_active: bool = Field(True, description="是否启用")

class ItemDataCreate(ItemDataBase):
    """创建数据项模式"""
    pass

class ItemDataUpdate(BaseModel):
    """更新数据项模式"""
    item_name: Optional[str] = None
    item_synonym: Optional[str] = None
    item_code: Optional[str] = None
    item_type: Optional[str] = None
    description: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None

class ItemDataResponse(ItemDataBase):
    """数据项响应模式"""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# 意图识别相关模式
class IntentRecognitionRequest(BaseModel):
    """意图识别请求模式"""
    text: str = Field(..., description="输入文本")
    context: Optional[Dict[str, Any]] = Field(None, description="上下文信息")

class ExtractedEntity(BaseModel):
    """提取的实体"""
    entity_type: str = Field(..., description="实体类型")
    entity_value: str = Field(..., description="实体值")
    start_pos: int = Field(..., description="开始位置")
    end_pos: int = Field(..., description="结束位置")

class MatchedRule(BaseModel):
    """匹配的规则"""
    rule_id: int = Field(..., description="规则ID")
    rule_name: str = Field(..., description="规则名称")
    rule_category: RuleCategory = Field(..., description="规则类别")
    matched_expression: str = Field(..., description="匹配的表达式")
    confidence: float = Field(..., description="置信度")

class IntentRecognitionResponse(BaseModel):
    """意图识别响应模式"""
    intent: str = Field(..., description="识别出的意图")
    confidence: float = Field(..., description="置信度")
    matched_rules: List[MatchedRule] = Field(..., description="匹配的规则")
    extracted_entities: List[ExtractedEntity] = Field(..., description="提取的实体")
    suggested_actions: List[str] = Field(..., description="建议的操作")

# 通用响应模式
class ResponseModel(BaseModel):
    """通用响应模式"""
    code: int = Field(200, description="响应码")
    message: str = Field("success", description="响应消息")
    data: Optional[Any] = Field(None, description="响应数据")
    timestamp: datetime = Field(default_factory=datetime.now, description="时间戳")

class PaginationParams(BaseModel):
    """分页参数"""
    page: int = Field(1, ge=1, description="页码")
    size: int = Field(20, ge=1, le=100, description="每页数量")

class PaginatedResponse(BaseModel):
    """分页响应模式"""
    items: List[dict] = Field(..., description="数据项")
    total: int = Field(..., description="总数量")
    page: int = Field(..., description="当前页码")
    size: int = Field(..., description="每页数量")
    pages: int = Field(..., description="总页数")

# 兼容路由中引用的复合响应模型
class LabelPageResponse(ResponseModel):
    data: Optional[PaginatedResponse] = Field(None, description="分页后的标签列表")

class ItemDataListResponse(ResponseModel):
    data: Optional[List[ItemDataResponse]] = Field(None, description="数据项列表")