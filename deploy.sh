#!/bin/bash

# 标签体系管理系统部署脚本
# 用于快速部署到生产环境

set -e

echo "=========================================="
echo "标签体系管理系统 - 部署脚本"
echo "=========================================="

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检查是否为 root 用户
if [ "$EUID" -ne 0 ]; then 
    echo -e "${RED}请使用 root 权限运行此脚本${NC}"
    echo "使用: sudo ./deploy.sh"
    exit 1
fi

# 获取项目根目录
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo -e "${GREEN}项目目录: ${PROJECT_DIR}${NC}"

# 1. 检查依赖
echo -e "\n${YELLOW}[1/6] 检查系统依赖...${NC}"
command -v python3 >/dev/null 2>&1 || { echo -e "${RED}需要安装 Python 3${NC}"; exit 1; }
command -v pip3 >/dev/null 2>&1 || { echo -e "${RED}需要安装 pip3${NC}"; exit 1; }
command -v nginx >/dev/null 2>&1 || { echo -e "${YELLOW}建议安装 Nginx 用于反向代理${NC}"; }

echo -e "${GREEN}✓ 系统依赖检查完成${NC}"

# 2. 安装 Python 依赖
echo -e "\n${YELLOW}[2/6] 安装 Python 依赖...${NC}"
cd "${PROJECT_DIR}/backend"
pip3 install -r requirements.txt
echo -e "${GREEN}✓ Python 依赖安装完成${NC}"

# 3. 配置环境变量
echo -e "\n${YELLOW}[3/6] 配置环境变量...${NC}"
if [ ! -f "${PROJECT_DIR}/backend/.env" ]; then
    if [ -f "${PROJECT_DIR}/backend/env.example" ]; then
        cp "${PROJECT_DIR}/backend/env.example" "${PROJECT_DIR}/backend/.env"
        echo -e "${YELLOW}已创建 .env 文件，请根据实际情况修改配置${NC}"
        echo -e "${YELLOW}配置文件位置: ${PROJECT_DIR}/backend/.env${NC}"
    else
        echo -e "${RED}未找到 env.example 文件${NC}"
    fi
else
    echo -e "${GREEN}✓ .env 文件已存在${NC}"
fi

# 4. 初始化数据库
echo -e "\n${YELLOW}[4/6] 初始化数据库...${NC}"
if [ -f "${PROJECT_DIR}/backend/init_db.py" ]; then
    cd "${PROJECT_DIR}/backend"
    python3 init_db.py
    echo -e "${GREEN}✓ 数据库初始化完成${NC}"
else
    echo -e "${YELLOW}未找到数据库初始化脚本，跳过此步骤${NC}"
fi

# 5. 配置 Nginx（可选）
echo -e "\n${YELLOW}[5/6] 配置 Nginx...${NC}"
if command -v nginx >/dev/null 2>&1; then
    read -p "是否配置 Nginx 反向代理? (y/n): " configure_nginx
    if [ "$configure_nginx" = "y" ]; then
        read -p "请输入域名 (例如: example.com): " domain_name
        
        # 创建 Nginx 配置
        nginx_config="/etc/nginx/sites-available/label-system"
        cp "${PROJECT_DIR}/nginx.conf.example" "$nginx_config"
        
        # 替换域名和路径
        sed -i "s|yourdomain.com|${domain_name}|g" "$nginx_config"
        sed -i "s|/path/to/manager_desktop|${PROJECT_DIR}|g" "$nginx_config"
        
        # 创建软链接
        ln -sf "$nginx_config" /etc/nginx/sites-enabled/label-system
        
        # 测试配置
        nginx -t
        
        # 重启 Nginx
        systemctl restart nginx
        
        echo -e "${GREEN}✓ Nginx 配置完成${NC}"
        echo -e "${GREEN}访问地址: http://${domain_name}${NC}"
    else
        echo -e "${YELLOW}跳过 Nginx 配置${NC}"
    fi
else
    echo -e "${YELLOW}未安装 Nginx，跳过此步骤${NC}"
fi

# 6. 创建 systemd 服务（可选）
echo -e "\n${YELLOW}[6/6] 配置系统服务...${NC}"
read -p "是否创建 systemd 服务以自动启动? (y/n): " create_service
if [ "$create_service" = "y" ]; then
    service_file="/etc/systemd/system/label-system.service"
    
    cat > "$service_file" <<EOF
[Unit]
Description=Label System Management Service
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=${PROJECT_DIR}
ExecStart=/usr/bin/python3 ${PROJECT_DIR}/start_backend.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

    # 重新加载 systemd
    systemctl daemon-reload
    
    # 启动服务
    systemctl start label-system
    
    # 设置开机自启
    systemctl enable label-system
    
    echo -e "${GREEN}✓ 系统服务配置完成${NC}"
    echo -e "${GREEN}服务状态: systemctl status label-system${NC}"
    echo -e "${GREEN}查看日志: journalctl -u label-system -f${NC}"
else
    echo -e "${YELLOW}跳过系统服务配置${NC}"
    echo -e "${YELLOW}手动启动: cd ${PROJECT_DIR} && python3 start_backend.py${NC}"
fi

# 完成
echo -e "\n=========================================="
echo -e "${GREEN}部署完成！${NC}"
echo -e "=========================================="
echo -e "\n${YELLOW}后续步骤:${NC}"
echo -e "1. 检查并修改配置文件: ${PROJECT_DIR}/backend/.env"
echo -e "2. 如果使用 systemd 服务:"
echo -e "   - 启动: systemctl start label-system"
echo -e "   - 停止: systemctl stop label-system"
echo -e "   - 重启: systemctl restart label-system"
echo -e "   - 状态: systemctl status label-system"
echo -e "3. 如果手动启动:"
echo -e "   - cd ${PROJECT_DIR} && python3 start_backend.py"
echo -e "4. 访问应用:"
echo -e "   - API 文档: http://your-domain/docs"
echo -e "   - 前端页面: http://your-domain/"
echo -e "\n${YELLOW}注意事项:${NC}"
echo -e "- 确保防火墙开放了 80 和 8000 端口"
echo -e "- 生产环境建议使用 HTTPS"
echo -e "- 定期备份数据库"
echo ""
