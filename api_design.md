# 标签体系管理系统 API 设计文档

## 基础信息
- **基础URL**: `http://localhost:8000/api/v1`
- **认证方式**: JWT Token
- **数据格式**: JSON

## 1. 标签体系管理 API

### 1.1 获取标签列表
```
GET /labels
```
**参数**:
- `parent_code` (可选): 父级标签编码
- `label_type` (可选): 标签类型 (intent/entity/category)
- `level` (可选): 标签层级
- `page` (可选): 页码，默认1
- `size` (可选): 每页数量，默认20

**响应**:
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "items": [
      {
        "id": 1,
        "label_name": "知识问答",
        "label_code": "knowledge_qa",
        "parent_label_name": null,
        "parent_label_code": null,
        "label_type": "intent",
        "level": 1,
        "description": "知识问答类意图",
        "is_active": true,
        "sort_order": 0,
        "created_at": "2024-01-01T00:00:00Z",
        "updated_at": "2024-01-01T00:00:00Z"
      }
    ],
    "total": 1,
    "page": 1,
    "size": 20
  }
}
```

### 1.2 创建标签
```
POST /labels
```
**请求体**:
```json
{
  "label_name": "故障码类",
  "label_code": "fault_code",
  "parent_label_name": "知识问答",
  "parent_label_code": "knowledge_qa",
  "label_type": "intent",
  "description": "故障码相关问答"
}
```

### 1.3 更新标签
```
PUT /labels/{label_id}
```

### 1.4 删除标签
```
DELETE /labels/{label_id}
```

## 2. 规则管理 API

### 2.1 获取规则列表
```
GET /rules
```
**参数**:
- `label_id` (可选): 标签ID
- `rule_category` (可选): 规则类别 (expression/sentence/keyword)
- `is_active` (可选): 是否启用
- `page` (可选): 页码
- `size` (可选): 每页数量

**响应**:
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "items": [
      {
        "id": 1,
        "rule_name": "故障码查询规则",
        "rule_category": "expression",
        "rule_expression": "{故障码}查询",
        "rule_sentence": "这个{故障码}是什么意思",
        "keywords": "故障码,错误代码,报警,异常",
        "target_label_id": 2,
        "priority": 1,
        "is_active": true,
        "created_at": "2024-01-01T00:00:00Z",
        "updated_at": "2024-01-01T00:00:00Z"
      }
    ],
    "total": 1,
    "page": 1,
    "size": 20
  }
}
```

### 2.2 创建规则
```
POST /rules
```
**请求体**:
```json
{
  "rule_name": "故障码查询规则",
  "rule_category": "expression",
  "rule_expression": "{故障码}查询",
  "rule_sentence": "这个{故障码}是什么意思",
  "keywords": "故障码,错误代码,报警,异常",
  "target_label_id": 2,
  "priority": 1
}
```

### 2.3 更新规则
```
PUT /rules/{rule_id}
```

### 2.4 删除规则
```
DELETE /rules/{rule_id}
```

## 3. 实体标签管理 API

### 3.1 获取实体标签列表
```
GET /entity-tags
```
**参数**:
- `entity_tag_name` (可选): 实体标签名称
- `entity_type` (可选): 实体类型
- `page` (可选): 页码
- `size` (可选): 每页数量

### 3.2 创建实体标签
```
POST /entity-tags
```
**请求体**:
```json
{
  "entity_tag_name": "产品型号",
  "entity_value": "SV630N",
  "entity_type": "product",
  "description": "汇川伺服驱动器SV630N"
}
```

### 3.3 更新实体标签
```
PUT /entity-tags/{entity_tag_id}
```

### 3.4 删除实体标签
```
DELETE /entity-tags/{entity_tag_id}
```

## 4. 意图识别 API

### 4.1 意图识别
```
POST /intent-recognition
```
**请求体**:
```json
{
  "text": "这个E001故障码是什么意思",
  "context": {
    "user_id": "12345",
    "session_id": "session_001"
  }
}
```

**响应**:
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "intent": "故障码查询",
    "confidence": 0.95,
    "matched_rules": [
      {
        "rule_id": 1,
        "rule_name": "故障码查询规则",
        "rule_category": "expression",
        "matched_expression": "{故障码}查询",
        "confidence": 0.95
      }
    ],
    "extracted_entities": [
      {
        "entity_type": "故障码",
        "entity_value": "E001",
        "start_pos": 2,
        "end_pos": 5
      }
    ],
    "suggested_actions": [
      "查询故障码E001的详细信息",
      "提供故障码E001的解决方案"
    ]
  }
}
```

## 5. 数据管理 API

### 5.1 获取数据项列表
```
GET /items
```
**参数**:
- `item_name` (可选): 数据项名称
- `item_type` (可选): 数据项类型
- `label_id` (可选): 关联标签ID
- `page` (可选): 页码
- `size` (可选): 每页数量

### 5.2 创建数据项
```
POST /items
```
**请求体**:
```json
{
  "item_name": "汇川伺服驱动器SV630N",
  "item_synonym": ["SV630N", "汇川630N", "伺服驱动器630N"],
  "item_code": "SV630N",
  "item_type": "product",
  "description": "汇川伺服驱动器SV630N产品信息",
  "metadata": {
    "voltage": "220V",
    "power": "1.5KW",
    "brand": "汇川"
  }
}
```

### 5.3 关联标签和数据项
```
POST /label-item-relations
```
**请求体**:
```json
{
  "label_id": 1,
  "item_id": 1,
  "relation_type": "belongs_to",
  "weight": 1.0
}
```

## 6. 统计和分析 API

### 6.1 获取标签统计
```
GET /statistics/labels
```

### 6.2 获取规则统计
```
GET /statistics/rules
```

### 6.3 获取意图识别统计
```
GET /statistics/intent-recognition
```

## 错误码说明

| 错误码 | 说明 |
|--------|------|
| 200 | 成功 |
| 400 | 请求参数错误 |
| 401 | 未授权 |
| 403 | 禁止访问 |
| 404 | 资源不存在 |
| 500 | 服务器内部错误 |

## 响应格式

所有API响应都遵循以下格式：
```json
{
  "code": 200,
  "message": "success",
  "data": {},
  "timestamp": "2024-01-01T00:00:00Z"
}
```
