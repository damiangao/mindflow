# Mindflow 详细开发计划

> **创建日期**: 2026-01-20  
> **总周期**: 24周 (约6个月)  
> **开始日期**: 2026-01-20

---

## 📅 总体时间线

| 阶段 | 时间 | 目标 |
|------|------|------|
| Phase 1 | Week 1-6 (1/20 - 3/2) | 核心知识库 |
| Phase 2 | Week 7-12 (3/3 - 4/13) | 输入输出层 |
| Phase 3 | Week 13-18 (4/14 - 5/25) | 自我演化 |
| Phase 4 | Week 19-21 (5/26 - 6/15) | UI 和体验 |
| Phase 5 | Week 22-24 (6/16 - 7/6) | 生产就绪 |

---

## 🚀 Phase 1: 核心知识库 (Week 1-6)

### Week 1 (1/20 - 1/26): 环境搭建 + 技术学习

**学习任务**:

| 天数 | 内容 | 产出 |
|------|------|------|
| Day 1-2 | NetworkX 基础 | 能创建/查询图结构 |
| Day 3-4 | Chroma + sentence-transformers | 能进行向量搜索 |
| Day 5 | Pydantic 数据模型 | 能定义验证模型 |

**开发任务**:
- 创建项目基础结构
- 初始化 requirements.txt
- 配置开发环境

**产出目录结构**:
```
mindflow/
├── src/
│   └── __init__.py
├── requirements.txt
├── .env.example
└── pyproject.toml
```

**✅ Milestone 1.1**: 开发环境就绪，能运行图+向量 demo

---

### Week 2 (1/27 - 2/2): 数据模型设计

**学习任务**:
- Claude API 基础调用 (3天)
- Tool Calling 机制

**开发任务**: `src/knowledge_base/models.py`

```python
# 1. 方法论节点
class Methodology:
    id: str
    name: str
    description: str
    principles: List[str]
    evaluation_rule: str      # 评估规则
    weight: float             # 全局权重 0-1
    status: NodeStatus        # active/deprecated/archived/pending
    guided_skills: List[str]  # 指导的 Skills
    created_at: datetime
    updated_at: datetime
    confidence: float

# 2. Skill 节点
class Skill:
    id: str
    name: str
    description: str
    instructions: str         # 执行步骤
    preconditions: List[str]  # 前置条件
    effects: List[str]        # 产生效果
    methodology_scores: Dict[str, float]  # 方法论评分
    parent_methodologies: List[str]
    called_skills: List[str]
    artifacts: List[str]
    success_rate: float
    usage_count: int
    created_at: datetime
    updated_at: datetime

# 3. 副产品节点
class Artifact:
    id: str
    name: str
    type: ArtifactType  # Code/Function/Template/Document/Config
    content: str
    parent_skills: List[str]
    usage_count: int
    tags: List[str]
    created_at: datetime
```

**✅ Milestone 1.2**: 三层数据模型定义完成，通过 Pydantic 验证

---

### Week 3 (2/3 - 2/9): 图存储层实现

**开发任务**: `src/knowledge_base/graph_store.py`

```python
class GraphStore:
    """图数据库抽象层"""
    
    # 节点操作
    def add_node(node) -> str
    def get_node(node_id: str) -> Optional[Node]
    def update_node(node_id: str, updates: dict) -> bool
    def delete_node(node_id: str) -> bool
    
    # 关系操作
    def add_edge(source_id, target_id, relation, properties) -> bool
    def get_edges(node_id, direction) -> List[Edge]
    def remove_edge(source_id, target_id, relation) -> bool
    
    # 查询操作
    def get_skills_by_methodology(meth_id) -> List[Skill]
    def get_artifacts_by_skill(skill_id) -> List[Artifact]
    def get_skill_chain(skill_id, depth) -> List[Skill]
```

**实现方案**:
- 开发环境: NetworkX + JSON 持久化
- 生产环境: Neo4j (后续迁移)

**✅ Milestone 1.3**: 图存储层 CRUD 完成，能持久化保存

---

### Week 4 (2/10 - 2/16): 向量索引层实现

**开发任务**: `src/knowledge_base/vector_store.py`

