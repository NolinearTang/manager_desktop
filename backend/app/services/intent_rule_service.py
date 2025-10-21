from sqlalchemy.orm import Session
from typing import List, Optional
from backend.app.models import IntentRule
from backend.app.core.schemas import IntentRuleCreate, IntentRuleUpdate

class IntentRuleService:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, rule_id: int) -> Optional[IntentRule]:
        return self.db.query(IntentRule).filter(IntentRule.id == rule_id).first()

    def get_by_code(self, rule_code: str) -> Optional[IntentRule]:
        return self.db.query(IntentRule).filter(IntentRule.rule_code == rule_code).first()

    def get_by_label(self, label_code: str) -> List[IntentRule]:
        return self.db.query(IntentRule).filter(IntentRule.label_code == label_code).all()

    def create(self, rule_create: IntentRuleCreate) -> IntentRule:
        if self.get_by_code(rule_create.rule_code):
            raise ValueError(f"Rule with code {rule_create.rule_code} already exists.")
        
        db_rule = IntentRule(**rule_create.dict())
        self.db.add(db_rule)
        self.db.commit()
        self.db.refresh(db_rule)
        return db_rule

    def update_by_id(self, rule_id: int, rule_update: IntentRuleUpdate) -> Optional[IntentRule]:
        db_rule = self.get_by_id(rule_id)
        if not db_rule:
            return None
        
        update_data = rule_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_rule, field, value)
            
        self.db.commit()
        self.db.refresh(db_rule)
        return db_rule

    def update(self, rule_code: str, rule_update: IntentRuleUpdate) -> Optional[IntentRule]:
        db_rule = self.get_by_code(rule_code)
        if not db_rule:
            return None
        
        update_data = rule_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_rule, field, value)
            
        self.db.commit()
        self.db.refresh(db_rule)
        return db_rule

    def delete_by_id(self, rule_id: int) -> bool:
        db_rule = self.get_by_id(rule_id)
        if not db_rule:
            return False
        
        self.db.delete(db_rule)
        self.db.commit()
        return True

    def delete(self, rule_code: str) -> bool:
        db_rule = self.get_by_code(rule_code)
        if not db_rule:
            return False
        
        self.db.delete(db_rule)
        self.db.commit()
        return True

    def match_rules(self, text: str) -> List[dict]:
        """
        Matches input text against all active rules.
        Returns a list of matched rule dicts, sorted by confidence.
        """
        active_rules = self.db.query(IntentRule).filter(IntentRule.is_active == True).all()
        matched_rules = []
        text = text.lower()

        for rule in active_rules:
            confidence = 0.0
            matched_text = ""

            if rule.rule_type == 'keyword':
                keywords = [k.strip().lower() for k in rule.rule_entity.split(',')]
                for keyword in keywords:
                    if keyword in text:
                        confidence = 0.9 # High confidence for keyword match
                        matched_text = keyword
                        break # Stop after first keyword match for this rule
            
            elif rule.rule_type == 'expression':
                # Simple substring search for now. Can be extended to regex.
                pattern = rule.rule_entity.lower()
                # A placeholder for a more complex pattern like "{产品型号}报{故障码}"
                # This simple version doesn't handle placeholders.
                if pattern in text:
                    confidence = 0.7 # Medium confidence for expression match
                    matched_text = pattern

            if confidence > 0:
                matched_rules.append({
                    "rule_code": rule.rule_code,
                    "rule_type": rule.rule_type,
                    "rule_entity": rule.rule_entity,
                    "label_code": rule.label_code,
                    "matched_text": matched_text,
                    "confidence": confidence,
                })

        # Sort by confidence descending
        return sorted(matched_rules, key=lambda k: k['confidence'], reverse=True)
