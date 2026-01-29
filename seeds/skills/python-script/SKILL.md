---
name: python-script
description: Generate concise Python scripts to solve specific problems. Use when user mentions writing Python code, generating scripts, or automation scripts.
metadata:
  id: skill_python_script
  display_name: Python Script Generation
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

# Python Script Generation

## Overview

Generate concise Python scripts to solve specific problems. Follow the simplicity-first principle and prefer standard library.

## Execution Steps

1. Clarify script inputs and outputs
2. Choose appropriate standard library or tools
3. Write concise implementation code
4. Add necessary error handling
5. Include usage examples

## Code Standards

### Script Structure

```python
#!/usr/bin/env python3
"""Script description

Usage:
    python script.py <input_file> <output_file>
"""
import sys
from pathlib import Path


def main(input_path: str, output_path: str) -> None:
    """Main function"""
    # Implementation logic
    pass


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)
    
    main(sys.argv[1], sys.argv[2])
```

### Best Practices

1. **Simplicity First**
   - Use one line of code instead of ten when possible
   - Avoid over-abstraction

2. **Standard Library First**
   - `pathlib` for path handling
   - `json` for JSON processing
   - `csv` for CSV processing
   - `argparse` for command-line arguments

3. **Error Handling**
   ```python
   try:
       result = process(data)
   except FileNotFoundError as e:
       print(f"Error: File not found - {e}")
       sys.exit(1)
   except Exception as e:
       print(f"Error: {e}")
       sys.exit(1)
   ```

4. **Type Hints**
   ```python
   def process(data: list[dict]) -> str:
       """Process data and return result"""
       pass
   ```

## Common Templates

### File Processing Script

```python
from pathlib import Path

def process_file(input_path: Path) -> str:
    content = input_path.read_text(encoding="utf-8")
    # Processing logic
    return content

if __name__ == "__main__":
    import sys
    result = process_file(Path(sys.argv[1]))
    print(result)
```

### Data Conversion Script

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
