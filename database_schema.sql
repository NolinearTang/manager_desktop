-- 标签体系管理系统数据库设计
-- 创建时间: 2024

-- 1. 标签体系表 (label_system)
-- 存储标签的层级关系和基本信息
CREATE TABLE label_system (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '主键ID',
    label_name VARCHAR(100) NOT NULL COMMENT '标签名称',
    label_code VARCHAR(50) NOT NULL UNIQUE COMMENT '标签编码',
    parent_label_name VARCHAR(100) COMMENT '父级标签名称',
    parent_label_code VARCHAR(50) COMMENT '父级标签编码',
    label_type ENUM('intent', 'entity', 'category') NOT NULL DEFAULT 'intent' COMMENT '标签类型：意图标签、实体标签、分类标签',
    level INT NOT NULL DEFAULT 1 COMMENT '标签层级',
    description TEXT COMMENT '标签描述',
    is_active BOOLEAN NOT NULL DEFAULT TRUE COMMENT '是否启用',
    sort_order INT DEFAULT 0 COMMENT '排序顺序',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_parent_code (parent_label_code),
    INDEX idx_label_type (label_type),
    INDEX idx_level (level)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='标签体系表';

-- 2. 数据信息表 (item_data)
-- 存储具体的实体数据项
CREATE TABLE item_data (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '主键ID',
    item_name VARCHAR(200) NOT NULL COMMENT '数据项名称',
    item_synonym TEXT COMMENT '同义词，JSON格式存储',
    item_code VARCHAR(100) COMMENT '数据项编码',
    item_type VARCHAR(50) COMMENT '数据项类型',
    description TEXT COMMENT '数据项描述',
    metadata JSON COMMENT '元数据，JSON格式存储',
    is_active BOOLEAN NOT NULL DEFAULT TRUE COMMENT '是否启用',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_item_name (item_name),
    INDEX idx_item_type (item_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='数据信息表';

-- 3. 标签体系关联表 (label_item_relation)
-- 关联标签和具体数据项
CREATE TABLE label_item_relation (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '主键ID',
    label_id BIGINT NOT NULL COMMENT '标签ID',
    item_id BIGINT NOT NULL COMMENT '数据项ID',
    relation_type ENUM('belongs_to', 'synonym', 'related') NOT NULL DEFAULT 'belongs_to' COMMENT '关联类型',
    weight DECIMAL(3,2) DEFAULT 1.00 COMMENT '权重',
    is_active BOOLEAN NOT NULL DEFAULT TRUE COMMENT '是否启用',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    UNIQUE KEY uk_label_item (label_id, item_id),
    FOREIGN KEY (label_id) REFERENCES label_system(id) ON DELETE CASCADE,
    FOREIGN KEY (item_id) REFERENCES item_data(id) ON DELETE CASCADE,
    INDEX idx_label_id (label_id),
    INDEX idx_item_id (item_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='标签体系关联表';

-- 4. 规则管理表 (rule_management)
-- 存储意图识别规则
CREATE TABLE rule_management (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '主键ID',
    rule_name VARCHAR(200) NOT NULL COMMENT '规则名称',
    rule_category ENUM('expression', 'sentence', 'keyword') NOT NULL COMMENT '规则类别：表达式、表达句、关键词',
    rule_expression TEXT NOT NULL COMMENT '规则表达式',
    rule_sentence TEXT COMMENT '规则表达句',
    keywords TEXT COMMENT '关键词，逗号分隔',
    target_label_id BIGINT NOT NULL COMMENT '目标标签ID',
    priority INT DEFAULT 0 COMMENT '优先级',
    is_active BOOLEAN NOT NULL DEFAULT TRUE COMMENT '是否启用',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    FOREIGN KEY (target_label_id) REFERENCES label_system(id) ON DELETE CASCADE,
    INDEX idx_target_label (target_label_id),
    INDEX idx_rule_category (rule_category),
    INDEX idx_priority (priority)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='规则管理表';

-- 5. 实体标签映射表 (entity_tag_mapping)
-- 存储实体标签的具体值
CREATE TABLE entity_tag_mapping (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '主键ID',
    entity_tag_name VARCHAR(100) NOT NULL COMMENT '实体标签名称',
    entity_value VARCHAR(200) NOT NULL COMMENT '实体值',
    entity_type VARCHAR(50) COMMENT '实体类型',
    description TEXT COMMENT '描述',
    is_active BOOLEAN NOT NULL DEFAULT TRUE COMMENT '是否启用',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    UNIQUE KEY uk_entity_value (entity_tag_name, entity_value),
    INDEX idx_entity_tag (entity_tag_name),
    INDEX idx_entity_type (entity_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='实体标签映射表';

-- 插入示例数据
-- 标签体系示例数据
INSERT INTO label_system (label_name, label_code, parent_label_name, parent_label_code, label_type, level, description) VALUES
('知识问答', 'knowledge_qa', NULL, NULL, 'intent', 1, '知识问答类意图'),
('故障码类', 'fault_code', '知识问答', 'knowledge_qa', 'intent', 2, '故障码相关问答'),
('代码', 'code', NULL, NULL, 'intent', 1, '代码相关意图'),
('JS代码', 'js_code', '代码', 'code', 'intent', 2, 'JavaScript代码相关'),
('写代码', 'write_code', '代码', 'code', 'intent', 2, '编写代码相关'),
('产品型号', 'product_model', NULL, NULL, 'entity', 1, '产品型号实体标签'),
('设备型号', 'device_model', NULL, NULL, 'entity', 1, '设备型号实体标签'),
('故障码', 'fault_code_entity', NULL, NULL, 'entity', 1, '故障码实体标签');

-- 实体标签映射示例数据
INSERT INTO entity_tag_mapping (entity_tag_name, entity_value, entity_type, description) VALUES
('产品型号', 'SV630N', 'product', '汇川伺服驱动器SV630N'),
('产品型号', 'SV660N', 'product', '汇川伺服驱动器SV660N'),
('产品型号', 'SV680N', 'product', '汇川伺服驱动器SV680N'),
('设备型号', 'PLC-200', 'device', '西门子PLC-200系列'),
('设备型号', 'PLC-300', 'device', '西门子PLC-300系列'),
('故障码', 'E001', 'fault', '过流故障'),
('故障码', 'E002', 'fault', '过压故障'),
('故障码', 'E003', 'fault', '欠压故障'),
('故障码', 'E004', 'fault', '过载故障');

-- 规则管理示例数据
INSERT INTO rule_management (rule_name, rule_category, rule_expression, rule_sentence, keywords, target_label_id, priority) VALUES
('故障码查询规则', 'expression', '{故障码}查询', '这个{故障码}是什么意思', '故障码,错误代码,报警,异常', 2, 1),
('故障码含义规则', 'expression', '{故障码}是什么', '{故障码}是什么', '是什么,含义,意思,代表', 2, 1),
('JS基础语法规则', 'expression', '{前端框架}语法', '{前端框架}的基础语法是什么', 'JavaScript,JS,语法,基础', 4, 1),
('写代码规则', 'keyword', '写代码', '写代码', '写代码,编程,开发,编写', 5, 1);
