"""种子库加载器

支持 Agent Skills 规范的 Markdown 格式 (SKILL.md)
"""
import yaml
import frontmatter
from pathlib import Path
from datetime import datetime
from knowledge_base import KnowledgeBase, Methodology, Skill


def load_skill_from_markdown(skill_dir: Path) -> Skill:
    """从 SKILL.md 文件加载 Skill
    
    Args:
        skill_dir: Skill 目录路径，包含 SKILL.md 文件
        
    Returns:
        Skill 实例
    """
    skill_file = skill_dir / "SKILL.md"
    if not skill_file.exists():
        raise FileNotFoundError(f"SKILL.md not found in {skill_dir}")
    
    content = skill_file.read_text(encoding="utf-8")
    post = frontmatter.loads(content)
    
    # 从 frontmatter 提取数据
    name = post.get("name", skill_dir.name)
    description = post.get("description", "")
    metadata = post.get("metadata", {})
    
    # 生成 id（优先使用 metadata 中的 id）
    skill_id = metadata.get("id") or f"skill_{name.replace('-', '_')}"
    
    # 显示名称
    display_name = metadata.get("display_name", name.replace("-", " ").title())
    
    return Skill(
        id=skill_id,
        name=display_name,
        description=description,
        instructions=post.content.strip(),
        preconditions=metadata.get("preconditions", []),
        effects=metadata.get("effects", []),
        methodology_scores=metadata.get("methodology_scores", {}),
        parent_methodologies=metadata.get("parent_methodologies", []),
        called_skills=metadata.get("called_skills", []),
        artifacts=metadata.get("artifacts", []),
        tags=metadata.get("tags", []),
        version=metadata.get("version", "1.0.0"),
        author=metadata.get("author", "MindFlow"),
        created_at=datetime.now(),
        updated_at=datetime.now(),
        success_rate=0.0,
        usage_count=0,
    )


def load_seeds(kb: KnowledgeBase, seeds_dir: str = "seeds"):
    """加载种子库
    
    支持两种格式：
    1. Agent Skills 规范: seeds/skills/{skill-name}/SKILL.md (推荐)
    2. 旧版 YAML 格式: seeds/skills/*.yaml (向后兼容)
    """
    seeds_path = Path(seeds_dir)
    
    # 加载方法论 (仍使用 YAML 格式)
    meth_dir = seeds_path / "methodologies"
    if meth_dir.exists():
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
    if skill_dir.exists():
        # 新格式: 目录结构 (Agent Skills 规范)
        for skill_subdir in skill_dir.iterdir():
            if skill_subdir.is_dir():
                skill_file = skill_subdir / "SKILL.md"
                if skill_file.exists():
                    try:
                        skill = load_skill_from_markdown(skill_subdir)
                        kb.add_skill(skill)
                        print(f"✓ 加载 Skill: {skill.name} (from {skill_subdir.name}/SKILL.md)")
                    except Exception as e:
                        print(f"✗ 加载失败: {skill_subdir.name} - {e}")
        
        # 旧格式: YAML 文件 (向后兼容)
        for yaml_file in skill_dir.glob("*.yaml"):
            data = yaml.safe_load(yaml_file.read_text(encoding="utf-8"))
            data["created_at"] = datetime.now()
            data["updated_at"] = datetime.now()
            data.setdefault("success_rate", 0.0)
            data.setdefault("usage_count", 0)
            data.setdefault("artifacts", [])
            data.setdefault("version", "1.0.0")
            data.setdefault("author", "MindFlow")
            data.setdefault("tags", [])
            
            skill = Skill(**data)
            kb.add_skill(skill)
            print(f"✓ 加载 Skill: {skill.name} (from {yaml_file.name}) [旧格式]")


if __name__ == "__main__":
    kb = KnowledgeBase()
    load_seeds(kb)
    print("\n种子库加载完成!")
    print(f"  - 方法论: {len(kb.graph.get_all_methodologies())} 个")
    print(f"  - Skills: {len(kb.graph.get_all_skills())} 个")
