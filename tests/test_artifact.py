"""Test Artifact with Summary"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from knowledge_base.models import Artifact, ArtifactType
from knowledge_base.graph_store import GraphStore

def test_artifact_summary():
    print("=== Test Artifact Summary ===\n")
    
    graph = GraphStore("data/graph.json")
    
    # 1. 创建文件
    filepath = Path("artifacts/csv_reader.py")
    filepath.parent.mkdir(exist_ok=True)
    content = """import pandas as pd

def read_csv_safe(filepath, **kwargs):
    '''安全读取CSV文件'''
    return pd.read_csv(filepath, **kwargs)
"""
    filepath.write_text(content, encoding="utf-8")
    print(f"1. Created file: {filepath}\n")
    
    # 2. 创建 Artifact（只存 summary + filepath）
    artifact = Artifact(
        id="csv_reader",
        name="CSV Reader Function",
        type=ArtifactType.FUNCTION,
        summary="Safe CSV file reader using pandas",
        filepath=str(filepath),
        tags=["csv", "pandas", "io"]
    )
    
    print("2. Adding to graph...")
    artifact_id = graph.add_node(artifact)
    print(f"   [OK] Added: {artifact_id}\n")
    
    # 3. 验证图数据库
    print("3. Checking graph...")
    node = graph.get_node(artifact_id)
    print(f"   Name: {node['name']}")
    print(f"   Summary: {node['summary']}")
    print(f"   Filepath: {node['filepath']}")
    print(f"   Has 'content' field: {'content' in node}\n")
    
    # 4. 验证文件可读取
    print("4. Reading file...")
    actual_content = Path(node['filepath']).read_text(encoding="utf-8")
    assert "def read_csv_safe" in actual_content
    print(f"   [OK] File readable, {len(actual_content)} chars\n")
    
    print("[SUCCESS] Summary-based artifact works!")
    print("\n优势：")
    print("  ✓ 图数据库轻量（只存 summary）")
    print("  ✓ 文件可复用（实际代码在文件中）")
    print("  ✓ 支持语义搜索（summary 用于向量索引）")
    
    filepath.unlink()
    print(f"\n[CLEANUP] Removed {filepath}")

if __name__ == "__main__":
    test_artifact_summary()
