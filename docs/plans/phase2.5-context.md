# Phase 2.5: 动态上下文 (Week 13)

> **时间**: 2026-04-14 ~ 2026-04-20  
> **状态**: ⏳ 待开始  
> **来源**: Claude Cowork 研究启发

---

## 背景

基于 [Claude Cowork 研究](../CLAUDE_COWORK_ANALYSIS.md)，我们发现动态上下文管理是提升 AI 响应质量的关键。

**核心启发**:
1. **对话即知识**: 对话历史是宝贵的知识资产
2. **动态上下文**: 根据项目状态动态构建上下文
3. **知识复用**: 过去的讨论可以指导未来的决策

详见 [整合分析](../COWORK_INTEGRATION_ANALYSIS.md)

---

## Week 13 (4/14 - 4/20): 动态上下文系统

### 开发任务

**1. ProjectContext 类** (`src/context/project_context.py`)

```python
from typing import List, Set, Optional
from ..knowledge_base import KnowledgeBase, Skill, Conversation

class ProjectContext:
    """动态项目上下文
    
    负责:
    1. 维护当前状态
    2. 跟踪最近使用的 Skills
    3. 管理对话历史
    4. 动态构建 Claude 系统提示
    """
    
    def __init__(self, kb: KnowledgeBase):
        self.kb = kb
        self.state: Set[str] = set()
        self.recent_skills: List[str] = []
        self.recent_conversations: List[str] = []
        self.max_recent = 10
    
    def build_system_prompt(self, query: str) -> str:
        """构建 Claude 系统提示
        
        Args:
            query: 用户查询
            
        Returns:
            格式化的系统提示
        """
        # 1. 搜索相关 Skills
        relevant_skills = self.kb.query(query, top_k=3)
        
        # 2. 搜索相关对话
        relevant_convs = self.kb.search_conversations(query, top_k=2)
        
        # 3. 获取当前状态
        state_desc = self.format_state()
        
        # 4. 组合上下文
        return self._format_prompt(
            skills=relevant_skills,
            conversations=relevant_convs,
            state=state_desc,
            query=query
        )
    
    def update_state(self, skill: Skill, success: bool):
        """更新状态
        
        Args:
            skill: 执行的 Skill
            success: 是否成功
        """
        if success:
            # 应用 Skill 效果
            self.state.update(skill.effects)
        
        # 记录最近使用
        self.recent_skills.append(skill.id)
        if len(self.recent_skills) > self.max_recent:
            self.recent_skills.pop(0)
    
    def add_conversation(self, conv_id: str):
        """添加对话到历史"""
        self.recent_conversations.append(conv_id)
        if len(self.recent_conversations) > self.max_recent:
            self.recent_conversations.pop(0)
    
    def format_state(self) -> str:
        """格式化当前状态"""
        if not self.state:
            return "No specific state"
        return ", ".join(sorted(self.state))
    
    def _format_prompt(
        self,
        skills: List[tuple],
        conversations: List[tuple],
        state: str,
        query: str
    ) -> str:
        """格式化系统提示"""
        sections = []
        
        # 项目状态
        sections.append(f"## Current State\n{state}")
        
        # 相关 Skills
        if skills:
            skill_text = "\n".join([
                f"- {s[0]['name']}: {s[0]['description'][:100]}..."
                for s in skills
            ])
            sections.append(f"## Relevant Skills\n{skill_text}")
        
        # 相关对话
        if conversations:
            conv_text = "\n".join([
                f"- {c[0]['title']}: {c[0]['summary'][:100]}..."
                for c in conversations
            ])
            sections.append(f"## Related Discussions\n{conv_text}")
        
        # 当前任务
        sections.append(f"## Current Task\n{query}")
        
        return "\n\n".join(sections)
```

**2. 上下文感知搜索** (`src/knowledge_base/vector_store.py` 扩展)

```python
def search_with_context(
    self,
    query: str,
    context: 'ProjectContext',
    top_k: int = 5
) -> List[Tuple[str, float]]:
    """带上下文的语义搜索
    
    Args:
        query: 查询文本
        context: 项目上下文
        top_k: 返回结果数量
        
    Returns:
        List of (skill_id, adjusted_score) tuples
    """
    # 1. 基础向量搜索
    base_results = self.search(query, top_k * 2)
    
    # 2. 上下文加权调整
    adjusted_results = []
    for skill_id, score in base_results:
        adjusted_score = score
        
        # 最近使用的 Skills 加权
        if skill_id in context.recent_skills:
            recency = context.recent_skills.index(skill_id)
            boost = 0.1 * (1 - recency / len(context.recent_skills))
            adjusted_score += boost
        
        adjusted_results.append((skill_id, adjusted_score))
    
    # 3. 重新排序
    adjusted_results.sort(key=lambda x: x[1], reverse=True)
    
    return adjusted_results[:top_k]
```

**3. 对话历史搜索** (`src/knowledge_base/knowledge_base.py` 扩展)

```python
def search_conversations(
    self,
    query: str,
    top_k: int = 5
) -> List[tuple]:
    """搜索相关对话
    
    Args:
        query: 查询文本
        top_k: 返回结果数量
        
    Returns:
        List of (conversation_data, score) tuples
    """
    matches = self.vector.search_conversations(query, top_k)
    
    results = []
    for conv_id, score in matches:
        conv_data = self.graph.get_node(conv_id)
        if conv_data:
            results.append((conv_data, score))
    
    return results
```

---

### 测试用例

```python
def test_project_context():
    """测试动态上下文"""
    kb = KnowledgeBase()
    kb.load_seeds("seeds/")
    
    context = ProjectContext(kb)
    
    # 测试1: 构建系统提示
    prompt = context.build_system_prompt("帮我处理CSV文件")
    assert "Relevant Skills" in prompt
    assert "CSV" in prompt.lower()
    
    # 测试2: 状态更新
    skill = kb.get_skill("skill_csv_processing")
    context.update_state(skill, success=True)
    assert "has_dataframe" in context.state
    
    # 测试3: 上下文感知搜索
    results = kb.vector.search_with_context(
        "数据处理",
        context,
        top_k=3
    )
    # 最近使用的 CSV 处理应该排名更高
    assert results[0][0] == "skill_csv_processing"

def test_conversation_search():
    """测试对话搜索"""
    kb = KnowledgeBase()
    
    # 添加测试对话
    conv = Conversation(
        id="conv_001",
        title="CSV处理讨论",
        messages=[...],
        summary="讨论了如何处理大型CSV文件的性能优化"
    )
    kb.add_conversation(conv)
    
    # 搜索
    results = kb.search_conversations("CSV性能优化")
    assert len(results) > 0
    assert results[0][0]["id"] == "conv_001"
```

---

### 验收标准

- [ ] ProjectContext 类实现完成
- [ ] 动态系统提示生成可用
- [ ] 上下文感知搜索实现
- [ ] 对话历史搜索实现
- [ ] 单元测试通过
- [ ] 集成测试通过

---

### 依赖关系

**前置条件** (Phase 2 Week 11-12):
- ✅ Conversation 数据模型
- ✅ VectorStore conversations 集合
- ✅ 对话保存和加载

**后续使用** (Phase 3):
- 副产品提取时使用上下文
- Skills 生成时参考历史对话

---

**返回**: [开发计划总览](./README.md)
