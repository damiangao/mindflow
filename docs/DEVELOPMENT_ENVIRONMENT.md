# MindFlow 开发环境配置

## 📅 创建日期
2026-01-28

## 🎯 目的
记录项目的环境配置、测试命令和常用操作，方便快速开发和测试。

---

## 🐍 Python 虚拟环境

### 环境位置
```
F:/workspace/mindflow/.venv
```

### 激活虚拟环境

#### PowerShell
```powershell
cd F:/workspace/mindflow
.venv\Scripts\Activate.ps1
```

#### CMD
```cmd
cd F:\workspace\mindflow
.venv\Scripts\activate.bat
```

### Python 可执行文件路径
```
F:/workspace/mindflow/.venv/Scripts/python.exe
```

### 直接使用（无需激活）
```powershell
# 运行 Python 脚本
.venv\Scripts\python.exe script.py

# 安装依赖
.venv\Scripts\pip.exe install -r requirements.txt

# 查看已安装包
.venv\Scripts\pip.exe list
```

---

## 📦 依赖管理

### 安装所有依赖
```bash
pip install -r requirements.txt
```

### 当前依赖列表
```txt
# 核心依赖
pydantic>=2.0.0
networkx>=3.0
python-dateutil>=2.8.0

# 向量搜索
# chromadb 已内置 sentence-transformers 支持，无需单独安装
chromadb>=0.4.0

# 数据处理
pyyaml>=6.0
python-frontmatter>=1.0.0  # Agent Skills 规范 Markdown 解析
```

### 更新依赖
```bash
pip install --upgrade -r requirements.txt
```

### 查看已安装版本
```bash
pip list | grep -E "pydantic|networkx|chromadb"
```

---

## 🧪 测试命令

### 运行所有测试
```bash
cd F:/workspace/mindflow
.venv\Scripts\python.exe -m pytest tests/
```

### 运行特定测试文件
```bash
# VectorStore 测试
.venv\Scripts\python.exe test_vector_store.py

# 知识库测试
.venv\Scripts\python.exe tests/test_kb.py

# 端到端测试
.venv\Scripts\python.exe tests/test_e2e.py
```

### 运行学习练习
```bash
# NetworkX 练习
cd learning/networkx/exercises
.venv\Scripts\python.exe week1_practice.py

# Chroma 练习
cd learning/chroma/exercises
.venv\Scripts\python.exe day1_basics.py
.venv\Scripts\python.exe chroma_with_sentence_transformers.py

# Pydantic 练习
cd learning/pydantic/exercises
.venv\Scripts\python.exe day5_practice.py
```

---

## 🔧 常用开发命令

### 项目结构查看
```bash
# 查看目录树
tree /F /A

# 查看 Python 文件
Get-ChildItem -Path . -Include *.py -Recurse | Select-Object FullName
```

### 代码检查
```bash
# 查找特定内容
Select-String -Pattern "sentence.?transformer" -Path *.py,*.md -Recurse

# 统计代码行数
Get-ChildItem -Path src -Include *.py -Recurse | Get-Content | Measure-Object -Line
```

### 清理缓存
```bash
# 清理 Python 缓存
Get-ChildItem -Path . -Include __pycache__,*.pyc -Recurse -Force | Remove-Item -Recurse -Force

# 清理测试数据
Remove-Item -Path data/vectors_test -Recurse -Force -ErrorAction SilentlyContinue
```

---

## 🌐 环境变量

### 设置环境变量（临时）

#### PowerShell
```powershell
# 设置 Python 路径
$env:PYTHONPATH = "F:/workspace/mindflow"

# 设置 UTF-8 编码
$env:PYTHONIOENCODING = "utf-8"

# 设置 Chroma 数据目录
$env:CHROMA_DATA_DIR = "F:/workspace/mindflow/data/vectors"
```

#### CMD
```cmd
set PYTHONPATH=F:\workspace\mindflow
set PYTHONIOENCODING=utf-8
set CHROMA_DATA_DIR=F:\workspace\mindflow\data\vectors
```

### 设置环境变量（永久）

#### Windows 系统环境变量
```powershell
# 添加到用户环境变量
[Environment]::SetEnvironmentVariable("PYTHONPATH", "F:/workspace/mindflow", "User")

# 查看环境变量
[Environment]::GetEnvironmentVariable("PYTHONPATH", "User")
```

### 项目特定环境变量

