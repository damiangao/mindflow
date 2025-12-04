# Phase 1 学习指南 + 部署步骤

## 📚 第一部分：Phase 1 技术栈学习路线

你说得对，Phase 1 的代码已经完成了，现在需要理解实现细节。这份指南会帮你逐步学习相关技术。

### 🎯 学习优先级和时间规划

**总体时间**: 2-3 周掌握核心概念，可以开始参与开发

| 优先级 | 技术 | 时间 | 难度 | 为什么需要 |
|--------|------|------|------|----------|
| ⭐⭐⭐⭐⭐ | Python 基础 | 1-2周 | 中 | Phase 1 所有代码都是 Python |
| ⭐⭐⭐⭐⭐ | Gradio | 3-5天 | 简 | src/ui/main.py 的 Web 应用框架 |
| ⭐⭐⭐⭐⭐ | SQLAlchemy ORM | 1周 | 中 | src/database/models.py 的数据库模型 |
| ⭐⭐⭐⭐ | SQLite + SQL | 3-5天 | 中 | 理解数据库如何存储数据 |
| ⭐⭐⭐⭐ | LangGraph 基础 | 1-2周 | 中-难 | Phase 2 会用到，现在理解架构 |
| ⭐⭐⭐⭐ | Claude API | 2-3天 | 简 | src/llm/claude.py 如何调用 API |
| ⭐⭐⭐ | Docker | 3-5天 | 简-中 | 部署到服务器 |
| ⭐⭐⭐ | Linux 基础 | 持续 | 中 | 在你的服务器上运行 |

---

## 📖 详细学习路线

### 第 1 周：Python 基础 + Gradio 快速入门

#### 学习目标
能读懂 Phase 1 的代码，理解类、装饰器、函数式编程

#### 1. Python 基础（3天）

**必须掌握的概念**：
```python
# 1. 类和对象 (src/config.py, src/database/models.py 都用了)
class Settings:
    def __init__(self, name: str):
        self.name = name

# 2. 装饰器 (Gradio 的 @gr.Interface 用了)
def my_decorator(func):
    def wrapper(*args, **kwargs):
        print("Before")
        result = func(*args, **kwargs)
        print("After")
        return result
    return wrapper

# 3. 类型提示 (Phase 1 代码到处都用了)
def get_session(self) -> Session:
    return self.SessionLocal()

# 4. 异常处理
try:
    provider = LLMConfig.get_provider()
except ValueError as e:
    print(f"Error: {e}")

# 5. with 语句 (数据库连接用)
with database.get_session() as session:
    user = session.query(User).first()
```

**推荐资源**：
- 官方文档：https://docs.python.org/3/
- 快速教程：https://www.learnpython.org/
- 视频教学：菜鸟教程 Python 教程

**检验方法**：
- [ ] 能理解 src/config.py 中 Settings 类的定义
- [ ] 能理解 src/llm/provider.py 中 @abstractmethod 装饰器
- [ ] 能读懂 src/database/models.py 中的类型提示

---

#### 2. Gradio 快速入门（2-3天）

**学习路径**：
1. **Gradio 是什么？** - 快速构建 Web UI 的 Python 框架（无需 JavaScript）
2. **基础组件** - Textbox, Button, DataFrame, Dropdown 等
3. **事件处理** - 按钮点击、文本输入等触发的函数
4. **布局** - Rows, Columns, Tabs 组织界面
5. **在 Phase 1 中的应用** - 查看 src/ui/main.py

**核心概念示例**：
```python
# src/ui/main.py 的结构
import gradio as gr

with gr.Blocks() as demo:  # 创建应用

    with gr.Tabs():  # 创建标签页

        with gr.Tab("Tab 1"):  # 第一个标签页
            gr.Markdown("# 标题")

            with gr.Row():  # 一行放两个组件
                input_box = gr.Textbox(label="输入")
                output_box = gr.Textbox(label="输出")

            submit_btn = gr.Button("提交")

            # 点击按钮触发函数
            submit_btn.click(
                fn=process_input,
                inputs=[input_box],
                outputs=[output_box]
            )

demo.launch()  # 启动应用，访问 http://localhost:7860
```

**推荐资源**：
- 官方文档：https://gradio.app/docs
- 官方示例：https://github.com/gradio-app/gradio/tree/main/demo
- 中文教程：搜索 "Gradio 教程"

