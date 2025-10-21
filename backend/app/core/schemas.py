"""
Pydantic Schemas for new database design (V2)
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

# ===================================================================
# 1. TagSystem Schemas
# ===================================================================
class TagSystemBase(BaseModel):
    system_name: str = Field(..., description="体系名称")
    system_code: str = Field(..., description="体系编码")
    system_type: str = Field(..., description="体系类型 (e.g., intent, entity)")
    description: Optional[str] = Field(None, description="体系描述")

class TagSystemCreate(TagSystemBase):
    pass

class TagSystemUpdate(BaseModel):
    system_name: Optional[str] = None
    system_type: Optional[str] = None
    description: Optional[str] = None

class TagSystemResponse(TagSystemBase):
    id: int
    created_at: datetime
    updated_at: datetime
    class Config: from_attributes = True

# ===================================================================
# 2. Label Schemas
# ===================================================================
class LabelBase(BaseModel):
    label_name: str = Field(..., description="标签名称")
    label_code: str = Field(..., description="标签编码")
    parent_label_code: Optional[str] = Field(None, description="父级标签编码")
    system_code: str = Field(..., description="所属体系编码")
    level: int = Field(1, description="标签层级")
    description: Optional[str] = Field(None, description="标签描述")

class LabelCreate(LabelBase):
    pass

class LabelUpdate(BaseModel):
    label_name: Optional[str] = None
    parent_label_code: Optional[str] = None
    description: Optional[str] = None

class LabelResponse(LabelBase):
    id: int
    created_at: datetime
    updated_at: datetime
    class Config: from_attributes = True

# ===================================================================
# 3. Item Schemas
# ===================================================================
class ItemSynonymBase(BaseModel):
    synonym: str = Field(..., description="同义词")

class ItemSynonymResponse(ItemSynonymBase):
    id: int
    item_code: str
    class Config: from_attributes = True

class ItemBase(BaseModel):
    item_name: str = Field(..., description="实体名称")
    item_code: str = Field(..., description="实体编码")
    parent_item_code: Optional[str] = Field(None, description="父级实体编码")
    label_code: str = Field(..., description="所属标签编码")
    description: Optional[str] = Field(None, description="实体描述")
    is_active: bool = Field(True, description="是否启用")

class ItemCreate(ItemBase):
    synonyms: List[str] = Field([], description="同义词列表")

class ItemUpdate(BaseModel):
    item_name: Optional[str] = None
    parent_item_code: Optional[str] = None
    label_code: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None
    synonyms: Optional[List[str]] = None

class ItemResponse(ItemBase):
    id: int
    created_at: datetime
    updated_at: datetime
    parent_item_name: Optional[str] = None
    synonyms: List[ItemSynonymResponse] = []
    class Config: from_attributes = True

# ===================================================================
# 4. IntentRule Schemas
# ===================================================================
class IntentRuleBase(BaseModel):
    rule_code: str = Field(..., description="规则编码")
    rule_type: str = Field(..., description="规则类型")
    rule_entity: str = Field(..., description="规则实体 (内容)")
    label_code: str = Field(..., description="关联的意图标签编码")
    is_active: bool = Field(True, description="是否启用")

class IntentRuleCreate(IntentRuleBase):
    pass

class IntentRuleUpdate(BaseModel):
    rule_type: Optional[str] = None
    rule_entity: Optional[str] = None
    label_code: Optional[str] = None
    is_active: Optional[bool] = None

class IntentRuleResponse(IntentRuleBase):
    id: int
    created_at: datetime
    updated_at: datetime
    class Config: from_attributes = True

# ===================================================================
# 5. Intent Recognition Schemas (Legacy, for compatibility)
# ===================================================================
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
    rule_code: str = Field(..., description="规则编码")
    rule_type: str = Field(..., description="规则类型")
    rule_entity: str = Field(..., description="规则实体(内容)")
    matched_text: str = Field(..., description="匹配到的文本")
    confidence: float = Field(..., description="置信度")

class IntentRecognitionResponse(BaseModel):
    """意图识别响应模式"""
    intent: str = Field(..., description="识别出的意图")
    confidence: float = Field(..., description="置信度")
    matched_rules: List[MatchedRule] = Field(..., description="匹配的规则")
    extracted_entities: List[ExtractedEntity] = Field(..., description="提取的实体")
    suggested_actions: List[str] = Field(..., description="建议的操作")

# ===================================================================
# 6. Utility Schemas
# ===================================================================
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
    items: List[Any]
    total: int
    page: int
    size: int