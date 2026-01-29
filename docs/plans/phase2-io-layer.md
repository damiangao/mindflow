# Phase 2: 输入输出层 (Week 7-12)

> **时间**: 2026-03-03 ~ 2026-04-13  
> **状态**: ⏳ 待开始  
> **更新**: 2026-01-29 - 整合 Claude Cowork 改进建议

---

## Week 7-8 (3/3 - 3/16): 意图识别模块

**开发任务**: `src/input_layer/intent_recognizer.py`

```python
class IntentRecognizer:
    """意图识别器"""
    
    def recognize(user_input: str, context: Context) -> Intent:
        """调用 LLM 识别意图"""
    
    def extract_context(user_input: str) -> Context:
        """提取情境信息"""

class Intent:
    task_type: str           # data_processing, planning, coding...
    entities: Dict[str, Any] # {"file_type": "csv", "operation": "clean"}
    required_effects: List[str]  # ["has_dataframe", "has_clean_data"]
    confidence: float
```

**✅ Milestone 2.1**: 意图识别准确率 > 80%

---

## Week 9-10 (3/17 - 3/30): Skills 执行引擎

**开发任务**: `src/output_layer/skill_executor.py`

```python
class SkillExecutor:
    """Skills 执行引擎"""
    
    def execute(skill: Skill, context: ExecutionContext) -> ExecutionResult:
        """执行单个 Skill"""
    
    def plan_and_execute(intent: Intent) -> List[ExecutionResult]:
        """规划并执行 Skills 序列"""
```

**✅ Milestone 2.2**: 能执行单个 Skill 并返回结果

---

## Week 11-12 (3/31 - 4/13): 对话管理 + 对话历史 🆕

> **更新**: 基于 [Claude Cowork 研究](../CLAUDE_COWORK_ANALYSIS.md) 新增对话历史管理

### 原有任务: 对话管理

**开发任务**: `src/output_layer/conversation.py`

```python
class ConversationManager:
    """对话管理器"""
    
    def process(user_input: str) -> Response:
        """完整处理: 意图识别 → Skills 匹配 → 执行 → 回复"""
    
    def generate_response(result: ExecutionResult) -> str:
        """生成自然语言回复"""
```

### 🆕 新增任务: 对话历史管理

**来源**: [整合分析](../COWORK_INTEGRATION_ANALYSIS.md)

**1. 数据模型** (`src/knowledge_base/models.py` 扩展)

```python
class Message(BaseModel):
    """对话消息"""
    role: str  # "user" or "assistant"
    content: str
    timestamp: datetime = Field(default_factory=datetime.now)
    metadata: dict = {}
    
    # 可选: 关联的 Skills
    related_skills: List[str] = []

class Conversation(BaseModel):
    """对话记录
    
    设计决策: 作为特殊的 Artifact 类型，复用现有架构
    """
    id: str
    title: str  # 自动生成或用户指定
    messages: List[Message]
    summary: str  # 用于向量索引
    
    # 关联信息
    related_skills: List[str] = []  # 对话中使用的 Skills
    tags: List[str] = []
    
    # 时间戳
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    
    def generate_summary(self) -> str:
        """自动生成对话摘要（使用 Claude）"""
        pass
    
    def to_artifact(self) -> Artifact:
        """转换为 Artifact 以复用存储"""
        return Artifact(
            id=self.id,
            name=self.title,
            type=ArtifactType.DOCUMENT,
            summary=self.summary,
            filepath=f"conversations/{self.id}.json",
            tags=self.tags
        )
```

**2. 向量存储扩展** (`src/knowledge_base/vector_store.py`)

```python
class VectorStore:
    def __init__(self, persist_dir: str, model_name: str):
        # ... 现有代码 ...
        
        # 🆕 新增 conversations 集合
        self.conversations_collection = self.client.get_or_create_collection(
            name="conversations",
            embedding_function=self.embedding_function
        )
    
    def index_conversation(self, conversation: Conversation):
        """索引对话"""
        text = f"{conversation.title} {conversation.summary}"
        self.conversations_collection.add(
            ids=[conversation.id],
            documents=[text],
            metadatas=[{"title": conversation.title}]
        )
    
    def search_conversations(self, query: str, top_k: int = 5) -> List[Tuple[str, float]]:
        """搜索相关对话"""
        results = self.conversations_collection.query(
            query_texts=[query],
            n_results=top_k
        )
        
        matches = []
        if results["ids"]:
            for conv_id, distance in zip(results["ids"][0], results["distances"][0]):
                score = 1 - distance
                matches.append((conv_id, score))
        
        return matches
```

**3. 知识库扩展** (`src/knowledge_base/knowledge_base.py`)

