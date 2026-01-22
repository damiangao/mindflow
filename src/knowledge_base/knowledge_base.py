"""知识库统一接口"""
from pathlib import Path
from typing import List, Optional
from .models import Methodology, Skill, Artifact, ArtifactType
from .graph_store import GraphStore
from .vector_store import VectorStore


class KnowledgeBase:
    """知识库统一接口"""
    
    def __init__(self, data_dir: str = "data"):
        self.graph = GraphStore(f"{data_dir}/graph.json")
        self.vector = VectorStore(f"{data_dir}/vectors")
    
    def add_methodology(self, methodology: Methodology) -> str:
        """添加方法论"""
        return self.graph.add_node(methodology)
    
    def add_skill(self, skill: Skill) -> str:
        """添加 Skill"""
        skill_id = self.graph.add_node(skill)
        self.vector.index_skill(skill)
        
        for meth_id in skill.parent_methodologies:
            self.graph.add_edge(meth_id, skill_id, "guides")
        
        return skill_id
    
    def add_artifact(self, artifact: Artifact) -> str:
        """添加副产品（文件需已存在）"""
        artifact_id = self.graph.add_node(artifact)
        self.vector.index_artifact(artifact)
        
        for skill_id in artifact.parent_skills:
            self.graph.add_edge(skill_id, artifact_id, "produces")
        
        return artifact_id
    
    def query(self, user_input: str, top_k: int = 5) -> List[tuple]:
        """查询相关 Skills"""
        matches = self.vector.search(user_input, top_k)
        
        results = []
        for skill_id, score in matches:
            skill_data = self.graph.get_node(skill_id)
            if skill_data:
                results.append((skill_data, score))
        
        return results
    
    def get_skill(self, skill_id: str) -> Optional[dict]:
        """获取 Skill 详情"""
        return self.graph.get_node(skill_id)
    
    def get_methodology(self, meth_id: str) -> Optional[dict]:
        """获取方法论详情"""
        return self.graph.get_node(meth_id)
