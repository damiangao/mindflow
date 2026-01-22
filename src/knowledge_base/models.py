"""Mindflow 知识库数据模型"""
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional
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
    """Skill 节点 - L2层"""
    id: str
    name: str
    description: str
    instructions: str
    preconditions: List[str] = Field(default_factory=list)
    effects: List[str] = Field(default_factory=list)
    methodology_scores: Dict[str, float] = Field(default_factory=dict)
    parent_methodologies: List[str] = Field(default_factory=list)
    called_skills: List[str] = Field(default_factory=list)
    artifacts: List[str] = Field(default_factory=list)
    success_rate: float = Field(default=0.0, ge=0, le=1)
    usage_count: int = Field(default=0, ge=0)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class Artifact(BaseModel):
    """副产品节点 - L3层"""
    id: str
    name: str
    type: ArtifactType
    summary: str
    filepath: str
    parent_skills: List[str] = Field(default_factory=list)
    usage_count: int = Field(default=0, ge=0)
    tags: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.now)
