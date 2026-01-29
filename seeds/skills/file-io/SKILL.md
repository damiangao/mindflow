---
name: file-io
description: Safely read and write files. Use when user mentions file reading/writing, file operations, read file, or save file.
metadata:
  id: skill_file_io
  display_name: File I/O
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

# File I/O

## Overview

Safely read and write files. Includes best practices for path checking, encoding handling, and exception handling.

## Execution Steps

1. Check if file path exists
2. Open file with appropriate encoding
3. Perform file read/write operations
4. Ensure file is properly closed
5. Handle possible exceptions

## Examples

### Read File

```python
from pathlib import Path

def read_file(filepath: str, encoding: str = "utf-8") -> str:
    """Safely read file content"""
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {filepath}")
    
    return path.read_text(encoding=encoding)
```

### Write File

```python
from pathlib import Path

def write_file(filepath: str, content: str, encoding: str = "utf-8") -> None:
    """Safely write file content"""
    path = Path(filepath)
    
    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)
    
    path.write_text(content, encoding=encoding)
```

### Using Context Manager

```python
# Recommended: Use with statement to ensure file is properly closed
with open("file.txt", "r", encoding="utf-8") as f:
    content = f.read()

with open("output.txt", "w", encoding="utf-8") as f:
    f.write("Hello, World!")
```

## Common Issues

### Encoding Problems
- Windows default encoding may be GBK
- Always explicitly specify `encoding="utf-8"`

### Path Issues
- Use `pathlib.Path` for cross-platform path handling
- Avoid hardcoding path separators