```python
class VectorStore:
    """向量搜索层"""
    
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.embedder = SentenceTransformer(model_name)
        self.collection = chromadb.Collection("skills")
    
    # 索引操作
    def index_skill(skill: Skill) -> None
    def reindex_all() -> None
    
    # 搜索操作
    def search(query: str, top_k: int = 5) -> List[Tuple[Skill, float]]
    def search_with_filter(query, filters, top_k) -> List[Tuple[Skill, float]]
```

**✅ Milestone 1.4**: 向量搜索可用，输入文本能返回相关 Skills

---

### Week 5 (2/17 - 2/23): 冷启动种子库

**种子库内容**:

| 层级 | 数量 | 内容 |
|------|------|------|
| 方法论 | 5个 | 简单优先、标准库优先、一致性、迭代、复盘 |
| Skills | 5个 | CSV处理、任务分解、Python脚本、文件读写、日复盘 |
| 副产品 | 5个 | 每个 Skill 1个核心代码片段 |

**文件格式示例**:

```yaml
# seeds/methodologies/simple_first.yaml
id: meth_simple
name: 简单优于复杂
description: 优先选择简单直接的解决方案
principles:
  - 能用一行代码解决的不用十行
  - 避免过度设计
  - 先让它工作，再优化
evaluation_rule: 检查代码行数和复杂度
weight: 0.9
status: active

# seeds/skills/csv_processing.yaml
id: skill_csv
name: CSV 文件处理
description: 读取、解析、处理 CSV 格式数据
instructions: |
  1. 使用 pandas 读取 CSV 文件
  2. 检查数据完整性
  3. 处理缺失值
  4. 返回 DataFrame
preconditions: ["has_csv_file"]
effects: ["has_dataframe"]
methodology_scores:
  meth_simple: 0.8
  meth_stdlib: 0.9
called_skills: ["file_read"]
```

**✅ Milestone 1.5**: 种子库加载完成，系统有初始知识

---

### Week 6 (2/24 - 3/2): 知识库整合 + 验收

**开发任务**: `src/knowledge_base/knowledge_base.py`

```python
class KnowledgeBase:
    """知识库统一接口"""
    
    def __init__(self):
        self.graph = GraphStore()
        self.vector = VectorStore()
    
    def query(user_input: str) -> QueryResult:
        """向量搜索 → 方法论评分 → 返回最佳匹配"""
    
    def activate_skill(skill_id: str) -> ActivationResult:
        """激活 Skill，返回相关方法论、子 Skills、副产品"""
    
    def get_stats() -> KBStats
```

**验收测试**:
```python
def test_end_to_end():
    kb = KnowledgeBase()
    kb.load_seeds("seeds/")
    
    result = kb.query("帮我处理这个CSV文件")
    assert result.best_skill.name == "CSV 文件处理"
    assert result.score > 0.7
```

**🎯 Phase 1 验收标准**:
- ✅ 三层知识库结构完整
- ✅ 能手动添加和查询节点
- ✅ 向量搜索返回相关 Skills
- ✅ 端到端: "处理CSV" → 激活 Skill

---

## 🔄 Phase 2: 输入输出层 (Week 7-12)

### Week 7-8 (3/3 - 3/16): 意图识别模块

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

### Week 9-10 (3/17 - 3/30): Skills 执行引擎

**开发任务**: `src/output_layer/skill_executor.py`

```python
class SkillExecutor:
    """Skills 执行引擎"""
    
    def execute(skill: Skill, context: ExecutionContext) -> ExecutionResult:
        """执行单个 Skill"""
    
    def plan_and_execute(intent: Intent) -> List[ExecutionResult]:
        """规划并执行 Skills 序列"""

class SkillPlanner:
    """Skills 规划器 (简化版 HTN)"""
    
    def plan(goal_effects: List[str], current_state: Set[str]) -> List[Skill]:
        """贪心搜索，返回执行序列"""
```

**✅ Milestone 2.2**: 能执行单个 Skill 并返回结果

---

### Week 11-12 (3/31 - 4/13): 对话管理 + Skills 扩展

**开发任务**: `src/output_layer/conversation.py`

```python
class ConversationManager:
    """对话管理器"""
    
    def process(user_input: str) -> Response:
        """完整处理: 意图识别 → Skills 匹配 → 执行 → 回复"""
    
    def generate_response(result: ExecutionResult) -> str:
        """生成自然语言回复"""
```

