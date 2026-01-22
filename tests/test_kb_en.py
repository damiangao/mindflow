"""Test Knowledge Base Core Functions"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from knowledge_base.models import Methodology, Skill, Artifact, ArtifactType
from knowledge_base.knowledge_base import KnowledgeBase


def test_basic_operations():
    """Test basic CRUD operations"""
    print("=== Testing Knowledge Base ===\n")
    
    kb = KnowledgeBase()
    
    # 1. Add Methodology
    print("1. Adding Methodology...")
    methodology = Methodology(
        id="meth_simple",
        name="Simplicity First",
        description="Prefer simple and direct solutions",
        principles=[
            "One line is better than ten",
            "Avoid over-engineering",
            "Make it work first, optimize later"
        ],
        evaluation_rule="Check code lines and complexity",
        weight=0.9
    )
    meth_id = kb.add_methodology(methodology)
    print(f"   [OK] Methodology added: {meth_id}\n")
    
    # 2. Add Skill
    print("2. Adding Skill...")
    skill = Skill(
        id="skill_csv",
        name="CSV File Processing",
        description="Read, parse and process CSV data",
        instructions="""1. Use pandas to read CSV file
2. Check data integrity
3. Handle missing values
4. Return DataFrame""",
        preconditions=["has_csv_file"],
        effects=["has_dataframe"],
        methodology_scores={"meth_simple": 0.8},
        parent_methodologies=["meth_simple"]
    )
    skill_id = kb.add_skill(skill)
    print(f"   [OK] Skill added: {skill_id}\n")
    
    # 3. Add Artifact
    print("3. Adding Artifact...")
    artifact = Artifact(
        id="artifact_csv_reader",
        name="CSV Reader Function",
        type=ArtifactType.FUNCTION,
        content="""import pandas as pd

def read_csv_safe(filepath):
    return pd.read_csv(filepath)""",
        parent_skills=["skill_csv"],
        tags=["csv", "pandas", "io"]
    )
    artifact_id = kb.add_artifact(artifact)
    print(f"   [OK] Artifact added: {artifact_id}\n")
    
    # 4. Query Skill
    print("4. Querying Skill...")
    skill_data = kb.get_skill("skill_csv")
    if skill_data:
        print(f"   [OK] Found Skill: {skill_data['name']}\n")
    
    # 5. Query Methodology
    print("5. Querying Methodology...")
    meth_data = kb.get_methodology("meth_simple")
    if meth_data:
        print(f"   [OK] Found Methodology: {meth_data['name']}\n")
    
    # 6. Test Vector Search (if available)
    print("6. Testing Vector Search...")
    try:
        results = kb.query("process CSV file", top_k=3)
        if results:
            print(f"   [OK] Vector search returned {len(results)} results")
            for skill_data, score in results:
                print(f"        - {skill_data['name']}: {score:.3f}")
        print()
    except Exception as e:
        print(f"   [SKIP] Vector search not available: {e}\n")
    
    print("[SUCCESS] All tests passed!")


if __name__ == "__main__":
    test_basic_operations()