```python
class KnowledgeBase:
    # ... 现有代码 ...
    
    def add_conversation(self, conversation: Conversation) -> str:
        """添加对话记录"""
        # 1. 保存到图数据库
        conv_id = self.graph.add_node(conversation)
        
        # 2. 索引到向量数据库
        self.vector.index_conversation(conversation)
        
        # 3. 建立与 Skills 的关系
        for skill_id in conversation.related_skills:
            self.graph.add_edge(skill_id, conv_id, "discussed_in")
        
        # 4. 保存对话文件
        self._save_conversation_file(conversation)
        
        return conv_id
    
    def get_conversation(self, conv_id: str) -> Optional[Conversation]:
        """获取对话记录"""
        data = self.graph.get_node(conv_id)
        if data:
            return Conversation(**data)
        return None
    
    def search_conversations(self, query: str, top_k: int = 5) -> List[tuple]:
        """搜索相关对话"""
        matches = self.vector.search_conversations(query, top_k)
        
        results = []
        for conv_id, score in matches:
            conv_data = self.graph.get_node(conv_id)
            if conv_data:
                results.append((conv_data, score))
        
        return results
    
    def _save_conversation_file(self, conversation: Conversation):
        """保存对话到文件"""
        filepath = Path(f"conversations/{conversation.id}.json")
        filepath.parent.mkdir(parents=True, exist_ok=True)
        filepath.write_text(
            conversation.model_dump_json(indent=2, ensure_ascii=False),
            encoding="utf-8"
        )
```

**4. 对话管理器增强** (`src/output_layer/conversation.py`)

```python
class ConversationManager:
    """对话管理器 - 增强版"""
    
    def __init__(self, kb: KnowledgeBase):
        self.kb = kb
        self.current_messages: List[Message] = []
        self.current_skills: List[str] = []
    
    def process(self, user_input: str) -> Response:
        """完整处理流程"""
        # 1. 记录用户消息
        self.current_messages.append(Message(
            role="user",
            content=user_input
        ))
        
        # 2. 意图识别 → Skills 匹配 → 执行
        result = self._execute_pipeline(user_input)
        
        # 3. 记录助手回复
        self.current_messages.append(Message(
            role="assistant",
            content=result.response,
            related_skills=result.used_skills
        ))
        
        # 4. 更新使用的 Skills
        self.current_skills.extend(result.used_skills)
        
        return result
    
    def save_conversation(self, title: str = None) -> Conversation:
        """保存当前对话"""
        # 1. 生成标题（如果未提供）
        if not title:
            title = self._generate_title()
        
        # 2. 生成摘要
        summary = self._generate_summary()
        
        # 3. 创建对话记录
        conversation = Conversation(
            id=f"conv_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            title=title,
            messages=self.current_messages.copy(),
            summary=summary,
            related_skills=list(set(self.current_skills))
        )
        
        # 4. 保存到知识库
        self.kb.add_conversation(conversation)
        
        # 5. 清空当前对话
        self.current_messages = []
        self.current_skills = []
        
        return conversation
    
    def _generate_title(self) -> str:
        """使用 Claude 生成对话标题"""
        # 取前几条消息生成标题
        pass
    
    def _generate_summary(self) -> str:
        """使用 Claude 生成对话摘要"""
        # 总结整个对话
        pass
```

---

### Skills 扩展 (5 → 30)

| 类别 | Skills |
|------|--------|
| 生活管理 | 任务分解、任务跟踪、日程规划、笔记整理、日复盘、周复盘 |
| 数据处理 | CSV处理、JSON处理、数据清洗、数据验证、数据转换、数据可视化 |
| 代码辅助 | Python脚本、函数重构、错误处理、代码审查 |
| 通用工具 | 文件读写、命令行调用、API请求、文本处理 |

---

### 新增目录结构

```
mindflow/
├── conversations/           # 🆕 对话历史存储
│   ├── conv_20260401_001.json
│   ├── conv_20260401_002.json
│   └── ...
├── src/
│   ├── knowledge_base/
│   │   ├── models.py       # 🔄 新增 Message, Conversation
│   │   ├── vector_store.py # 🔄 新增 conversations 集合
│   │   └── knowledge_base.py # 🔄 新增对话管理方法
│   └── output_layer/
│       └── conversation.py  # 🔄 增强对话管理
```

---

### 验收标准

**🎯 Phase 2 验收标准** (更新):

- ✅ 用户输入 → Skills 匹配 → 执行 → 返回结果
- ✅ 首次命中率 > 80%
- ✅ 30个 Skills 可用
- ✅ 结构化日志记录决策过程
- 🆕 ✅ 对话历史保存和加载
- 🆕 ✅ 对话语义搜索可用
- 🆕 ✅ 对话与 Skills 关联

---

### 工作量估算

| 任务 | 原计划 | 新增 | 总计 |
|------|--------|------|------|
| Week 7-8: 意图识别 | 2周 | - | 2周 |
| Week 9-10: 执行引擎 | 2周 | - | 2周 |
| Week 11-12: 对话管理 | 2周 | +2天 | 2周 |
| **总计** | 6周 | +2天 | 6周 |

> 新增任务可在 Week 11-12 内完成，无需延长 Phase 2 时间

---

**返回**: [开发计划总览](./README.md)  
**下一阶段**: [Phase 2.5: 动态上下文](./phase2.5-context.md)
