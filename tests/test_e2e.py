"""End-to-End Test: Query and Activate Skill"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from knowledge_base.models import Methodology, Skill, Artifact, ArtifactType
from knowledge_base.knowledge_base import KnowledgeBase


def test_end_to_end():
    """Test complete workflow: Query -> Activate Skill"""
    print("=== End-to-End Test ===\n")
    
    kb = KnowledgeBase()
    
    # Setup: Add methodology, skill, and artifact
    print("Setup: Creating knowledge base...")
    
    methodology = Methodology(
        id="meth_simple",
        name="Simplicity First",
        description="Prefer simple solutions",
        principles=["Keep it simple"],
        evaluation_rule="Check simplicity",
        weight=0.9
    )
    kb.add_methodology(methodology)
    
    skill = Skill(
        id="skill_csv",
        name="CSV Processing",
        description="Process CSV files efficiently",
        instructions="1. Read CSV\n2. Process data\n3. Return result",
        preconditions=["has_csv_file"],
        effects=["has_dataframe"],
        methodology_scores={"meth_simple": 0.8},
        parent_methodologies=["meth_simple"]
    )
    kb.add_skill(skill)
    
    artifact = Artifact(
        id="artifact_csv_func",
        name="CSV Reader",
        type=ArtifactType.FUNCTION,
        content="def read_csv(path): return pd.read_csv(path)",
        parent_skills=["skill_csv"],
        tags=["csv"]
    )
    kb.add_artifact(artifact)
    
    print("   [OK] Knowledge base ready\n")
    
    # Test 1: Query for CSV processing
    print("Test 1: Query 'process CSV file'")
    results = kb.query("process CSV file", top_k=3)
    
    if results:
        best_skill, score = results[0]
        print(f"   [OK] Found: {best_skill['name']} (score: {score:.3f})")
        assert best_skill['id'] == 'skill_csv', "Wrong skill matched!"
        print(f"   [OK] Correct skill matched!\n")
    else:
        print("   [FAIL] No results found\n")
        return False
    
    # Test 2: Get skill details
    print("Test 2: Get skill details")
    skill_data = kb.get_skill("skill_csv")
    assert skill_data is not None, "Skill not found!"
    print(f"   [OK] Skill: {skill_data['name']}")
    print(f"   [OK] Effects: {skill_data['effects']}")
    print(f"   [OK] Preconditions: {skill_data['preconditions']}\n")
    
    # Test 3: Verify relationships
    print("Test 3: Verify relationships")
    edges = kb.graph.get_edges("meth_simple", direction="out")
    assert len(edges) > 0, "No edges found!"
    print(f"   [OK] Found {len(edges)} relationship(s)")
    
    for source, target, data in edges:
        print(f"        {source} --[{data['relation']}]--> {target}")
    print()
    
    print("[SUCCESS] End-to-end test passed!")
    return True


if __name__ == "__main__":
    success = test_end_to_end()
    sys.exit(0 if success else 1)
