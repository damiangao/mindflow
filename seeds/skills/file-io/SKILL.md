---
name: file-io
description: 安全地读取和写入文件。当用户提到文件读写、文件操作、读取文件、保存文件时使用。
metadata:
  id: skill_file_io
  display_name: 文件读写
  preconditions:
    - has_file_path
  effects:
    - has_file_content
  methodology_scores:
    meth_simple: 0.8
    meth_stdlib: 0.9
  parent_methodologies:
    - meth_simple
    - meth_stdlib
  called_skills: []
  tags:
    - file-system
    - io
    - basic
  version: "1.0.0"
  author: MindFlow
---

# 文件读写

## 概述

安全地读取和写入文件。包含路径检查、编码处理、异常处理等最佳实践。

## 执行步骤

1. 检查文件路径是否存在
2. 使用合适的编码打开文件
3. 处理文件读写操作
4. 确保文件正确关闭
5. 处理可能的异常

## 示例

### 读取文件

```python
from pathlib import Path

def read_file(filepath: str, encoding: str = "utf-8") -> str:
    """安全读取文件内容"""
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"文件不存在: {filepath}")
    
    return path.read_text(encoding=encoding)
```

### 写入文件

```python
from pathlib import Path

def write_file(filepath: str, content: str, encoding: str = "utf-8") -> None:
    """安全写入文件内容"""
    path = Path(filepath)
    
    # 确保父目录存在
    path.parent.mkdir(parents=True, exist_ok=True)
    
    path.write_text(content, encoding=encoding)
```

### 使用上下文管理器

```python
# 推荐方式：使用 with 语句确保文件正确关闭
with open("file.txt", "r", encoding="utf-8") as f:
    content = f.read()

with open("output.txt", "w", encoding="utf-8") as f:
    f.write("Hello, World!")
```

## 常见问题

### 编码问题
- Windows 默认编码可能是 GBK
- 建议始终显式指定 `encoding="utf-8"`

### 路径问题
- 使用 `pathlib.Path` 处理跨平台路径
- 避免硬编码路径分隔符
