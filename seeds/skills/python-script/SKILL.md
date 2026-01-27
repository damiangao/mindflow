---
name: python-script
description: 生成简洁的Python脚本解决具体问题。当用户提到写Python代码、生成脚本、自动化脚本时使用。
metadata:
  id: skill_python_script
  display_name: Python脚本生成
  preconditions:
    - has_requirement
  effects:
    - has_python_code
  methodology_scores:
    meth_simple: 0.9
    meth_stdlib: 0.8
    meth_consistency: 0.7
  parent_methodologies:
    - meth_simple
    - meth_stdlib
    - meth_consistency
  called_skills: []
  tags:
    - code-generation
    - python
    - automation
  version: "1.0.0"
  author: MindFlow
---

# Python脚本生成

## 概述

生成简洁的Python脚本解决具体问题。遵循简单优先原则，优先使用标准库。

## 执行步骤

1. 明确脚本的输入和输出
2. 选择合适的标准库或工具
3. 编写简洁的实现代码
4. 添加必要的错误处理
5. 包含使用示例

## 代码规范

### 脚本结构

```python
#!/usr/bin/env python3
"""脚本���述

Usage:
    python script.py <input_file> <output_file>
"""
import sys
from pathlib import Path


def main(input_path: str, output_path: str) -> None:
    """主函数"""
    # 实现逻辑
    pass


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)
    
    main(sys.argv[1], sys.argv[2])
```

### 最佳实践

1. **简单优先**
   - 能用一行代码解决的不用十行
   - 避免过度抽象

2. **标准库优先**
   - `pathlib` 处理路径
   - `json` 处理 JSON
   - `csv` 处理 CSV
   - `argparse` 处理命令行参数

3. **错误处理**
   ```python
   try:
       result = process(data)
   except FileNotFoundError as e:
       print(f"错误: 文件不存在 - {e}")
       sys.exit(1)
   except Exception as e:
       print(f"错误: {e}")
       sys.exit(1)
   ```

4. **类型提示**
   ```python
   def process(data: list[dict]) -> str:
       """处理数据并返回结果"""
       pass
   ```

## 常用模板

### 文件处理脚本

```python
from pathlib import Path

def process_file(input_path: Path) -> str:
    content = input_path.read_text(encoding="utf-8")
    # 处理逻辑
    return content

if __name__ == "__main__":
    import sys
    result = process_file(Path(sys.argv[1]))
    print(result)
```

### 数据转换脚本

```python
import json
import csv
from pathlib import Path

def json_to_csv(json_path: Path, csv_path: Path) -> None:
    data = json.loads(json_path.read_text())
    
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
```
