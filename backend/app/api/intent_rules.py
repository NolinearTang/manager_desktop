from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend.app.core.database import get_db
from backend.app.services.intent_rule_service import IntentRuleService
from backend.app.core.schemas import IntentRuleCreate, IntentRuleUpdate, IntentRuleResponse

router = APIRouter()

@router.post("/", response_model=IntentRuleResponse)
def create_rule(rule: IntentRuleCreate, db: Session = Depends(get_db)):
    service = IntentRuleService(db)
    try:
        return service.create(rule)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/by_label/{label_code}", response_model=List[IntentRuleResponse])
def get_rules_by_label(label_code: str, db: Session = Depends(get_db)):
    service = IntentRuleService(db)
    return service.get_by_label(label_code)

@router.get("/id/{rule_id}", response_model=IntentRuleResponse)
def get_rule_by_id(rule_id: int, db: Session = Depends(get_db)):
    service = IntentRuleService(db)
    db_rule = service.get_by_id(rule_id)
    if db_rule is None:
        raise HTTPException(status_code=404, detail="Rule not found")
    return db_rule

@router.get("/{rule_code}", response_model=IntentRuleResponse)
def get_rule(rule_code: str, db: Session = Depends(get_db)):
    service = IntentRuleService(db)
    db_rule = service.get_by_code(rule_code)
    if db_rule is None:
        raise HTTPException(status_code=404, detail="Rule not found")
    return db_rule

@router.put("/id/{rule_id}", response_model=IntentRuleResponse)
def update_rule_by_id(rule_id: int, rule: IntentRuleUpdate, db: Session = Depends(get_db)):
    service = IntentRuleService(db)
    db_rule = service.update_by_id(rule_id, rule)
    if db_rule is None:
        raise HTTPException(status_code=404, detail="Rule not found")
    return db_rule

@router.put("/{rule_code}", response_model=IntentRuleResponse)
def update_rule(rule_code: str, rule: IntentRuleUpdate, db: Session = Depends(get_db)):
    service = IntentRuleService(db)
    db_rule = service.update(rule_code, rule)
    if db_rule is None:
        raise HTTPException(status_code=404, detail="Rule not found")
    return db_rule

@router.delete("/id/{rule_id}", status_code=204)
def delete_rule_by_id(rule_id: int, db: Session = Depends(get_db)):
    service = IntentRuleService(db)
    if not service.delete_by_id(rule_id):
        raise HTTPException(status_code=404, detail="Rule not found")
    return {"ok": True}

@router.delete("/{rule_code}", status_code=204)
def delete_rule(rule_code: str, db: Session = Depends(get_db)):
    service = IntentRuleService(db)
    if not service.delete(rule_code):
        raise HTTPException(status_code=404, detail="Rule not found")
    return {"ok": True}