**实战**：
打开 src/ui/main.py，理解：
- [ ] 5 个 Tab 的结构和组件
- [ ] 按钮点击如何触发函数
- [ ] DataFrame 如何显示数据
- [ ] 下拉菜单（Dropdown）的用法

---

### 第 2 周：数据库 + ORM 理解

#### 学习目标
理解数据如何存储、查询、更新；掌握 SQLAlchemy 的基本用法

#### 3. SQL 基础（2-3天）

**需要理解的 SQL 操作**：
```sql
-- SELECT: 查询数据
SELECT * FROM users WHERE age > 18;

-- INSERT: 插入数据
INSERT INTO users (name, age) VALUES ('张三', 25);

-- UPDATE: 更新数据
UPDATE users SET age = 26 WHERE name = '张三';

-- DELETE: 删除数据
DELETE FROM users WHERE name = '张三';

-- JOIN: 关联查询 (Phase 1 的表有外键关系)
SELECT u.name, e.title
FROM users u
JOIN events e ON u.id = e.user_id;
```

**Phase 1 中用到的表**：
- users (用户档案)
- events (生活事件)
- plans (计划)
- reviews (复盘记录)

**推荐资源**：
- SQLite 官方教程：https://www.sqlite.org/docs.html
- SQL 在线学习：https://sqlzoo.net/
- 菜鸟教程 SQL：https://www.runoob.com/sql/

**检验**：
- [ ] 理解 SELECT, INSERT, UPDATE, DELETE 的用法
- [ ] 理解 JOIN 的概念
- [ ] 理解 WHERE 条件过滤

---

#### 4. SQLAlchemy ORM（3-4天）

**核心概念**：ORM = Object Relational Mapping（将数据库表映射为 Python 对象）

```python
# src/database/models.py 的模式

from sqlalchemy import Column, String, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# 定义模型 = 定义数据库表
class UserProfile(Base):
    __tablename__ = "user_profile"  # 表名

    # 列定义
    id = Column(String(36), primary_key=True)
    name = Column(String(255))
    goals = Column(JSON)  # JSON 类型可存储列表
    created_at = Column(DateTime, default=datetime.utcnow)

    # 关系定义
    events = relationship("Event", back_populates="user")


# 使用模型操作数据（比 SQL 更 Pythonic）
from src.database.connection import get_session

session = get_session()

# Create: 创建
user = UserProfile(
    id="uuid-123",
    name="张三",
    goals=["目标1", "目标2"]
)
session.add(user)
session.commit()

# Read: 读取
user = session.query(UserProfile).filter(UserProfile.name == "张三").first()
print(user.name)

# Update: 更新
user.goals = ["新目标"]
session.commit()

# Delete: 删除
session.delete(user)
session.commit()

session.close()
```

**学习 Phase 1 中的 7 个模型**：

1. **UserProfile** - 用户档案 (src/database/models.py:14-42)
2. **UserBehaviorFeatures** - 用户特征 (src/database/models.py:45-58)
3. **Event** - 生活事件 (src/database/models.py:61-80)
4. **Plan** - 计划 (src/database/models.py:83-105)
5. **PlanUpdate** - 计划更新记录 (src/database/models.py:108-119)
6. **Review** - 每日复盘 (src/database/models.py:122-138)
7. **ConversationHistory** - 对话历史 (src/database/models.py:141-157)

**推荐资源**：
- SQLAlchemy 官方文档：https://docs.sqlalchemy.org/
- SQLAlchemy 中文教程：搜索 "SQLAlchemy 教程"

**检验**：
- [ ] 理解 Column 和不同的数据类型
- [ ] 理解 Primary Key（主键）和 Foreign Key（外键）
- [ ] 理解 relationship（关系）的定义
- [ ] 能读懂 src/database/models.py 中 7 个模型的定义

---

### 第 3 周：LLM + 框架理解

#### 学习目标
理解 Claude API 如何调用；理解 Phase 2 会用到的 LangGraph

#### 5. Claude API 快速入门（2-3天）

