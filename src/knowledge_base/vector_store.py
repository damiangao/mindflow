"""向量搜索层 - 基于 Chroma"""
from typing import List, Tuple
import chromadb
from chromadb.utils import embedding_functions
from .models import Skill, Artifact


class VectorStore:
    """向量搜索层
    
    使用 Chroma 内置的 sentence-transformers 支持，无需单独管理嵌入模型。
    默认使用多语言模型以支持中文内容。
    """
    
    def __init__(self, persist_dir: str = "data/vectors", model_name: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"):
        """初始化向量存储
        
        Args:
            persist_dir: 持久化目录
            model_name: sentence-transformers 模型名称
                - all-MiniLM-L6-v2: 默认英文模型（快速）
                - paraphrase-multilingual-MiniLM-L12-v2: 多语言模型（推荐，支持中文）
                - paraphrase-multilingual-mpnet-base-v2: 更强大的多语言模型
        """
        # 配置嵌入函数（Chroma 内置 sentence-transformers）
        self.embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=model_name
        )
        
        # 初始化 Chroma 客户端
        self.client = chromadb.PersistentClient(path=persist_dir)
        
        # 创建集合（指定嵌入函数）
        self.skills_collection = self.client.get_or_create_collection(
            name="skills",
            embedding_function=self.embedding_function
        )
        self.artifacts_collection = self.client.get_or_create_collection(
            name="artifacts",
            embedding_function=self.embedding_function
        )
    
    def index_skill(self, skill: Skill):
        """索引单个 Skill
        
        Chroma 会自动使用配置的 embedding_function 计算向量。
        """
        text = f"{skill.name} {skill.description}"
        self.skills_collection.add(
            ids=[skill.id],
            documents=[text],  # Chroma 自动计算嵌入向量
            metadatas=[{"name": skill.name}]
        )
    
    def index_artifact(self, artifact: Artifact):
        """索引单个 Artifact
        
        Chroma 会自动使用配置的 embedding_function 计算向量。
        """
        text = f"{artifact.name} {artifact.summary}"
        self.artifacts_collection.add(
            ids=[artifact.id],
            documents=[text],  # Chroma 自动计算嵌入向量
            metadatas=[{"name": artifact.name, "type": artifact.type}]
        )
    
    def search(self, query: str, top_k: int = 5) -> List[Tuple[str, float]]:
        """搜索相关 Skills
        
        Chroma 会自��使用配置的 embedding_function 计算查询向量。
        
        Args:
            query: 查询文本
            top_k: 返回结果数量
            
        Returns:
            List of (skill_id, similarity_score) tuples
        """
        results = self.skills_collection.query(
            query_texts=[query],  # Chroma 自动计算查询向量
            n_results=top_k
        )
        
        matches = []
        if results["ids"]:
            for skill_id, distance in zip(results["ids"][0], results["distances"][0]):
                score = 1 - distance  # 转换为相似度分数
                matches.append((skill_id, score))
        
        return matches
    
    def search_artifacts(self, query: str, top_k: int = 5) -> List[Tuple[str, float]]:
        """搜索相关 Artifacts
        
        Chroma 会自动使用配置的 embedding_function 计算查询向量。
        
        Args:
            query: 查询文本
            top_k: 返回结果数量
            
        Returns:
            List of (artifact_id, similarity_score) tuples
        """
        results = self.artifacts_collection.query(
            query_texts=[query],  # Chroma 自动计算查询向量
            n_results=top_k
        )
        
        matches = []
        if results["ids"]:
            for artifact_id, distance in zip(results["ids"][0], results["distances"][0]):
                score = 1 - distance  # 转换为相似度分数
                matches.append((artifact_id, score))
        
        return matches
    
    def reindex_all(self, skills: List[Skill]):
        """重建所有索引
        
        Args:
            skills: 所有技能列表
        """
        # 清空现有索引
        self.skills_collection.delete(where={})
        
        # 重新索引
        for skill in skills:
            self.index_skill(skill)
