"""
意图识别API (V2)
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.core.database import get_db
from backend.app.core.schemas import (
    IntentRecognitionRequest, IntentRecognitionResponse,
    ResponseModel, ExtractedEntity, MatchedRule
)
from backend.app.services.intent_rule_service import IntentRuleService
from backend.app.services.item_service import ItemService
from backend.app.services.label_service import LabelService

router = APIRouter()

@router.post("/", response_model=ResponseModel)
async def recognize_intent(
    request: IntentRecognitionRequest,
    db: Session = Depends(get_db)
):
    """意图识别接口"""
    try:
        text = request.text.strip()
        if not text:
            raise HTTPException(status_code=400, detail="输入文本不能为空")
        
        # 1. 初始化服务
        rule_service = IntentRuleService(db)
        item_service = ItemService(db)
        label_service = LabelService(db)
        
        # 2. 匹配规则
        matched_rules_data = rule_service.match_rules(text)
        
        if not matched_rules_data:
            return ResponseModel(
                data=IntentRecognitionResponse(
                    intent="未识别",
                    confidence=0.0,
                    matched_rules=[],
                    extracted_entities=[],
                    suggested_actions=["请提供更明确的描述"]
                )
            )
        
        # 3. 获取最佳匹配和目标意图
        best_rule = matched_rules_data[0]
        target_label = label_service.get_by_code(best_rule["label_code"])
        intent_name = target_label.label_name if target_label else "未知意图"
        
        # 4. 提取实体
        extracted_entities_data = item_service.extract_entities_from_text(text)
        
        # 5. 生成建议操作 (此函数可保持不变)
        suggested_actions = generate_suggested_actions(intent_name, extracted_entities_data)
        
        # 6. 构建响应
        response_data = IntentRecognitionResponse(
            intent=intent_name,
            confidence=best_rule["confidence"],
            matched_rules=[
                MatchedRule(
                    rule_code=rule["rule_code"],
                    rule_type=rule["rule_type"],
                    rule_entity=rule["rule_entity"],
                    matched_text=rule["matched_text"],
                    confidence=rule["confidence"]
                ) for rule in matched_rules_data
            ],
            extracted_entities=[
                ExtractedEntity(
                    entity_type=entity["entity_type"],
                    entity_value=entity["entity_value"],
                    start_pos=entity["start_pos"],
                    end_pos=entity["end_pos"]
                ) for entity in extracted_entities_data
            ],
            suggested_actions=suggested_actions
        )
        
        return ResponseModel(data=response_data)
        
    except HTTPException:
        raise
    except Exception as e:
        # For debugging
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

def generate_suggested_actions(intent_name: str, extracted_entities: list) -> list:
    """生成建议操作"""
    actions = []
    if "故障码" in intent_name:
        actions.append("查询故障码详细信息")
        actions.append("提供故障码解决方案")
        if extracted_entities:
            actions.append(f"分析{extracted_entities[0]['entity_value']}相关故障")
    elif "代码" in intent_name or "编程" in intent_name:
        actions.append("提供代码示例")
    else:
        actions.append("提供相关帮助")
    return actions