**核心概念**：
```python
# src/llm/claude.py 的简化版本

from anthropic import Anthropic

# 创建客户端
client = Anthropic(api_key="sk-ant-...")

# 生成文本
response = client.messages.create(
    model="claude-3-5-haiku-20241022",
    max_tokens=1000,
    messages=[
        {
            "role": "user",
            "content": "请总结这段文本..."
        }
    ]
)

print(response.content[0].text)
```

**Phase 1 中如何使用**：
- src/llm/claude.py 定义了 ClaudeProvider 类
- src/llm/config.py 用工厂模式统一管理所有 LLM 提供商
- 可以通过 `get_llm()` 快速获取 Claude 实例

**推荐资源**：
- Claude API 文档：https://docs.anthropic.com/
- 中文教程：搜索 "Claude API 调用"

**检验**：
- [ ] 理解 API 密钥和模型选择
- [ ] 理解 messages 的结构（role + content）
- [ ] 理解 max_tokens 的概念
- [ ] 能读懂 src/llm/claude.py 的 generate() 和 chat() 方法

---

#### 6. LangGraph 基础概念（理解为主，Phase 2 才深入学习）

**为什么需要 LangGraph？**

```
简单的 LLM 调用：
  输入 → Claude API → 输出

使用 LangGraph 的 Agent：
  输入 → 事件提取Agent → 识别事件
  事件 → 用户画像Agent → 更新特征
  特征 → 计划推动Agent → 生成建议

这些 Agent 可以有复杂的工作流、条件判断、循环等
```

**Phase 1 中的准备**：
- src/agents/ 目录已创建（Phase 2 会填充）
- src/llm/ 提供了 LLM 的接口（LangGraph 会使用）
- src/database/ 提供了数据存储（Agent 的结果会保存）

**推荐资源**：
- LangGraph 官方文档：https://langchain-ai.github.io/langgraph/
- LangChain 官方文档：https://python.langchain.com/

**现阶段**：只需要理解概念，Phase 2 时深入学习

---

#### 7. Docker 基础（部署前学习）（2-3天）

**Docker 是什么？**
一个容器化工具，可以把应用和所有依赖打包成一个"盒子"，在任何机器上都能运行

**Phase 1 中的应用**：
- Dockerfile：定义如何构建应用镜像
- docker-compose.yml：定义如何运行容器

**基础概念**：
```bash
# 构建镜像（根据 Dockerfile）
docker build -t mindflow:latest .

# 运行容器（根据镜像）
docker run -p 7860:7860 mindflow:latest

# 查看运行的容器
docker ps

# 查看日志
docker logs <container_id>

# 使用 docker-compose（更简单）
docker-compose up -d      # 启动
docker-compose logs -f    # 看日志
docker-compose down       # 停止
```

**Dockerfile 在 Phase 1 中的作用**：
```dockerfile
# Dockerfile 的核心
FROM python:3.11-slim         # 基础镜像
WORKDIR /app                  # 工作目录
COPY requirements.txt .       # 复制依赖文件
RUN pip install -r requirements.txt  # 安装依赖
COPY . .                      # 复制应用代码
EXPOSE 7860                   # 暴露端口
CMD ["python", "-m", "src.ui.main"]  # 启动命令
```

**推荐资源**：
- Docker 官方文档：https://docs.docker.com/
- Docker 中文教程：https://www.runoob.com/docker/

**检验**：
- [ ] 理解镜像（Image）和容器（Container）的区别
- [ ] 理解 Dockerfile 的基本指令
- [ ] 理解 docker-compose 的作用

---

### 学习完成后的检验清单

```
基础理解：
- [ ] 能读懂 Python 的类、装饰器、类型提示
- [ ] 能理解 Gradio 的 5 个标签页结构

数据库理解：
- [ ] 能理解 7 个数据库表的关系
- [ ] 能读懂 SQLAlchemy 模型的定义
- [ ] 能理解如何查询、插入、更新、删除数据

LLM 理解：
- [ ] 能理解 Claude API 的基本调用
- [ ] 能理解多提供商 LLM 的切换原理

部署理解：
- [ ] 能理解 Dockerfile 的作用
- [ ] 能理解 docker-compose 的配置

现在可以开始 Phase 2：
- [ ] 理解事件提取 Agent 的概念
- [ ] 准备学习 LangGraph 框架
```

---

---

## 🚀 第二部分：Linux 服务器部署步骤

现在来说部署。你有 Linux 云服务器，以下是完整的部署步骤。

