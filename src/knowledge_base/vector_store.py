"""向量搜索层 - 基于 Chroma"""
from typing import List, Tuple
import chromadb
from sentence_transformers import SentenceTransformer
from .models import Skill, Artifact


class VectorStore:
    """向量搜索层"""
    
    def __init__(self, persist_dir: str = "data/vectors", model_name: str = "all-MiniLM-L6-v2"):
        self.embedder = SentenceTransformer(model_name)
        self.client = chromadb.PersistentClient(path=persist_dir)
        self.skills_collection = self.client.get_or_create_collection("skills")
        self.artifacts_collection = self.client.get_or_create_collection("artifacts")
    
    def index_skill(self, skill: Skill):
        """索引单个 Skill"""
        text = f"{skill.name} {skill.description}"
        embedding = self.embedder.encode(text).tolist()
        self.skills_collection.add(
            ids=[skill.id],
            embeddings=[embedding],
            metadatas=[{"name": skill.name}],
            documents=[text]
        )
    
    def index_artifact(self, artifact: Artifact):
        """索引单个 Artifact"""
        text = f"{artifact.name} {artifact.summary}"
        embedding = self.embedder.encode(text).tolist()
        self.artifacts_collection.add(
            ids=[artifact.id],
            embeddings=[embedding],
            metadatas=[{"name": artifact.name, "type": artifact.type}],
            documents=[text]
        )
    
    def search(self, query: str, top_k: int = 5) -> List[Tuple[str, float]]:
        """搜索相关 Skills"""
        query_embedding = self.embedder.encode(query).tolist()
        results = self.skills_collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )
        
        matches = []
        if results["ids"]:
            for skill_id, distance in zip(results["ids"][0], results["distances"][0]):
                score = 1 - distance
                matches.append((skill_id, score))
        
        return matches
    
    def search_artifacts(self, query: str, top_k: int = 5) -> List[Tuple[str, float]]:
        """搜索相关 Artifacts"""
        query_embedding = self.embedder.encode(query).tolist()
        results = self.artifacts_collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )
        
        matches = []
        if results["ids"]:
            for artifact_id, distance in zip(results["ids"][0], results["distances"][0]):
                score = 1 - distance
                matches.append((artifact_id, score))
        
        return matches
    
    def reindex_all(self, skills: List[Skill]):
        """重建所有索引"""
        self.skills_collection.delete(where={})
        for skill in skills:
            self.index_skill(skill)
