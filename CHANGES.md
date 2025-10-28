# 公网部署适配修改说明

## 修改日期
2024-10-22

## 问题描述
系统在公网部署后，前端无法访问后端 API，因为前端代码中硬编码了 `http://localhost:8000`，导致从互联网访问时无法连接到后端服务。

## 解决方案
将前端 API 地址从硬编码的 localhost 改为使用相对路径，自动适配当前访问的域名。

## 修改文件列表

### 1. 前端配置文件

#### 新增文件：`web/js/config.js`
- **作用**: 统一管理前端配置，包括 API 基础 URL
- **默认配置**: 使用相对路径 `/api/v1`
- **灵活性**: 可以在页面加载前通过 `window.API_BASE_URL` 自定义 API 地址

#### 修改文件：`web/js/api.js`
- **修改内容**: 
  - 原代码: `constructor(baseURL = 'http://localhost:8000/api/v1')`
  - 新代码: `constructor(baseURL = null)` + 自动从 `window.API_BASE_URL` 或使用默认值 `/api/v1`
- **优势**: 支持多种配置方式，优先级为：传入参数 > 环境变量 > 相对路径

#### 修改文件：`web/tag-system-list.html`
- **修改内容**:
  - 原代码: `const API_BASE_URL = 'http://localhost:8000/api/v1';`
  - 新代码: `const API_BASE_URL = '/api/v1';`
  - 新增: `<script src="js/config.js"></script>` 引用
- **效果**: 使用相对路径，自动适配当前域名

#### 修改文件：`web/customer-service-intent-system.html`
- **修改内容**: 在 `<head>` 中添加 `<script src="js/config.js"></script>`
- **效果**: 确保该页面也能使用统一的配置

#### 修改文件：`web/product-tag-system-updated.html`
- **修改内容**: 在 `<head>` 中添加 `<script src="js/config.js"></script>`
- **效果**: 确保该页面也能使用统一的配置

### 2. 部署文档

#### 新增文件：`DEPLOYMENT.md`
- **内容**: 详细的公网部署指南
- **包含**:
  - 前后端同域部署方案（推荐）
  - 前后端分离部署方案
  - Nginx 配置说明
  - 环境变量配置
  - 常见问题解决
  - Docker 部署（可选）
  - 安全建议
  - 性能优化

#### 新增文件：`nginx.conf.example`
- **内容**: Nginx 反向代理配置示例
- **功能**:
  - 前端静态文件服务
  - 后端 API 反向代理
  - 静态资源缓存
  - WebSocket 支持
  - 健康检查

#### 新增文件：`deploy.sh`
- **内容**: 自动化部署脚本
- **功能**:
  - 检查系统依赖
  - 安装 Python 依赖
  - 配置环境变量
  - 初始化数据库
  - 配置 Nginx（可选）
  - 创建 systemd 服务（可选）

#### 修改文件：`README.md`
- **修改内容**: 添加"公网部署"章节
- **包含**: 快速部署步骤和文档链接

## 技术实现

### 相对路径原理
当前端使用相对路径 `/api/v1` 时：
- 如果访问 `http://example.com/`，API 请求会发送到 `http://example.com/api/v1`
- 如果访问 `https://example.com/`，API 请求会发送到 `https://example.com/api/v1`
- 自动适配协议（HTTP/HTTPS）和域名

### 配置优先级
```javascript
// 1. 传入的 baseURL（最高优先级）
const api = new LabelSystemAPI('https://custom-api.com/api/v1');

// 2. window.API_BASE_URL（环境变量）
window.API_BASE_URL = 'https://api.example.com/api/v1';
const api = new LabelSystemAPI();

// 3. 默认相对路径（最低优先级）
const api = new LabelSystemAPI(); // 使用 '/api/v1'
```

## 部署方式

### 方式一：前后端同域部署（推荐）
```
域名: example.com
前端: example.com/ (Nginx 静态文件服务)
后端: example.com/api/ (Nginx 反向代理到 localhost:8000)
```

**优势**:
- 无需配置 CORS
- 使用相对路径，无需修改代码
- 部署简单

### 方式二：前后端分离部署
```
前端: frontend.example.com
后端: api.example.com
```

**配置**:
```javascript
// 在 web/js/config.js 中修改
window.API_BASE_URL = 'https://api.example.com/api/v1';
```

**注意**:
- 需要配置 CORS
- 后端 `ALLOWED_HOSTS` 需要包含前端域名

## 验证步骤

### 1. 本地测试
```bash
# 启动后端
python start_backend.py

# 访问前端
open http://localhost:8000/static/tag-system-list.html
```

### 2. 公网测试
```bash
# 检查后端健康
curl http://your-domain.com/health

# 检查 API
curl http://your-domain.com/api/v1/systems

# 浏览器访问
open http://your-domain.com/
```

### 3. 浏览器调试
打开浏览器开发者工具（F12）：
- **Network** 标签: 查看 API 请求是否正确
- **Console** 标签: 查看是否有错误信息
- 确认 API 请求的 URL 是否正确

## 后续维护

### 修改 API 地址
如果需要修改 API 地址，有三种方式：

1. **修改配置文件**（推荐）:
   ```javascript
   // 编辑 web/js/config.js
   window.API_BASE_URL = 'https://new-api.example.com/api/v1';
   ```

2. **在页面中设置**:
   ```html
   <script>
       window.API_BASE_URL = 'https://new-api.example.com/api/v1';
   </script>
   <script src="js/config.js"></script>
   ```

3. **使用 Nginx 反向代理**（无需修改代码）:
   ```nginx
   location /api/ {
       proxy_pass http://backend-server:8000;
   }
   ```

### 环境切换
可以根据不同环境使用不同的配置：

```javascript
// 开发环境
if (window.location.hostname === 'localhost') {
    window.API_BASE_URL = 'http://localhost:8000/api/v1';
}
// 测试环境
else if (window.location.hostname === 'test.example.com') {
    window.API_BASE_URL = 'https://test-api.example.com/api/v1';
}
// 生产环境
else {
    window.API_BASE_URL = '/api/v1'; // 使用相对路径
}
```

## 注意事项

1. **CORS 配置**: 如果前后端分离部署，确保后端 CORS 配置正确
2. **HTTPS**: 生产环境建议使用 HTTPS
3. **防火墙**: 确保开放必要的端口（80, 443, 8000）
4. **缓存**: 修改配置后可能需要清除浏览器缓存
5. **日志**: 定期检查后端日志，监控异常访问

## 回滚方案

如果需要回滚到原来的配置：

1. 恢复 `web/js/api.js`:
   ```javascript
   constructor(baseURL = 'http://localhost:8000/api/v1')
   ```

2. 恢复 `web/tag-system-list.html`:
   ```javascript
   const API_BASE_URL = 'http://localhost:8000/api/v1';
   ```

3. 删除 `web/js/config.js` 的引用

## 总结

本次修改实现了前端 API 地址的灵活配置，支持：
- ✅ 本地开发环境
- ✅ 公网部署（同域）
- ✅ 公网部署（跨域）
- ✅ 多环境切换
- ✅ 自定义 API 地址

修改后的系统可以在任何环境下部署，无需修改代码，只需通过配置文件或 Nginx 反向代理即可适配不同的部署场景。