### 部署前准备

**服务器要求**：
- CPU: 2 核以上
- 内存: 2GB 以上
- 存储: 10GB 以上
- OS: Ubuntu 20.04+ 或其他 Linux 发行版

**你需要的信息**：
- 服务器地址（IP 或域名）
- SSH 用户名和密码（或 SSH 密钥）
- Claude API 密钥

---

### 部署步骤

#### Step 1: SSH 登录服务器

```bash
# 如果有 SSH 密钥
ssh -i /path/to/key.pem user@your_server_ip

# 如果用密码
ssh user@your_server_ip
# 然后输入密码
```

---

#### Step 2: 安装 Docker 和 docker-compose

```bash
# 更新包管理器
sudo apt update
sudo apt upgrade -y

# 安装 Docker
sudo apt install -y docker.io docker-compose

# 验证安装
docker --version
docker-compose --version

# （可选）将当前用户添加到 docker 组，避免每次都用 sudo
sudo usermod -aG docker $USER
# 需要重新登录才能生效，或运行：
newgrp docker
```

---

#### Step 3: 获取应用代码

**选项 A：从 GitHub 克隆**（推荐）

```bash
# 创建应用目录
mkdir -p /opt/mindflow
cd /opt/mindflow

# 克隆代码（替换为你的仓库 URL）
git clone https://github.com/damiangao/mindflow.git .

# 检查分支（确保在 Phase 1 的分支）
git branch -a
git checkout damiangao/phase1-framework  # 或 main（如果已合并）
```

**选项 B：上传本地代码**

```bash
# 从你的本地机器上传（本地机器执行）
scp -r /local/path/to/mindflow user@your_server:/opt/

# 然后在服务器上
cd /opt/mindflow
```

---

#### Step 4: 配置环境变量

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env 文件，填入你的 API 密钥
nano .env  # 或 vi .env

# 需要修改的关键变量：
# LLM_PROVIDER=claude
# CLAUDE_API_KEY=sk-ant-xxxxxxx  （你的实际 API 密钥）
# GRADIO_HOST=0.0.0.0           （允许外网访问）
# APP_ENV=production             （生产环境）

# 保存：Ctrl+X，然后输入 Y，再按 Enter
```

**`.env` 文件中的重要配置**：
```env
# LLM 配置
LLM_PROVIDER=claude
CLAUDE_API_KEY=你的API密钥  # 这是必须的！
CLAUDE_MODEL=claude-3-5-haiku-20241022

# 应用配置
APP_ENV=production
DEBUG=false
GRADIO_HOST=0.0.0.0       # 允许任何 IP 访问
GRADIO_PORT=7860

# 数据库
DATABASE_URL=sqlite:///./data/mindflow.db
```

---

#### Step 5: 启动应用（使用 docker-compose）

```bash
# 在 /opt/mindflow 目录中执行
docker-compose up -d

# 检查状态
docker-compose ps

# 查看日志
docker-compose logs -f mindflow

# 停止应用（如需要）
docker-compose down
```

**输出应该显示**：
```
NAME       STATUS         PORTS
mindflow   Up 2 seconds   0.0.0.0:7860->7860/tcp
```

---

#### Step 6: 配置防火墙和访问

```bash
# 如果服务器有防火墙，开放 7860 端口
sudo ufw allow 7860/tcp

# 验证
sudo ufw status

# 查看应用是否在监听 7860 端口
sudo netstat -tlnp | grep 7860
```

---

#### Step 7: 访问应用

在你的浏览器中访问：
```
http://your_server_ip:7860
```

例如：
```
http://114.119.45.123:7860    # 如果你的服务器 IP 是这个
```

如果有域名，也可以：
```
http://your_domain.com:7860
```

---

#### Step 8: 配置 Nginx 反向代理（可选但推荐）

这样可以用 80/443 端口，不用写 7860

```bash
# 安装 Nginx
sudo apt install -y nginx

# 创建配置文件
sudo nano /etc/nginx/sites-available/mindflow

# 添加以下内容：
```

```nginx
upstream mindflow {
    server localhost:7860;
}