**Skills 扩展** (5 → 20):

| 类别 | Skills |
|------|--------|
| 生活管理 | 任务分解、任务跟踪、日程规划、笔记整理、日复盘、周复盘 |
| 数据处理 | CSV处理、JSON处理、数据清洗、数据验证、数据转换、数据可视化 |
| 代码辅助 | Python脚本、函数重构、错误处理 |
| 通用工具 | 文件读写、命令行调用 |

**🎯 Phase 2 验收标准**:
- ✅ 用户输入 → Skills 匹配 → 执行 → 返回结果
- ✅ 首次命中率 > 80%
- ✅ 20个 Skills 可用
- ✅ 结构化日志记录决策过程

---

## 🧬 Phase 3: 自我演化 (Week 13-18)

### Week 13-14 (4/14 - 4/27): 副产品提取

**开发任务**: `src/evolution/artifact_extractor.py`

```python
class ArtifactExtractor:
    """副产品提取器"""
    
    def extract_from_execution(result: ExecutionResult) -> List[Artifact]:
        """从执行结果中提取代码片段、模板、配置"""
    
    def extract_code_snippets(code: str) -> List[CodeArtifact]:
        """使用 AST 解析代码，提取函数"""
    
    def should_save(artifact: Artifact) -> bool:
        """判断是否值得保存"""
```

**✅ Milestone 3.1**: 能从代码执行中自动提取函数级副产品

---

### Week 15-16 (4/28 - 5/11): Skills 自动生成

**开发任务**: `src/evolution/skill_generator.py`

```python
class SkillGenerator:
    """Skills 生成器"""
    
    def generate_from_artifacts(artifacts: List[Artifact]) -> Optional[Skill]:
        """从多个副产品中识别模式，生成新 Skill"""
    
    def generate_from_conversation(history: List[Message]) -> Optional[Skill]:
        """从对话历史中学习新 Skill"""
    
    def validate_skill(skill: Skill) -> ValidationResult:
        """验证生成的 Skill 质量"""
```

**✅ Milestone 3.2**: 能自动生成新 Skill 并提交审核

---

### Week 17-18 (5/12 - 5/25): 用户交互 + 审核机制

**开发任务**: `src/evolution/review_queue.py`

```python
class ReviewQueue:
    """审核队列"""
    
    def add(item: ReviewItem) -> str
    def get_pending() -> List[ReviewItem]
    def approve(item_id: str) -> bool
    def reject(item_id: str, reason: str) -> bool
    def auto_approve_expired() -> int  # 1小时后自动批准

class RiskAssessor:
    """风险评估器"""
    
    RISK_LEVELS = {
        "artifact_add": 0.1,
        "skill_update": 0.5,
        "skill_create": 0.6,
        "methodology_change": 0.9
    }
    
    def assess(operation: Operation) -> float
    def get_action(risk: float) -> str:
        # < 0.3: silent, 0.3-0.8: queue, > 0.8: confirm
```

**🎯 Phase 3 验收标准**:
- ✅ 能从任务执行中自动提取副产品
- ✅ 能生成新 Skills 并请求用户审核
- ✅ 三级交互策略实现
- ✅ 自动化测试: 模拟交互 → 生成有意义的 Skills

---

## 🎨 Phase 4: UI 和体验 (Week 19-21)

### Week 19-20 (5/26 - 6/8): Gradio 界面

**开发任务**: `src/ui/app.py`

```python
import gradio as gr

def create_app(mindflow: Mindflow) -> gr.Blocks:
    with gr.Blocks() as app:
        # 主对话区
        chatbot = gr.Chatbot()
        msg = gr.Textbox(placeholder="输入你的请求...")
        
        # 侧边栏: 知识库状态
        with gr.Accordion("知识库"):
            stats = gr.JSON()
        
        # 审核队列
        with gr.Accordion("待审核"):
            review_list = gr.Dataframe()
    
    return app
```

**界面功能**:
- 对话交互
- 知识库浏览
- 审核队列管理
- 执行日志查看

**✅ Milestone 4.1**: 基础 UI 可用

---

### Week 21 (6/9 - 6/15): 知识库可视化

**开发任务**: `src/ui/visualizer.py`

