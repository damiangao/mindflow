# Mindflow 部署指南

## 部署概览

本指南提供在自建Linux服务器上部署Mindflow的完整说明。系统设计为完全自托管，所有数据存储在本地，不依赖外部云服务。

## 部署架构

```
用户的Linux服务器
    │
    ├── Docker 容器
    │   ├── Gradio 应用 (Python)
    │   └── SQLite 数据库
    │
    └── 环境配置 (.env)
```

## 系统要求

### 最低要求
- **CPU**: 2核
- **内存**: 2GB RAM
- **存储**: 10GB（包括操作系统）
- **操作系统**: Ubuntu 20.04 LTS 或更高版本，或其他Linux发行版
- **网络**: 固定IP地址或域名

### 推荐配置
- **CPU**: 4核
- **内存**: 4GB RAM
- **存储**: 20GB SSD
- **操作系统**: Ubuntu 22.04 LTS

## 前置条件

### 1. 安装Docker

```bash
# 更新包管理器
sudo apt update
sudo apt upgrade -y

# 安装Docker
sudo apt install -y docker.io docker-compose

# 验证安装
docker --version
docker-compose --version

# 将当前用户添加到docker组（可选，避免每次使用sudo）
sudo usermod -aG docker $USER
# 需要重新登录才能生效
```

### 2. 安装Git（如需要从GitHub克隆）

```bash
sudo apt install -y git
git --version
```

### 3. 配置固定IP（如果需要）

```bash
# 编辑网络配置
sudo nano /etc/netplan/00-installer-config.yaml

# 示例配置（取决于你的网络设置）
# 添加静态IP配置后保存

# 应用配置
sudo netplan apply

# 验证
ip addr show
```

## 部署步骤

### Step 1: 获取应用代码

**选项A: 从GitHub克隆（推荐）**
```bash
cd /opt
sudo git clone https://github.com/yourusername/mindflow.git
sudo chown -R $USER:$USER mindflow
cd mindflow
```

**选项B: 上传本地文件**
```bash
# 从本地机器上传
scp -r /local/path/to/mindflow user@server:/opt/

# 在服务器上
cd /opt/mindflow
```

### Step 2: 配置环境变量

```bash
# 进入应用目录
cd /opt/mindflow

# 复制示例文件
cp .env.example .env

# 编辑配置
nano .env
```

编辑以下关键变量：

```bash
# ============================================
# LLM 配置
# ============================================
LLM_PROVIDER=claude
CLAUDE_API_KEY=your_api_key_here
CLAUDE_MODEL=claude-3-5-haiku-20241022

# 或者使用其他LLM
# LLM_PROVIDER=openai
# OPENAI_API_KEY=your_api_key_here

# ============================================
# 应用配置
# ============================================
APP_NAME=Mindflow
APP_PORT=7860
LOG_LEVEL=INFO

# ============================================
# 数据库配置
# ============================================
DATABASE_URL=sqlite:///./data/mindflow.db
DATABASE_PATH=/app/data

# ============================================
# 安全配置
# ============================================
SECRET_KEY=your_secret_key_here
# 建议使用: python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Step 3: 构建Docker镜像

```bash
# 确保在mindflow目录
cd /opt/mindflow

# 构建镜像
docker build -t mindflow:latest .

# 验证镜像
docker images | grep mindflow
```

### Step 4: 创建数据目录

```bash
# 创建数据存储目录
mkdir -p /opt/mindflow/data

# 设置权限（使Docker能够访问）
sudo chown -R 1000:1000 /opt/mindflow/data
```

### Step 5: 启动容器

**选项A: 使用Docker Compose（推荐）**

```bash
# 创建或编辑 docker-compose.yml
cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  mindflow:
    image: mindflow:latest
    container_name: mindflow
    ports:
      - "7860:7860"
    volumes:
      - ./data:/app/data
    environment:
      - LLM_PROVIDER=${LLM_PROVIDER}
      - CLAUDE_API_KEY=${CLAUDE_API_KEY}
      - APP_PORT=7860
      - DATABASE_URL=sqlite:///./data/mindflow.db
    restart: always
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:7860/"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

