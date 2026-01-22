"""图存储层 - 基于 NetworkX"""
import json
from pathlib import Path
from typing import Dict, List, Optional, Union
import networkx as nx
from .models import Methodology, Skill, Artifact


class GraphStore:
    """图数据库抽象层"""
    
    def __init__(self, data_file: str = "data/graph.json"):
        self.graph = nx.DiGraph()
        self.data_file = Path(data_file)
        self._load()
    
    def _load(self):
        """从文件加载图"""
        if self.data_file.exists():
            data = json.loads(self.data_file.read_text(encoding="utf-8"))
            self.graph = nx.node_link_graph(data)
    
    def save(self):
        """保存图到文件"""
        self.data_file.parent.mkdir(parents=True, exist_ok=True)
        data = nx.node_link_data(self.graph)
        self.data_file.write_text(json.dumps(data, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    
    def add_node(self, node: Union[Methodology, Skill, Artifact]) -> str:
        """添加节点"""
        self.graph.add_node(node.id, **node.model_dump())
        self.save()
        return node.id
    
    def get_node(self, node_id: str) -> Optional[Dict]:
        """获取节点"""
        return self.graph.nodes.get(node_id)
    
    def update_node(self, node_id: str, updates: dict) -> bool:
        """更新节点"""
        if node_id not in self.graph:
            return False
        self.graph.nodes[node_id].update(updates)
        self.save()
        return True
    
    def delete_node(self, node_id: str) -> bool:
        """删除节点"""
        if node_id not in self.graph:
            return False
        self.graph.remove_node(node_id)
        self.save()
        return True
    
    def add_edge(self, source_id: str, target_id: str, relation: str, properties: dict = None) -> bool:
        """添加关系"""
        props = properties or {}
        props["relation"] = relation
        self.graph.add_edge(source_id, target_id, **props)
        self.save()
        return True
    
    def get_edges(self, node_id: str, direction: str = "out") -> List[tuple]:
        """获取节点的边"""
        if direction == "out":
            return list(self.graph.out_edges(node_id, data=True))
        elif direction == "in":
            return list(self.graph.in_edges(node_id, data=True))
        else:
            return list(self.graph.edges(node_id, data=True))
    
    def get_skills_by_methodology(self, meth_id: str) -> List[Dict]:
        """获取方法论指导的 Skills"""
        skills = []
        for _, target, data in self.graph.out_edges(meth_id, data=True):
            if data.get("relation") == "guides":
                skills.append(self.graph.nodes[target])
        return skills
    
    def get_artifacts_by_skill(self, skill_id: str) -> List[Dict]:
        """获取 Skill 的副产品"""
        artifacts = []
        for _, target, data in self.graph.out_edges(skill_id, data=True):
            if data.get("relation") == "produces":
                artifacts.append(self.graph.nodes[target])
        return artifacts
