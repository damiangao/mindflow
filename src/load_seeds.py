"""种子库加载器"""
import yaml
from pathlib import Path
from datetime import datetime
from knowledge_base import KnowledgeBase, Methodology, Skill


def load_seeds(kb: KnowledgeBase, seeds_dir: str = "seeds"):
    """加载种子库"""
    seeds_path = Path(seeds_dir)
    
    # 加载方法论
    meth_dir = seeds_path / "methodologies"
    for yaml_file in meth_dir.glob("*.yaml"):
        data = yaml.safe_load(yaml_file.read_text(encoding="utf-8"))
        data["created_at"] = datetime.now()
        data["updated_at"] = datetime.now()
        data.setdefault("guided_skills", [])
        data.setdefault("confidence", 1.0)
        
        methodology = Methodology(**data)
        kb.add_methodology(methodology)
        print(f"✓ 加载方法论: {methodology.name}")
    
    # 加载 Skills
    skill_dir = seeds_path / "skills"
    for yaml_file in skill_dir.glob("*.yaml"):
        data = yaml.safe_load(yaml_file.read_text(encoding="utf-8"))
        data["created_at"] = datetime.now()
        data["updated_at"] = datetime.now()
        data.setdefault("success_rate", 0.0)
        data.setdefault("usage_count", 0)
        data.setdefault("artifacts", [])
        
        skill = Skill(**data)
        kb.add_skill(skill)
        print(f"✓ 加载 Skill: {skill.name}")


if __name__ == "__main__":
    kb = KnowledgeBase()
    load_seeds(kb)
    print("\n种子库加载完成!")