volumes:
  data:
EOF

# 启动服务
docker-compose up -d

# 查看日志
docker-compose logs -f
```

**选项B: 直接使用Docker命令**

```bash
docker run -d \
  --name mindflow \
  -p 7860:7860 \
  -v /opt/mindflow/data:/app/data \
  --env-file .env \
  --restart always \
  mindflow:latest
```

### Step 6: 验证部署

```bash
# 检查容器状态
docker ps | grep mindflow

# 查看容器日志
docker logs mindflow

# 测试应用访问
curl http://localhost:7860
```

## 访问应用

### 本地访问
```
http://localhost:7860
```

### 远程访问

**通过服务器IP**：
```
http://your_server_ip:7860
```

**通过域名**（如已配置）：
```
http://your_domain.com:7860
```

### 配置反向代理（可选但推荐）

**使用Nginx**：

```bash
# 安装Nginx
sudo apt install -y nginx

# 创建配置文件
sudo nano /etc/nginx/sites-available/mindflow
```

配置内容：
```nginx
server {
    listen 80;
    server_name your_domain.com;  # 或你的IP

    location / {
        proxy_pass http://localhost:7860;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

启用配置：
```bash
sudo ln -s /etc/nginx/sites-available/mindflow /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 配置HTTPS（推荐）

使用Let's Encrypt和Certbot：

```bash
# 安装Certbot
sudo apt install -y certbot python3-certbot-nginx

# 获取证书
sudo certbot --nginx -d your_domain.com

# 自动续期（已默认配置）
```

## 持久化和备份

### 数据位置

所有数据存储在：
```
/opt/mindflow/data/mindflow.db
```

### 自动备份脚本

创建备份脚本：

```bash
# 创建备份目录
mkdir -p /opt/mindflow/backups

# 创建备份脚本
cat > /opt/mindflow/backup.sh << 'EOF'
#!/bin/bash

# 备份数据库
BACKUP_DIR="/opt/mindflow/backups"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/mindflow_backup_$DATE.db"

# 创建备份
cp /opt/mindflow/data/mindflow.db "$BACKUP_FILE"

# 保留最近30天的备份
find "$BACKUP_DIR" -name "mindflow_backup_*.db" -mtime +30 -delete

echo "Backup completed: $BACKUP_FILE"
EOF

# 使脚本可执行
chmod +x /opt/mindflow/backup.sh
```

配置定时备份：

```bash
# 编辑cron任务
crontab -e

# 添加每日备份任务（每天凌晨2点）
0 2 * * * /opt/mindflow/backup.sh >> /opt/mindflow/logs/backup.log 2>&1
```

### 手动备份

```bash
# 备份数据库
cp /opt/mindflow/data/mindflow.db /opt/mindflow/backups/mindflow_$(date +%Y%m%d).db

# 备份整个应用目录
tar -czf mindflow_backup_$(date +%Y%m%d).tar.gz /opt/mindflow/
```

### 恢复备份

```bash
# 停止容器
docker-compose down

# 恢复数据库
cp /opt/mindflow/backups/mindflow_BACKUP_DATE.db /opt/mindflow/data/mindflow.db

# 重启容器
docker-compose up -d
```

## 维护和监控

### 查看日志

```bash
# 实时日志
docker-compose logs -f

# 特定容器日志
docker logs -f mindflow

# 查看特定数量的行
docker logs --tail 100 mindflow
```

### 系统监控

```bash
# 查看容器资源使用
docker stats mindflow

# 查看磁盘使用
du -sh /opt/mindflow/

# 查看数据库大小
ls -lh /opt/mindflow/data/mindflow.db
```

### 定期维护

```bash
# 清理Docker缓存
docker system prune

# 更新基础镜像
docker pull mindflow:latest

# 重建镜像（如代码更新）
docker-compose down
docker build -t mindflow:latest .
docker-compose up -d
```

## 更新应用

### 从GitHub更新

```bash
cd /opt/mindflow

# 拉取最新代码
git pull origin main

# 重建镜像
docker build -t mindflow:latest .

# 重启容器
docker-compose restart
```

### 零停机更新

```bash
# 如果需要零停机时间，使用蓝绿部署或金丝雀部署策略
# 为此需要额外的负载均衡器配置
```

## 故障排除

### 容器无法启动

```bash
# 查看错误日志
docker logs mindflow

# 检查配置文件
cat .env

# 检查端口是否被占用
sudo lsof -i :7860
```

### 应用响应缓慢

```bash
# 检查系统资源
docker stats

# 检查数据库大小
ls -lh /opt/mindflow/data/mindflow.db

# 考虑优化数据库查询或升级硬件
```

### 无法连接到LLM API

```bash
# 验证API密钥
echo $CLAUDE_API_KEY

# 测试网络连接
curl -I https://api.anthropic.com

# 检查防火墙
sudo ufw status
```

### 存储空间不足

```bash
# 检查磁盘使用
df -h

# 清理旧备份
rm /opt/mindflow/backups/mindflow_backup_*.db

# 如果数据库太大，考虑归档旧数据
```

## 安全建议

### 1. 防火墙配置

```bash
# 安装ufw（如未安装）
sudo apt install -y ufw

# 默认规则
sudo ufw default deny incoming
sudo ufw default allow outgoing

# 允许SSH
sudo ufw allow 22/tcp

# 允许HTTP/HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# 启用防火墙
sudo ufw enable
```

### 2. API密钥管理

- 不要在代码中硬编码API密钥
- 使用`.env`文件（已在`.gitignore`中）
- 定期轮换API密钥
- 限制API密钥的权限范围

### 3. 定期更新

```bash
# 更新系统包
sudo apt update && sudo apt upgrade -y

# 更新Docker镜像基础
docker pull ubuntu:22.04  # 如果使用Ubuntu基础镜像
```

### 4. 监控和告警

```bash
# 监控磁盘空间
watch -n 10 'df -h'

# 监控容器状态
watch 'docker ps | grep mindflow'
```

## 性能优化

### Docker容器资源限制

```yaml
# docker-compose.yml
services:
  mindflow:
    # ... 其他配置 ...
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
        reservations:
          cpus: '1'
          memory: 1G
```

### 数据库优化

```bash
# 为SQLite优化
# 增加缓存大小、页面大小等
```

### 缓存策略

- 实现LLM响应缓存
- 使用Redis（如需要）
- 优化前端资源加载

## 扩展部署

### 多实例部署

使用Docker Swarm或Kubernetes实现高可用部署（超出MVP范围）。

### 升级到PostgreSQL

参考 [DATABASE.md](DATABASE.md) 中的升级路径。

## 常见问题

**Q: 如何更改应用端口？**
```bash
# 编辑 .env
APP_PORT=8000

# 编辑 docker-compose.yml
ports:
  - "8000:8000"
```

**Q: 如何进行数据库备份和恢复？**
```bash
# 参考本文档的"持久化和备份"部分
```

**Q: 如何监控系统健康状态？**
```bash
# 使用 healthcheck 部分的配置
docker inspect mindflow | grep -A 5 Health
```

**Q: 如何处理存储空间限制？**
```bash
# 定期清理备份
# 考虑升级存储
# 或者只保留最近N天的数据
```

## 参考资源

- [Docker官方文档](https://docs.docker.com/)
- [Docker Compose文档](https://docs.docker.com/compose/)
- [Nginx反向代理](https://nginx.org/en/docs/)
- [Let's Encrypt](https://letsencrypt.org/)
- [Linux系统管理](https://wiki.archlinux.org/)

## 支持

如遇到问题，请：
1. 查看本文档的故障排除部分
2. 检查应用日志
3. 提交Issue到GitHub仓库
