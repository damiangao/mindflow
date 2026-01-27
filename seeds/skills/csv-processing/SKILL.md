---
name: csv-processing
description: 读取、解析、处理CSV格式数据。当用户提到CSV文件、表格数据、数据清洗、数据导入时使用。
metadata:
  id: skill_csv
  display_name: CSV文件处理
  preconditions:
    - has_csv_file
  effects:
    - has_dataframe
  methodology_scores:
    meth_simple: 0.8
    meth_stdlib: 0.9
  parent_methodologies:
    - meth_simple
    - meth_stdlib
  called_skills: []
  tags:
    - data-processing
    - csv
    - pandas
  version: "1.0.0"
  author: MindFlow
---

# CSV文件处理

## 概述

读取、解析、处理CSV格式数据。支持数据清洗、缺失值处理、数据验证等常见操作。

## 执行步骤

1. 使用 pandas 读取 CSV 文件
2. 检查数据完整性和列名
3. 处理缺失值和异常数据
4. 返回处理后的 DataFrame

## 示例

```python
import pandas as pd

# 读取 CSV 文件
df = pd.read_csv("data.csv")

# 检查数据
print(df.info())
print(df.head())

# 处理缺失值
df.fillna(df.mean(), inplace=True)
```

## 常见问题

### 编码问题
如果遇到编码错误，尝试指定编码：
```python
df = pd.read_csv("data.csv", encoding="utf-8")
# 或
df = pd.read_csv("data.csv", encoding="gbk")
```

### 大文件处理
对于大文件，使用分块读取：
```python
chunks = pd.read_csv("large_file.csv", chunksize=10000)
for chunk in chunks:
    process(chunk)
```