```python
def visualize_knowledge_graph(kb: KnowledgeBase) -> str:
    """生成知识图谱可视化"""

def visualize_skill_chain(skill_id: str) -> str:
    """可视化 Skill 调用链"""
```

**🎯 Phase 4 验收标准**:
- ✅ Gradio 界面完整
- ✅ 知识库可视化
- ✅ 用户体验流畅

---

## 🏭 Phase 5: 生产就绪 (Week 22-24)

### Week 22-23 (6/16 - 6/29): 错误处理 + 测试

**开发任务**: `src/core/error_handler.py`

```python
class ErrorHandler:
    """分层错误处理"""
    
    def handle_llm_error(error) -> Response:
        """LLM 调用错误: 重试/降级"""
    
    def handle_skill_error(error, skill) -> Response:
        """Skill 执行错误: 跳过/替代"""
    
    def handle_kb_error(error) -> Response:
        """知识库错误: 降级搜索"""
```

**测试结构**:
```
tests/
├── unit/
│   ├── test_models.py
│   ├── test_graph_store.py
│   ├── test_vector_store.py
│   └── test_skill_executor.py
├── integration/
│   ├── test_knowledge_base.py
│   └── test_conversation.py
└── e2e/
    └── test_full_flow.py
```

**✅ Milestone 5.1**: 测试覆盖率 > 70%

---

### Week 24 (6/30 - 7/6): 文档 + 部署

**任务**:
- 完善 API 文档
- 编写用户手册
- Docker 打包
- 发布 v1.0.0

**🎯 Phase 5 验收标准**:
- ✅ 错误处理完善
- ✅ 测试覆盖充分
- ✅ 文档完整
- ✅ 可部署运行

---

## 📊 里程碑总览

```
Week 1  ──────────────────────────────────────────────────────► Week 24
   │                                                               │
   ▼                                                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│  Phase 1: 核心知识库 (Week 1-6)                                      │
│  ├─ M1.1 (W1): 环境就绪                                             │
│  ├─ M1.2 (W2): 数据模型完成                                          │
│  ├─ M1.3 (W3): 图存储完成                                            │
│  ├─ M1.4 (W4): 向量搜索完成                                          │
│  ├─ M1.5 (W5): 种子库完成                                            │
│  └─ M1.6 (W6): Phase 1 验收 ✓                                       │
├──────────────────────��──────────────────────────────────────────────┤
│  Phase 2: 输入输出层 (Week 7-12)                                     │
│  ├─ M2.1 (W8): 意图识别完成                                          │
│  ├─ M2.2 (W10): 执行引擎完成                                         │
│  └─ M2.3 (W12): Phase 2 验收 ✓                                      │
├─────────────────────────────────────────────────────────────────────┤
│  Phase 3: 自我演化 (Week 13-18)                                      │
│  ├─ M3.1 (W14): 副产品提取完成                                        │
│  ├─ M3.2 (W16): Skills 生成完成                                      │
│  └─ M3.3 (W18): Phase 3 验收 ✓                                      │
├─────────────────────────────────────────────────────────────────────┤
│  Phase 4: UI 和体验 (Week 19-21)                                     │
│  └─ M4.1 (W21): UI 完成 ✓                                           │
├─────────────────────────────────────────────────────────────────────┤
│  Phase 5: 生产就绪 (Week 22-24)                                      │
│  └─ M5.1 (W24): v1.0.0 发布 ✓                                       │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 🔍 可复用的开源项目

在开始开发前，建议调研以下开源项目：

| 组件 | 可能的开源项目 | 复用价值 |
|------|---------------|---------|
| 知识图谱 + LLM | Microsoft GraphRAG, LlamaIndex | 高 |
| Agent 框架 | LangGraph, CrewAI, AutoGPT | 高 |
| 向量搜索封装 | LangChain VectorStore | 中 |
| 自我演化 | Voyager Skill Library | 参考 |
| HTN Planning | PyHOP | 参考 |

---

## 🎯 本周任务 (Week 1)

**立即开始**:
1. 创建项目基础结构
2. 初始化 requirements.txt
3. 学习 NetworkX 基础

**本周目标**:
- 完成 NetworkX + Chroma 学习
- 搭建开发环境
- 运行第一个图+向量 demo

---

**创建日期**: 2026-01-20  
**维护者**: [@damiangao](https://github.com/damiangao)
