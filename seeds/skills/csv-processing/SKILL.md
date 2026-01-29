---
name: csv-processing
description: Read, parse, and process CSV format data. Use when user mentions CSV files, tabular data, data cleaning, or data import.
metadata:
  id: skill_csv
  display_name: CSV File Processing
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

# CSV File Processing

## Overview

Read, parse, and process CSV format data. Supports common operations like data cleaning, missing value handling, and data validation.

## Execution Steps

1. Read CSV file using pandas
2. Check data integrity and column names
3. Handle missing values and anomalous data
4. Return processed DataFrame

## Example

```python
import pandas as pd

# Read CSV file
df = pd.read_csv("data.csv")

# Check data
print(df.info())
print(df.head())

# Handle missing values
df.fillna(df.mean(), inplace=True)
```

## Common Issues

### Encoding Problems
If you encounter encoding errors, try specifying the encoding:
```python
df = pd.read_csv("data.csv", encoding="utf-8")
# or
df = pd.read_csv("data.csv", encoding="gbk")
```

### Large File Processing
For large files, use chunked reading:
```python
chunks = pd.read_csv("large_file.csv", chunksize=10000)
for chunk in chunks:
    process(chunk)
```
