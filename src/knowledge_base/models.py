"""Mindflow 知识库数据模型

遵循 Agent Skills 规范 (https://agentskills.io/specification)
"""
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, ClassVar
from pydantic import BaseModel, Field


class NodeStatus(str, Enum):
    """节点状态"""
    ACTIVE = "active"
    DEPRECATED = "deprecated"
    ARCHIVED = "archived"
    PENDING = "pending"


class ArtifactType(str, Enum):
    """副产品类型"""
    CODE = "code"
    FUNCTION = "function"
    TEMPLATE = "template"
    DOCUMENT = "document"
    CONFIG = "config"


class Methodology(BaseModel):
    """方法论节点 - L1层"""
    id: str
    name: str
    description: str
    principles: List[str]
    evaluation_rule: str
    weight: float = Field(ge=0, le=1)
    status: NodeStatus = NodeStatus.ACTIVE
    guided_skills: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    confidence: float = Field(default=1.0, ge=0, le=1)


class Skill(BaseModel):
    """Skill 节点 - L2层
    
    遵循 Agent Skills 规范，支持 Markdown 格式导入导出
    """
    id: str
    name: str
    description: str  # 触发条件描述（Agent Skills 规范要求）
    instructions: str  # Markdown 格式的执行步骤
    
    # 规划相关
    preconditions: List[str] = Field(default_factory=list)
    effects: List[str] = Field(default_factory=list)
    
    # 方法论评分
    methodology_scores: Dict[str, float] = Field(default_factory=dict)
    parent_methodologies: List[str] = Field(default_factory=list)
    
    # 依赖关系
    called_skills: List[str] = Field(default_factory=list)
    artifacts: List[str] = Field(default_factory=list)
    
    # 统计信息
    success_rate: float = Field(default=0.0, ge=0, le=1)
    usage_count: int = Field(default=0, ge=0)
    
    # 元数据（Agent Skills 规范扩展）
    version: str = Field(default="1.0.0")
    author: str = Field(default="MindFlow")
    tags: List[str] = Field(default_factory=list)
    
    # 时间戳
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    
    def to_markdown(self) -> str:
        """导出为 Agent Skills 规范的 Markdown 格式
        
        Returns:
            符合 Agent Skills 规范的 SKILL.md 内容
        """
        # 构建 YAML frontmatter
        frontmatter_lines = [
            "---",
            f"name: {self.id.replace('skill_', '').replace('_', '-')}",
            f"description: {self.description}",
        ]
        
        # 添加 metadata 块（MindFlow 扩展字段）
        frontmatter_lines.append("metadata:")
        frontmatter_lines.append(f"  id: {self.id}")
        
        if self.preconditions:
            frontmatter_lines.append(f"  preconditions: {self.preconditions}")
        if self.effects:
            frontmatter_lines.append(f"  effects: {self.effects}")
        if self.methodology_scores:
            frontmatter_lines.append(f"  methodology_scores:")
            for meth_id, score in self.methodology_scores.items():
                frontmatter_lines.append(f"    {meth_id}: {score}")
        if self.parent_methodologies:
            frontmatter_lines.append(f"  parent_methodologies: {self.parent_methodologies}")
        if self.called_skills:
            frontmatter_lines.append(f"  called_skills: {self.called_skills}")
        if self.tags:
            frontmatter_lines.append(f"  tags: {self.tags}")
        
        frontmatter_lines.append(f"  version: \"{self.version}\"")
        frontmatter_lines.append(f"  author: {self.author}")
        frontmatter_lines.append("---")
        
        # 构建 Markdown 正文
        body_lines = [
            "",
            f"# {self.name}",
            "",
            "## 概述",
            "",
            self.description,
            "",
            "## 执行步骤",
            "",
            self.instructions,
        ]
        
        return "\n".join(frontmatter_lines + body_lines)
    
    @classmethod
    def from_markdown(cls, content: str, skill_dir: Optional[str] = None) -> "Skill":
        """从 Agent Skills 规范的 Markdown 格式解析
        
        Args:
            content: SKILL.md 文件内容
            skill_dir: Skill 目录名（用于生成 id）
            
        Returns:
            Skill 实例
        """
        import frontmatter
        
        post = frontmatter.loads(content)
        
        # 从 frontmatter 提取数据
        name = post.get("name", "")
        description = post.get("description", "")
        metadata = post.get("metadata", {})
        
        # 生成 id
        skill_id = metadata.get("id") or f"skill_{name.replace('-', '_')}"
        
        # 从 metadata 提取 MindFlow 扩展字段
        return cls(
            id=skill_id,
            name=metadata.get("display_name", name.replace("-", " ").title()),
            description=description,
            instructions=post.content.strip(),
            preconditions=metadata.get("preconditions", []),
            effects=metadata.get("effects", []),
            methodology_scores=metadata.get("methodology_scores", {}),
            parent_methodologies=metadata.get("parent_methodologies", []),
            called_skills=metadata.get("called_skills", []),
            tags=metadata.get("tags", []),
            version=metadata.get("version", "1.0.0"),
            author=metadata.get("author", "MindFlow"),
        )


class Artifact(BaseModel):
    """副产品节点 - L3层
    
    轻量化设计：只存储元数据，实际内容存储在文件系统
    """
    id: str
    name: str
    type: ArtifactType
    summary: str  # 文档总结（用于向量索引）
    filepath: str  # 文件路径（指向实际文件）
    parent_skills: List[str] = Field(default_factory=list)
    usage_count: int = Field(default=0, ge=0)
    tags: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.now)
