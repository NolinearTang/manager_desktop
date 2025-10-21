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
            TagSystem(
                system_name="汇川产品实体体系", 
                system_code="product_entity_system", 
                system_type="entity",
                description="汇川技术产品的层级标签体系，包括产品线、产品系列、产品型号、产品规格等实体标签"
            ),
            TagSystem(
                system_name="知识问答意图体系", 
                system_code="intent_system", 
                system_type="intent",
                description="用于识别用户知识问答相关的意图，包括故障码查询、参数查询等意图标签"
            ),
            TagSystem(
                system_name="硬工委实体标签体系", 
                system_code="hardware_committee_entity_system", 
                system_type="entity",
                description="硬工委相关的实体标签体系，包括委员会成员、组织架构、项目分类等实体标签"
            ),
            TagSystem(
                system_name="参数实体标签体系", 
                system_code="parameter_entity_system", 
                system_type="entity",
                description="产品参数相关的实体标签体系，包括参数类型、参数分组、参数配置等实体标签"
            ),
            TagSystem(
                system_name="易知助手意图体系", 
                system_code="yizhi_assistant_intent_system", 
                system_type="intent",
                description="易知助手的意图识别体系，包括问候、咨询、投诉、建议等对话意图标签"
            ),
        ]
        db.add_all(tag_systems)
        db.commit()

        # 2. 插入标签定义 (Label)
        print("  - 正在插入 Label...")
        labels = [
            # ========== 意图体系标签 (前缀: intent_label_) ==========
            # 1级标签
            Label(label_name="知识问答", label_code="intent_label_001", system_code="intent_system", level=1, description="知识问答相关意图"),
            Label(label_name="代码类", label_code="intent_label_002", system_code="intent_system", level=1, description="代码编写相关意图"),
            Label(label_name="无意义", label_code="intent_label_003", system_code="intent_system", level=1, description="无意义对话"),
            Label(label_name="身份认知", label_code="intent_label_004", system_code="intent_system", level=1, description="身份认知相关"),
            Label(label_name="有害", label_code="intent_label_005", system_code="intent_system", level=1, description="有害内容"),
            Label(label_name="其他", label_code="intent_label_006", system_code="intent_system", level=1, description="其他意图"),
            
            # 2级标签 - 知识问答下的子标签
            Label(label_name="其他知识问答", label_code="intent_label_101", parent_label_code="intent_label_001", system_code="intent_system", level=2, description="其他类型的知识问答"),
            Label(label_name="故障类", label_code="intent_label_102", parent_label_code="intent_label_001", system_code="intent_system", level=2, description="故障相关问答"),
            Label(label_name="通识类", label_code="intent_label_103", parent_label_code="intent_label_001", system_code="intent_system", level=2, description="通用知识问答"),
            Label(label_name="故障码类", label_code="intent_label_104", parent_label_code="intent_label_001", system_code="intent_system", level=2, description="故障码查询"),
            
            # 2级标签 - 代码类下的子标签
            Label(label_name="ST代码", label_code="intent_label_201", parent_label_code="intent_label_002", system_code="intent_system", level=2, description="ST语言代码"),
            Label(label_name="JS代码", label_code="intent_label_202", parent_label_code="intent_label_002", system_code="intent_system", level=2, description="JavaScript代码"),
            Label(label_name="其他语言代码", label_code="intent_label_203", parent_label_code="intent_label_002", system_code="intent_system", level=2, description="其他编程语言代码"),
            
            # 3级标签 - 其他知识问答下的子标签
            Label(label_name="产品查询", label_code="intent_label_10101", parent_label_code="intent_label_101", system_code="intent_system", level=3, description="产品信息查询"),
            
            # ========== 产品实体体系标签 (前缀: entity_label_) ==========
            Label(label_name='产品线', label_code='entity_label_001', system_code='product_entity_system', level=1, description='产品线分类'),
            Label(label_name="故障码", label_code="entity_label_002", system_code="product_entity_system", level=1, description='故障码信息'),
            Label(label_name="指令信息", label_code="entity_label_003", system_code="product_entity_system", level=1, description='指令相关信息'),
            Label(label_name='产品系列', label_code='entity_label_101', parent_label_code='entity_label_001', system_code='product_entity_system', level=2, description='产品系列分类'),
            Label(label_name='产品型号', label_code='entity_label_10101', parent_label_code='entity_label_101', system_code='product_entity_system', level=3, description='具体产品型号'),
            Label(label_name='产品规格', label_code='entity_label_1010101', parent_label_code='entity_label_10101', system_code='product_entity_system', level=4, description='产品规格参数'),
        ]
        db.add_all(labels)
        db.commit()

        # 3. 插入实体 (Item) 及其同义词 (前缀: item_code_)
        print("  - 正在插入 Item...")
        items = [
            Item(item_name='伺服', item_code='item_code_001', label_code='entity_label_001', description='伺服产品线'),
            Item(item_name='PLC', item_code='item_code_002', label_code='entity_label_001', description='PLC产品线'),
            Item(item_name='SV660系列', item_code='item_code_101', parent_item_code='item_code_001', label_code='entity_label_101', description='SV660伺服系列'),
            Item(item_name='SV660A', item_code='item_code_10101', parent_item_code='item_code_101', label_code='entity_label_10101', description='SV660A型号'),
            Item(item_name='SV660N', item_code='item_code_10102', parent_item_code='item_code_101', label_code='entity_label_10101', description='SV660N通用伺服', synonyms=[
                ItemSynonym(synonym="SV660N通用伺服"),
                ItemSynonym(synonym="SV660N")
            ]),
            Item(item_name='SV660NS2R8', item_code='item_code_1010201', parent_item_code='item_code_10102', label_code='entity_label_1010101', description='SV660NS2R8规格'),
            Item(item_name='SV660NS3R6', item_code='item_code_1010202', parent_item_code='item_code_10102', label_code='entity_label_1010101', description='SV660NS3R6规格'),
        ]
        db.add_all(items)
        db.commit()

        # 4. 插入意图规则 (IntentRule)
        print("  - 正在插入 IntentRule...")
        rules = [
            # 故障码类规则
            IntentRule(
                rule_code="intent_rule_001",
                rule_type="keyword",
                rule_entity="故障,报警,错误代码,故障码",
                label_code="intent_label_104",
                is_active=True
            ),
            IntentRule(
                rule_code="intent_rule_002",
                rule_type="expression",
                rule_entity="{产品型号}报{故障码}",
                label_code="intent_label_104",
                is_active=True
            ),
            # 产品查询规则
            IntentRule(
                rule_code="intent_rule_003",
                rule_type="keyword",
                rule_entity="产品,型号,规格,参数",
                label_code="intent_label_10101",
                is_active=True
            ),
            # ST代码规则
            IntentRule(
                rule_code="intent_rule_004",
                rule_type="keyword",
                rule_entity="ST代码,ST语言,结构化文本",
                label_code="intent_label_201",
                is_active=True
            ),
            # JS代码规则
            IntentRule(
                rule_code="intent_rule_005",
                rule_type="keyword",
                rule_entity="JavaScript,JS代码,前端代码",
                label_code="intent_label_202",
                is_active=True
            ),
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
