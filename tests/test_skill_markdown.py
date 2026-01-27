"""测试 Skill Markdown 格式解析"""
import frontmatter
from pathlib import Path


def test_skill_loading():
    """测试从 SKILL.md 加载 Skill"""
    print("=== Test Skill Markdown Format ===\n")
    
    skills_dir = Path("../seeds/skills")
    
    for skill_subdir in skills_dir.iterdir():
        if skill_subdir.is_dir():
            skill_file = skill_subdir / "SKILL.md"
            if skill_file.exists():
                print(f"[OK] Loading: {skill_subdir.name}/SKILL.md")
                
                content = skill_file.read_text(encoding="utf-8")
                post = frontmatter.loads(content)
                
                # 提取字段
                name = post.get("name", "")
                description = post.get("description", "")
                metadata = post.get("metadata", {})
                
                print(f"     name: {name}")
                print(f"     description: {description[:50]}...")
                print(f"     metadata keys: {list(metadata.keys())}")
                print(f"     content length: {len(post.content)} chars")
                print()
    
    print("[SUCCESS] All Skills parsed successfully!")


if __name__ == "__main__":
    test_skill_loading()
