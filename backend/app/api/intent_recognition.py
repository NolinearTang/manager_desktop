"""
意图识别API
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.core.database import get_db
from backend.app.core.schemas import (
    IntentRecognitionRequest, IntentRecognitionResponse,
    ResponseModel, ExtractedEntity, MatchedRule
)
from backend.app.services.rule_service import RuleService
from backend.app.services.entity_tag_service import EntityTagService
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
        
        # 初始化服务
        rule_service = RuleService(db)
        entity_service = EntityTagService(db)
        label_service = LabelService(db)
        
        # 匹配规则
        matched_rules = rule_service.match_rules(text)
        
        if not matched_rules:
            # 没有匹配到规则，返回默认意图
            return ResponseModel(
                data=IntentRecognitionResponse(
                    intent="未识别",
                    confidence=0.0,
                    matched_rules=[],
                    extracted_entities=[],
                    suggested_actions=["请提供更明确的描述"]
                )
            )
        
        # 获取最佳匹配规则
        best_rule = matched_rules[0]
        
        # 获取目标标签信息
        target_label = label_service.get_label_by_id(best_rule["rule_id"])
        intent_name = target_label.label_name if target_label else "未知意图"
        
        # 提取实体
        extracted_entities = entity_service.extract_entities_from_text(text)
        
        # 生成建议操作
        suggested_actions = generate_suggested_actions(intent_name, extracted_entities)
        
        # 构建响应
        response_data = IntentRecognitionResponse(
            intent=intent_name,
            confidence=best_rule["confidence"],
            matched_rules=[
                MatchedRule(
                    rule_id=rule["rule_id"],
                    rule_name=rule["rule_name"],
                    rule_category=rule["rule_category"],
                    matched_expression=rule["matched_expression"],
                    confidence=rule["confidence"]
                ) for rule in matched_rules
            ],
            extracted_entities=[
                ExtractedEntity(
                    entity_type=entity["entity_type"],
                    entity_value=entity["entity_value"],
                    start_pos=entity["start_pos"],
                    end_pos=entity["end_pos"]
                ) for entity in extracted_entities
            ],
            suggested_actions=suggested_actions
        )
        
        return ResponseModel(data=response_data)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def generate_suggested_actions(intent_name: str, extracted_entities: list) -> list:
    """生成建议操作"""
    actions = []
    
    # 根据意图类型生成建议
    if "故障码" in intent_name:
        actions.append("查询故障码详细信息")
        actions.append("提供故障码解决方案")
        if extracted_entities:
            actions.append(f"分析{extracted_entities[0]['entity_value']}相关故障")
    
    elif "代码" in intent_name or "编程" in intent_name:
        actions.append("提供代码示例")
        actions.append("解释代码逻辑")
        actions.append("提供调试建议")
    
    elif "知识问答" in intent_name:
        actions.append("提供详细解答")
        actions.append("查找相关资料")
        actions.append("联系技术支持")
    
    else:
        actions.append("提供相关帮助")
        actions.append("查找更多信息")
    
    return actions