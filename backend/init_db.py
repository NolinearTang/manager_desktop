#!/usr/bin/env python3
"""
数据库初始化脚本
"""
import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from backend.app.core.database import engine, Base
from backend.app.models import label_system, rule_management, entity_tag_mapping, item_data, label_item_relation

def init_database():
    """初始化数据库"""
    print("🗄️ 初始化数据库...")
    
    # 创建所有表
    Base.metadata.create_all(bind=engine)
    print("✅ 数据库表创建成功")
    
    # 插入示例数据
    from sqlalchemy.orm import sessionmaker
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        # 检查是否已有数据
        from backend.app.models.label_system import LabelSystem
        if db.query(LabelSystem).first():
            print("ℹ️ 数据库已有数据，跳过初始化")
            return
        
        # 插入标签数据（完整原始数据）
        labels = [
            # 一级意图标签
            LabelSystem(
                label_name="知识问答",
                label_code="knowledge_qa",
                parent_label_name=None,
                parent_label_code=None,
                label_type="intent",
                level=1,
                description="知识问答类意图",
                is_active=True,
                sort_order=0
            ),
            LabelSystem(
                label_name="代码",
                label_code="code",
                parent_label_name=None,
                parent_label_code=None,
                label_type="intent",
                level=1,
                description="代码相关意图",
                is_active=True,
                sort_order=1
            ),
            # 二级意图标签
            LabelSystem(
                label_name="故障码类",
                label_code="fault_code",
                parent_label_name="知识问答",
                parent_label_code="knowledge_qa",
                label_type="intent",
                level=2,
                description="故障码相关问答",
                is_active=True,
                sort_order=0
            ),
            LabelSystem(
                label_name="JS代码",
                label_code="js_code",
                parent_label_name="代码",
                parent_label_code="code",
                label_type="intent",
                level=2,
                description="JavaScript代码相关",
                is_active=True,
                sort_order=0
            ),
            LabelSystem(
                label_name="写代码",
                label_code="write_code",
                parent_label_name="代码",
                parent_label_code="code",
                label_type="intent",
                level=2,
                description="编写代码相关",
                is_active=True,
                sort_order=1
            ),
            # 实体标签
            LabelSystem(
                label_name="产品型号",
                label_code="product_model",
                parent_label_name=None,
                parent_label_code=None,
                label_type="entity",
                level=1,
                description="产品型号实体标签",
                is_active=True,
                sort_order=0
            ),
            LabelSystem(
                label_name="设备型号",
                label_code="device_model",
                parent_label_name=None,
                parent_label_code=None,
                label_type="entity",
                level=1,
                description="设备型号实体标签",
                is_active=True,
                sort_order=1
            ),
            LabelSystem(
                label_name="故障码",
                label_code="fault_code_entity",
                parent_label_name=None,
                parent_label_code=None,
                label_type="entity",
                level=1,
                description="故障码实体标签",
                is_active=True,
                sort_order=2
            )
        ]
        
        for label in labels:
            db.add(label)
        
        db.commit()
        print("✅ 标签数据插入成功")
        
        # 插入规则数据
        from backend.app.models.rule_management import RuleManagement
        
        # 获取标签ID
        fault_code_label = db.query(LabelSystem).filter(LabelSystem.label_code == "fault_code").first()
        js_code_label = db.query(LabelSystem).filter(LabelSystem.label_code == "js_code").first()
        write_code_label = db.query(LabelSystem).filter(LabelSystem.label_code == "write_code").first()
        
        # 插入规则数据（完整原始数据）
        rules = [
            # 故障码类规则
            RuleManagement(
                rule_name="故障码查询规则",
                rule_category="expression",
                rule_expression="{故障码}查询",
                rule_sentence="这个{故障码}是什么意思",
                keywords="故障码,错误代码,报警,异常",
                target_label_id=fault_code_label.id,
                priority=1,
                is_active=True
            ),
            RuleManagement(
                rule_name="故障码含义规则",
                rule_category="expression",
                rule_expression="{故障码}是什么",
                rule_sentence="{故障码}是什么",
                keywords="是什么,含义,意思,代表",
                target_label_id=fault_code_label.id,
                priority=1,
                is_active=True
            ),
            # JS代码规则
            RuleManagement(
                rule_name="JS基础语法规则",
                rule_category="expression",
                rule_expression="{前端框架}语法",
                rule_sentence="{前端框架}的基础语法是什么",
                keywords="JavaScript,JS,语法,基础",
                target_label_id=js_code_label.id,
                priority=1,
                is_active=True
            ),
            # 写代码规则
            RuleManagement(
                rule_name="写代码规则",
                rule_category="keyword",
                rule_expression="写代码",
                rule_sentence="写代码",
                keywords="写代码,编程,开发,编写",
                target_label_id=write_code_label.id,
                priority=1,
                is_active=True
            )
        ]
        
        for rule in rules:
            db.add(rule)
        
        db.commit()
        print("✅ 规则数据插入成功")
        
        # 插入实体标签数据
        from backend.app.models.entity_tag_mapping import EntityTagMapping
        
        # 插入实体标签映射数据（完整原始数据）
        entities = [
            # 产品型号实体
            EntityTagMapping(
                entity_tag_name="产品型号",
                entity_value="SV630N",
                entity_type="product",
                description="汇川伺服驱动器SV630N",
                is_active=True
            ),
            EntityTagMapping(
                entity_tag_name="产品型号",
                entity_value="SV660N",
                entity_type="product",
                description="汇川伺服驱动器SV660N",
                is_active=True
            ),
            EntityTagMapping(
                entity_tag_name="产品型号",
                entity_value="SV680N",
                entity_type="product",
                description="汇川伺服驱动器SV680N",
                is_active=True
            ),
            # 设备型号实体
            EntityTagMapping(
                entity_tag_name="设备型号",
                entity_value="PLC-200",
                entity_type="device",
                description="西门子PLC-200系列",
                is_active=True
            ),
            EntityTagMapping(
                entity_tag_name="设备型号",
                entity_value="PLC-300",
                entity_type="device",
                description="西门子PLC-300系列",
                is_active=True
            ),
            # 故障码实体
            EntityTagMapping(
                entity_tag_name="故障码",
                entity_value="E001",
                entity_type="fault",
                description="过流故障",
                is_active=True
            ),
            EntityTagMapping(
                entity_tag_name="故障码",
                entity_value="E002",
                entity_type="fault",
                description="过压故障",
                is_active=True
            ),
            EntityTagMapping(
                entity_tag_name="故障码",
                entity_value="E003",
                entity_type="fault",
                description="欠压故障",
                is_active=True
            ),
            EntityTagMapping(
                entity_tag_name="故障码",
                entity_value="E004",
                entity_type="fault",
                description="过载故障",
                is_active=True
            )
        ]
        
        for entity in entities:
            db.add(entity)
        
        db.commit()
        print("✅ 实体标签数据插入成功")
        
        # 插入实体数据项并建立关联（完整原始数据）
        from backend.app.models.item_data import ItemData
        from backend.app.models.label_item_relation import LabelItemRelation

        # 如果还没有任何实体数据，则插入一些示例并与标签关联
        if not db.query(ItemData).first():
            items = [
                ItemData(
                    item_name="SV630N变频器",
                    item_code="PROD_SV630N",
                    item_type="product",
                    item_synonym="SV630,变频器630",
                    description="汇川SV630N系列变频器",
                    is_active=True
                ),
                ItemData(
                    item_name="SV660N变频器",
                    item_code="PROD_SV660N",
                    item_type="product",
                    item_synonym="SV660,变频器660",
                    description="汇川SV660N系列变频器",
                    is_active=True
                ),
                ItemData(
                    item_name="E001过流故障",
                    item_code="FAULT_E001",
                    item_type="fault",
                    item_synonym="过流,电流过大",
                    description="E001 过流故障码",
                    is_active=True
                ),
                ItemData(
                    item_name="E002过压故障",
                    item_code="FAULT_E002",
                    item_type="fault",
                    item_synonym="过压,电压过高",
                    description="E002 过压故障码",
                    is_active=True
                ),
                ItemData(
                    item_name="PLC-200控制器",
                    item_code="DEVICE_PLC200",
                    item_type="device",
                    item_synonym="PLC200,控制器200",
                    description="西门子PLC-200系列控制器",
                    is_active=True
                )
            ]
            for it in items:
                db.add(it)
            db.flush()

            # 与标签建立关联
            relations = []
            # 故障码类关联故障数据
            if fault_code_label:
                fault_items = db.query(ItemData).filter(ItemData.item_code.like("FAULT_%")).all()
                for item in fault_items:
                    relations.append(LabelItemRelation(label_id=fault_code_label.id, item_id=item.id, relation_type='belongs_to'))
            
            # 产品型号标签关联产品数据
            product_model_label = db.query(LabelSystem).filter(LabelSystem.label_code == "product_model").first()
            if product_model_label:
                product_items = db.query(ItemData).filter(ItemData.item_code.like("PROD_%")).all()
                for item in product_items:
                    relations.append(LabelItemRelation(label_id=product_model_label.id, item_id=item.id, relation_type='belongs_to'))
            
            # 设备型号标签关联设备数据
            device_model_label = db.query(LabelSystem).filter(LabelSystem.label_code == "device_model").first()
            if device_model_label:
                device_items = db.query(ItemData).filter(ItemData.item_code.like("DEVICE_%")).all()
                for item in device_items:
                    relations.append(LabelItemRelation(label_id=device_model_label.id, item_id=item.id, relation_type='belongs_to'))
            
            for rel in relations:
                db.add(rel)
            db.commit()
            print("✅ 实体数据与关联关系插入成功")

        print("🎉 数据库初始化完成！")
        
    except Exception as e:
        print(f"❌ 数据库初始化失败: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    init_database()
