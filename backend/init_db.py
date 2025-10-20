#!/usr/bin/env python3
"""
数据库初始化脚本 (V2)
"""
import sys
from pathlib import Path

# 添加项目根目录到Python路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.app.core.database import engine, Base
from backend.app.models import (
    TagSystem, Label, Item, ItemSynonym, IntentRule
)
from sqlalchemy.orm import sessionmaker

def init_database():
    """初始化数据库 V2"""
    print("🗄️  正在初始化数据库 (V2)...")
    
    print("🗑️  正在删除旧表...")
    Base.metadata.drop_all(bind=engine)
    print("✨  正在创建新表...")
    Base.metadata.create_all(bind=engine)
    print("✅  数据库表创建成功")
    
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        if db.query(TagSystem).first():
            print("ℹ️  数据库已有数据，跳过初始化")
            return

        # 1. 插入标签体系 (TagSystem)
        print("  - 正在插入 TagSystem...")
        tag_systems = [
            TagSystem(system_name="产品实体体系", system_code="product_entity_system", system_type="entity"),
            TagSystem(system_name="客户意图体系", system_code="intent_system", system_type="intent"),
        ]
        db.add_all(tag_systems)
        db.commit()

        # 2. 插入标签定义 (Label)
        print("  - 正在插入 Label...")
        labels = [
            # 意图体系
            Label(label_name="知识问答", label_code="knowledge_qa", system_code="intent_system", level=1),
            Label(label_name="故障码查询", label_code="fault_code_query", parent_label_code="knowledge_qa", system_code="intent_system", level=2),
            # 产品实体体系
            Label(label_name='产品线', label_code='product_line', system_code='product_entity_system', level=1),
            Label(label_name='产品系列', label_code='product_series', parent_label_code='product_line', system_code='product_entity_system', level=2),
            Label(label_name='产品型号', label_code='product_model', parent_label_code='product_series', system_code='product_entity_system', level=3),
            Label(label_name='产品规格', label_code='product_spec', parent_label_code='product_model', system_code='product_entity_system', level=4),
        ]
        db.add_all(labels)
        db.commit()

        # 3. 插入实体 (Item) 及其同义词
        print("  - 正在插入 Item...")
        items = [
            Item(item_name='伺服', item_code='servo', label_code='product_line'),
            Item(item_name='PLC', item_code='plc', label_code='product_line'),
            Item(item_name='SV660系列', item_code='sv660_series', parent_item_code='servo', label_code='product_series'),
            Item(item_name='SV660A', item_code='sv660a', parent_item_code='sv660_series', label_code='product_model'),
            Item(item_name='SV660N', item_code='sv660n', parent_item_code='sv660_series', label_code='product_model', synonyms=[
                ItemSynonym(synonym="SV660N通用伺服")
            ]),
            Item(item_name='SV660NS2R8', item_code='sv660ns2r8', parent_item_code='sv660n', label_code='product_spec'),
            Item(item_name='SV660NS3R6', item_code='sv660ns3r6', parent_item_code='sv660n', label_code='product_spec'),
        ]
        db.add_all(items)
        db.commit()

        # 4. 插入意图规则 (IntentRule)
        print("  - 正在插入 IntentRule...")
        rules = [
            IntentRule(
                rule_code="fault_query_keyword_1",
                rule_type="keyword",
                rule_entity="故障,报警,错误代码",
                label_code="fault_code_query",
            ),
            IntentRule(
                rule_code="fault_query_expr_1",
                rule_type="expression",
                rule_entity="{产品型号}报{故障码}",
                label_code="fault_code_query",
            )
        ]
        db.add_all(rules)
        db.commit()

        print("🎉 数据库初始化完成！")
        
    except Exception as e:
        print(f"❌ 数据库初始化失败: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    init_database()