server {
    listen 80;
    server_name your_domain.com;  # 替换为你的域名或 IP

    location / {
        proxy_pass http://mindflow;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
# 启用配置
sudo ln -s /etc/nginx/sites-available/mindflow /etc/nginx/sites-enabled/

# 测试配置
sudo nginx -t

# 启动 Nginx
sudo systemctl start nginx
sudo systemctl enable nginx

# 现在可以直接访问：
# http://your_domain.com
```

---

### 常见问题排查

#### 问题 1：应用无法启动

```bash
# 查看详细日志
docker-compose logs mindflow

# 常见原因：
# 1. API 密钥错误
# 2. 端口已被占用
# 3. 磁盘空间不足
```

#### 问题 2：无法访问应用

```bash
# 检查防火墙
sudo ufw status

# 检查端口是否开放
sudo netstat -tlnp | grep 7860

# 检查容器状态
docker-compose ps

# 如果容器未运行，查看错误：
docker-compose logs mindflow
```

#### 问题 3：数据丢失

```bash
# 数据存储在 data/ 目录
# 定期备份这个目录
tar -czf mindflow-backup-$(date +%Y%m%d).tar.gz data/

# 或使用 docker 卷备份
docker-compose exec mindflow tar -czf /app/backup-$(date +%Y%m%d).tar.gz /app/data
```

---

### 生产部署最佳实践

```bash
# 1. 使用 Docker 数据卷（而不是本地路径）
# 修改 docker-compose.yml 中的 volumes

# 2. 定期备份
# 创建备份脚本
nano /opt/backup.sh
```

```bash
#!/bin/bash
# 每天备份
BACKUP_DIR="/opt/backups"
mkdir -p $BACKUP_DIR
tar -czf $BACKUP_DIR/mindflow-$(date +%Y%m%d).tar.gz /opt/mindflow/data/

# 保留最近 7 天的备份
find $BACKUP_DIR -mtime +7 -delete
```

```bash
# 3. 设置自动启动
# 编辑 /opt/mindflow/docker-compose.yml
# 添加 restart: unless-stopped
# 这样服务器重启后，应用会自动启动

# 4. 配置监控和告警（可选）
# 使用 cloudwatch, prometheus 等监控工具
```

---

### 更新应用代码

当有新版本时：

```bash
cd /opt/mindflow

# 停止当前应用
docker-compose down

# 拉取最新代码
git pull origin main  # 或 git pull origin damiangao/phase1-framework

# 重新构建镜像（如果 requirements.txt 有变化）
docker-compose build

# 启动新版本
docker-compose up -d

# 查看日志确保正常启动
docker-compose logs -f mindflow
```

---

### 监控和维护

```bash
# 查看应用实时日志
docker-compose logs -f mindflow

# 查看资源使用情况
docker stats

# 进入容器调试（如需要）
docker-compose exec mindflow bash

# 检查数据库状态
docker-compose exec mindflow sqlite3 data/mindflow.db "SELECT COUNT(*) FROM user_profile;"

# 清理 Docker 垃圾（释放空间）
docker system prune -a
```

---

## 📋 部署检验清单

部署完成后，确保以下都正常：

```
部署准备：
- [ ] 服务器已连接
- [ ] Docker 已安装
- [ ] 代码已上传

配置：
- [ ] .env 文件已配置
- [ ] Claude API 密钥已填入
- [ ] 防火墙已开放 7860 端口

启动：
- [ ] docker-compose up -d 执行成功
- [ ] docker-compose ps 显示容器正在运行
- [ ] 日志无错误（docker-compose logs）

访问：
- [ ] 浏览器可以访问 http://server_ip:7860
- [ ] Gradio UI 可以正常加载
- [ ] 5 个标签页都能显示

功能测试（可选）：
- [ ] 生活记录标签页可以输入文本
- [ ] 计划管理标签页可以创建计划
- [ ] 系统设置可以测试 LLM 连接
- [ ] 日志中没有错误信息
```

---

## 🎯 下一步

部署完成后，你可以：

1. **测试应用** - 在浏览器中使用各个功能
2. **学习代码** - 使用上面的学习路线逐个理解 Phase 1 的实现
3. **准备 Phase 2** - 开始学习 LangGraph，准备实现事件提取 Agent
4. **收集反馈** - 使用过程中发现的问题、改进意见

---

**祝部署顺利！** 🚀

有任何问题，可以查看日志：`docker-compose logs mindflow`
