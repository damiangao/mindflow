"""测试知识库核心功能"""
import sys
from pathlib import Path

# 添加 src 到路径
sys.path.insert(0, str(Path(__file__).parent / "src"))

from knowledge_base.models import Methodology, Skill, Artifact, NodeStatus, ArtifactType
from knowledge_base.knowledge_base import KnowledgeBase


def test_basic_operations():
    """测试基础操作"""
    print("=== 测试知识库基础操作 ===\n")
    
    # 初始化知识库
    kb = KnowledgeBase()
    
    # 1. 添加方法论
    print("1. 添加方法论...")
    methodology = Methodology(
        id="meth_simple",
        name="简单优于复杂",
        description="优先选择简单直接的解决方案",
        principles=[
            "能用一行代码解决的不用十行",
            "避免过度设计",
            "先让它工作，再优化"
        ],
        evaluation_rule="检查代码行数和复杂度",
        weight=0.9
    )
    meth_id = kb.add_methodology(methodology)
    print(f"   [OK] 方法论已添加: {meth_id}\n")
    
    # 2. 添加 Skill
    print("2. 添加 Skill...")
    skill = Skill(
        id="skill_csv",
        name="CSV 文件处理",
        description="读取、解析、处理 CSV 格式数据",
        instructions="""1. 使用 pandas 读取 CSV 文件
2. 检查数据完整性
3. 处理缺失值
4. 返回 DataFrame""",
        preconditions=["has_csv_file"],
        effects=["has_dataframe"],
        methodology_scores={"meth_simple": 0.8},
        parent_methodologies=["meth_simple"]
    )
    skill_id = kb.add_skill(skill)
    print(f"   [OK] Skill 已添加: {skill_id}\n")
    
    # 3. 添加副产品
    print("3. 添加副产品...")
    artifact = Artifact(
        id="artifact_csv_reader",
        name="CSV 读取函数",
        type=ArtifactType.FUNCTION,
        content="""import pandas as pd

def read_csv_safe(filepath):
    return pd.read_csv(filepath)""",
        parent_skills=["skill_csv"],
        tags=["csv", "pandas", "io"]
    )
    artifact_id = kb.add_artifact(artifact)
    print(f"   [OK] 副产品已添加: {artifact_id}\n")
    
    # 4. 查询 Skill
    print("4. 查询 Skill...")
    skill_data = kb.get_skill("skill_csv")
    if skill_data:
        print(f"   [OK] 找到 Skill: {skill_data['name']}\n")
    
    # 5. 查询方法论
    print("5. 查询方法论...")
    meth_data = kb.get_methodology("meth_simple")
    if meth_data:
        print(f"   [OK] 找到方法论: {meth_data['name']}\n")
    
    print("[SUCCESS] 所有测试通过!")


if __name__ == "__main__":
    test_basic_operations()
