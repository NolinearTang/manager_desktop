# 标签体系管理系统

基于意图识别的智能标签体系管理平台，支持多层级标签管理、规则配置和智能意图识别。

## 📁 项目结构

```
manager_desktop/
├── web/                                    # 前端静态文件
│   ├── tag-system-list.html               # 标签体系列表页面
│   ├── customer-service-intent-system.html # 客服对话意图体系页面
│   └── product-tag-system-updated.html    # 产品标签体系页面
├── backend/                               # 后端服务
│   ├── app/
│   │   ├── api/                          # API路由
│   │   ├── core/                         # 核心配置
│   │   ├── models/                       # 数据模型
│   │   ├── services/                     # 业务逻辑
│   │   └── utils/                        # 工具函数
│   ├── tests/                            # 测试文件
│   ├── docs/                             # 文档
│   └── requirements.txt                  # Python依赖
├── database_schema.sql                   # 数据库设计
├── api_design.md                         # API设计文档
└── README.md                             # 项目说明
```

## 🗄️ 数据库设计

### 核心表结构

1. **标签体系表 (label_system)**
   - 存储标签的层级关系和基本信息
   - 支持意图标签、实体标签、分类标签三种类型

2. **规则管理表 (rule_management)**
   - 存储意图识别规则
   - 支持表达式、表达句、关键词三种规则类型

3. **实体标签映射表 (entity_tag_mapping)**
   - 存储实体标签的具体值
   - 支持动态实体标签扩展

4. **数据信息表 (item_data)**
   - 存储具体的实体数据项
   - 支持同义词和元数据管理

5. **标签体系关联表 (label_item_relation)**
   - 关联标签和具体数据项
   - 支持多种关联类型和权重

## 🚀 快速开始

### 环境要求

- Python 3.8+
- MySQL 5.7+ 或 PostgreSQL 12+
- Redis 6.0+

### 安装步骤

1. **克隆项目**
   ```bash
   git clone <repository-url>
   cd manager_desktop
   ```

2. **安装后端依赖**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. **配置数据库**
   ```bash
   # 创建数据库
   mysql -u root -p
   CREATE DATABASE label_system;
   
   # 导入数据库结构
   mysql -u root -p label_system < ../database_schema.sql
   ```

4. **配置环境变量**
   ```bash
   cp .env.example .env
   # 编辑 .env 文件，配置数据库连接等信息
   ```

5. **启动后端服务**
   ```bash
   cd backend
   python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

6. **访问应用**
   - API文档: http://localhost:8000/docs
   - 前端页面: http://localhost:8000/static/tag-system-list.html

## 📋 功能特性

### 标签管理
- ✅ 多层级标签体系管理
- ✅ 标签类型分类（意图、实体、分类）
- ✅ 标签的增删改查操作
- ✅ 标签层级关系维护

### 规则管理
- ✅ 三种规则类型支持（表达式、表达句、关键词）
- ✅ 实体标签引用支持（如 `{故障码}`、`{产品型号}`）
- ✅ 规则优先级管理
- ✅ 规则启用/禁用控制

### 意图识别
- ✅ 基于规则的智能意图识别
- ✅ 实体标签自动提取
- ✅ 多规则匹配和置信度计算
- ✅ 意图识别结果和建议

### 数据管理
- ✅ 实体数据项管理
- ✅ 同义词和元数据支持
- ✅ 标签与数据项关联
- ✅ 数据导入导出功能

## 🔧 API接口

### 标签管理
- `GET /api/v1/labels` - 获取标签列表
- `POST /api/v1/labels` - 创建标签
- `PUT /api/v1/labels/{id}` - 更新标签
- `DELETE /api/v1/labels/{id}` - 删除标签

### 规则管理
- `GET /api/v1/rules` - 获取规则列表
- `POST /api/v1/rules` - 创建规则
- `PUT /api/v1/rules/{id}` - 更新规则
- `DELETE /api/v1/rules/{id}` - 删除规则

### 意图识别
- `POST /api/v1/intent-recognition` - 意图识别接口

详细API文档请参考 [api_design.md](api_design.md)

## 🎯 使用场景

### 客服对话意图识别
- 自动识别用户问题类型（知识问答、代码相关、无意义等）
- 提取关键实体信息（故障码、产品型号等）
- 提供智能回复建议

### 产品标签管理
- 管理产品相关的实体标签
- 支持产品型号、规格等信息的结构化存储
- 实现产品信息的智能检索

### 规则配置管理
- 灵活配置意图识别规则
- 支持多种规则类型和实体标签引用
- 实现规则的动态调整和优化

## 🛠️ 技术栈

### 前端
- HTML5 + CSS3
- Tailwind CSS
- Font Awesome
- JavaScript (ES6+)

### 后端
- Python 3.8+
- FastAPI
- SQLAlchemy
- Redis
- MySQL/PostgreSQL

### 部署
- Docker (可选)
- Nginx (可选)
- Gunicorn (生产环境)

## 📝 开发计划

- [ ] 完善后端API实现
- [ ] 添加用户认证和权限管理
- [ ] 实现数据导入导出功能
- [ ] 添加规则测试和调试工具
- [ ] 实现意图识别性能优化
- [ ] 添加系统监控和日志分析
- [ ] 完善单元测试和集成测试
- [ ] 添加Docker容器化部署

## 🤝 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 📞 联系方式

如有问题或建议，请通过以下方式联系：

- 项目Issues: [GitHub Issues](https://github.com/your-repo/issues)
- 邮箱: your-email@example.com

---

**标签体系管理系统** - 让意图识别更智能，让标签管理更简单！