创建 `.env` 文件（如果需要）：
```bash
# .env
PYTHONPATH=F:/workspace/mindflow
CHROMA_DATA_DIR=./data/vectors
PYTHONIOENCODING=utf-8
```

---

## 🐛 调试技巧

### Python 调试
```python
# 在代码中添加断点
import pdb; pdb.set_trace()

# 或使用 breakpoint() (Python 3.7+)
breakpoint()
```

### 查看模块路径
```python
import sys
print(sys.path)

import chromadb
print(chromadb.__file__)
```

### 测试 Chroma 模型下载
```python
from chromadb.utils import embedding_functions

# 测试模型下载（首次会下载）
ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="paraphrase-multilingual-MiniLM-L12-v2"
)
print("模型加载成功！")
```

---

## 📝 常见问题解决

### 问题 1: ModuleNotFoundError
```bash
# 解决方案：设置 PYTHONPATH
$env:PYTHONPATH = "F:/workspace/mindflow"
# 或在代码中添加
import sys
sys.path.insert(0, 'F:/workspace/mindflow')
```

### 问题 2: UnicodeEncodeError (Windows 控制台)
```python
# 解决方案：在脚本开头添加
import sys
import io
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
```

### 问题 3: Chroma 模型下载失败
```bash
# 解决方案 1: 使用 VPN
# 解决方案 2: 使用镜像源
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple chromadb

# 解决方案 3: 使用更小的英文模型
model_name="all-MiniLM-L6-v2"  # 约 80MB
```

### 问题 4: 文件锁定（Windows）
```bash
# 清理 Chroma 数据库连接
# 在代码中添加
import gc
gc.collect()

# 或重启 Python 进程
```

---

## 🚀 快速启动脚本

### 创建 `run_tests.ps1`
```powershell
# run_tests.ps1
$env:PYTHONPATH = "F:/workspace/mindflow"
$env:PYTHONIOENCODING = "utf-8"

Write-Host "运行 VectorStore 测试..." -ForegroundColor Green
.venv\Scripts\python.exe test_vector_store.py

Write-Host "`n运行知识库测试..." -ForegroundColor Green
.venv\Scripts\python.exe tests/test_kb.py
```

### 创建 `setup_env.ps1`
```powershell
# setup_env.ps1
Write-Host "设置 MindFlow 开发环境..." -ForegroundColor Cyan

# 激活虚拟环境
.venv\Scripts\Activate.ps1

# 设置环境变量
$env:PYTHONPATH = "F:/workspace/mindflow"
$env:PYTHONIOENCODING = "utf-8"

# 显示 Python 版本
Write-Host "`nPython 版本:" -ForegroundColor Yellow
python --version

# 显示已安装包
Write-Host "`n已安装的关键包:" -ForegroundColor Yellow
pip list | Select-String -Pattern "pydantic|networkx|chromadb"

Write-Host "`n环境设置完成！" -ForegroundColor Green
```

使用方法：
```powershell
# 设置环境
.\setup_env.ps1

# 运行测试
.\run_tests.ps1
```

---

## 📊 性能监控

### 查看内存使用
```python
import psutil
import os

process = psutil.Process(os.getpid())
print(f"内存使用: {process.memory_info().rss / 1024 / 1024:.2f} MB")
```

### 测试执行时间
```python
import time

start = time.time()
# 你的代码
end = time.time()
print(f"执行时间: {end - start:.2f} 秒")
```

---

## 🔗 相关文档

- [项目 README](../README.md)
- [开发计划](DEVELOPMENT_PLAN.md)
- [技术设计](TECHNICAL_DESIGN.md)
- [VectorStore 优化](VECTOR_STORE_OPTIMIZATION.md)

---

## 📌 快速参考

### 一键测试命令
```powershell
# 设置环境并运行测试
cd F:/workspace/mindflow; $env:PYTHONPATH="F:/workspace/mindflow"; .venv\Scripts\python.exe test_vector_store.py
```

### 一键运行学习练习
```powershell
# Pydantic 练习
cd F:/workspace/mindflow/learning/pydantic/exercises; ..\..\..\..\.venv\Scripts\python.exe day5_practice.py
```

### 一键清理
```powershell
# 清理所有缓存和测试数据
Get-ChildItem -Path . -Include __pycache__,*.pyc,data/vectors_test -Recurse -Force | Remove-Item -Recurse -Force
```

---

**最后更新**: 2026-01-28  
**维护者**: MindFlow Team
