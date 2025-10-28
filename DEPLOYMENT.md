# 部署指南

## 公网部署配置说明

本系统已经修改为支持公网部署，前端使用相对路径自动适配当前域名。

### 修改内容

#### 1. 前端配置
- **修改文件**: `web/js/api.js`, `web/tag-system-list.html`
- **修改内容**: 将硬编码的 `http://localhost:8000` 改为相对路径 `/api/v1`
- **新增文件**: `web/js/config.js` - 前端配置文件

#### 2. 配置文件说明

**`web/js/config.js`**:
```javascript
// 默认使用相对路径（推荐）
window.API_BASE_URL = window.API_BASE_URL || '/api/v1';
```

如果需要指定特定的 API 地址，可以在加载 `config.js` 之前设置：
```html
<script>
    // 开发环境
    window.API_BASE_URL = 'http://localhost:8000/api/v1';
    
    // 或者指定其他域名
    window.API_BASE_URL = 'https://api.yourdomain.com/api/v1';
</script>
<script src="js/config.js"></script>
```

### 部署步骤

#### 方案一：前后端同域部署（推荐）

前端和后端部署在同一个域名下，使用 Nginx 反向代理：

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    # 前端静态文件
    location / {
        root /path/to/manager_desktop/web;
        index tag-system-list.html;
        try_files $uri $uri/ /tag-system-list.html;
    }

    # 后端 API 代理
    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # 静态文件（如果后端也提供静态文件）
    location /static/ {
        proxy_pass http://127.0.0.1:8000/static/;
    }
}
```

**启动后端**:
```bash
cd /path/to/manager_desktop
python start_backend.py
```

#### 方案二：前后端分离部署

如果前端和后端部署在不同的域名，需要修改 `web/js/config.js`：

```javascript
// 指定后端 API 完整地址
window.API_BASE_URL = 'https://api.yourdomain.com/api/v1';
```

**后端配置**（确保 CORS 配置正确）:

编辑 `backend/.env` 文件：
```env
# 允许的跨域来源（多个用逗号分隔）
ALLOWED_HOSTS=https://frontend.yourdomain.com,https://www.yourdomain.com
```

或者在 `backend/app/core/config.py` 中修改：
```python
ALLOWED_HOSTS: List[str] = ["*"]  # 允许所有来源（不推荐生产环境）
# 或者指定具体域名
ALLOWED_HOSTS: List[str] = ["https://frontend.yourdomain.com"]
```

### 环境变量配置

创建 `backend/.env` 文件：

```env
# 应用配置
APP_NAME=标签体系管理系统
DEBUG=false

# 服务器配置
HOST=0.0.0.0
PORT=8000

# 数据库配置
DATABASE_URL=sqlite:///label_system.db
# 或使用 MySQL
# DATABASE_URL=mysql+pymysql://user:password@host:3306/database

# CORS 配置
ALLOWED_HOSTS=*
# 生产环境建议指定具体域名
# ALLOWED_HOSTS=https://yourdomain.com,https://www.yourdomain.com

# JWT 配置
SECRET_KEY=your-secret-key-change-in-production
```

### 验证部署

1. **检查后端服务**:
```bash
curl http://your-domain.com/health
# 应该返回: {"status": "healthy", "message": "服务运行正常"}
```

2. **检查 API**:
```bash
curl http://your-domain.com/api/v1/systems
# 应该返回标签体系列表
```

3. **访问前端**:
```
http://your-domain.com/
或
http://your-domain.com/tag-system-list.html
```

### 常见问题

#### 1. 跨域问题
**症状**: 浏览器控制台显示 CORS 错误

**解决方案**:
- 检查后端 `ALLOWED_HOSTS` 配置
- 确保包含前端域名
- 或者使用 Nginx 反向代理，前后端同域部署

#### 2. API 404 错误
**症状**: 前端无法获取数据，API 返回 404

**解决方案**:
- 检查 `web/js/config.js` 中的 `API_BASE_URL` 配置
- 确保后端服务正常运行
- 检查 Nginx 配置中的 proxy_pass 路径

#### 3. 静态文件无法加载
**症状**: 页面样式错误，js/css 文件 404

**解决方案**:
- 检查 Nginx 配置中的 root 路径
- 确保 `web/js/config.js` 和 `web/js/api.js` 文件存在
- 检查文件权限

### 使用 Docker 部署（可选）

创建 `Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "start_backend.py"]
```

构建和运行:
```bash
docker build -t label-system .
docker run -d -p 8000:8000 label-system
```

### 安全建议

1. **生产环境配置**:
   - 设置强密码的 `SECRET_KEY`
   - 限制 `ALLOWED_HOSTS` 为具体域名
   - 使用 HTTPS
   - 配置防火墙规则

2. **数据库安全**:
   - 使用强密码
   - 限制数据库访问 IP
   - 定期备份数据

3. **日志监控**:
   - 定期检查 `logs/app.log`
   - 配置日志轮转
   - 监控异常访问

### 性能优化

1. **使用 Gunicorn 运行后端**:
```bash
gunicorn backend.app.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

2. **启用 Nginx 缓存**:
```nginx
location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}
```

3. **使用 CDN**:
   - 将静态资源部署到 CDN
   - 减少服务器负载

---

更新时间: 2024-10-22
