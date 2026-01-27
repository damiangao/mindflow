# Mindflow 详细开发计划

> **创建日期**: 2026-01-20  
> **更新日期**: 2026-01-27  
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

### Week 1 (1/20 - 1/26): 环境搭建 + 基础实现 ✅

**已完成**:
- ✅ 三层数据模型 (Pydantic): Methodology, Skill, Artifact
- ✅ 图存储层 (NetworkX + JSON 持久化)
- ✅ 向量索引层 (Chroma + sentence-transformers)
- ✅ 统一接口 (KnowledgeBase)
- ✅ Artifact 轻量化优化 (summary + filepath)

**✅ Milestone 1.1**: 核心知识库架构完成

---

### Week 2 (1/27 - 2/2): Agent Skills 规范 + 种子库扩展

> **更新日期**: 2026-01-27  
> **调整原因**: 基于 Obsidian Skills 调研，优先实现业界标准兼容

#### ✅ 已完成 (1/27)

**Agent Skills 规范迁移**:
- ✅ Skill 格式从 YAML 迁移到 Markdown (SKILL.md)
- ✅ 遵循 [Agent Skills Specification](https://agentskills.io/specification)
- ✅ 数据模型增加 `to_markdown()` / `from_markdown()` 方法
- ✅ 种子库加载器支持新格式 + 向后兼容
- ✅ 创建格式规范文档 `docs/SKILL_FORMAT.md`
- ✅ Obsidian Skills 调研报告 `docs/research/obsidian_skills_analysis.md`

**新目录结构**:
```
seeds/skills/
├── csv-processing/
│   └── SKILL.md          # Agent Skills 规范格式
├── daily-review/
│   └── SKILL.md
├── file-io/
│   └── SKILL.md
├── python-script/
│   └── SKILL.md
└── task-decompose/
    └── SKILL.md
```

#### 📋 本周剩余任务 (1/28 - 2/2)

**1. 种子库扩展** (2天)
- [ ] 扩展到 15-20 个 Skills (SKILL.md 格式)
- [ ] 补充 Methodology 关联关系
- [ ] 每个 Skill 包含完整文档（示例、常见问题）

**新增 Skills 计划**:

| 类别 | Skills |
|------|--------|
| 数据处理 | json-processing, data-validation, data-transform |
| 生活管理 | weekly-review, task-tracking, note-organize |
| 代码辅助 | code-refactor, error-handling |
| 通用工具 | command-line, api-request |

**2. 方法论评分机制** (2天)
- [ ] 实现加权归一化算法
- [ ] Skill 查询时自动评分排序
- [ ] 测试评分准确性

```python
def calculate_skill_score(skill, methodologies):
    weighted_sum = 0
    total_weight = 0
    
    for meth in methodologies:
        score = skill.methodology_scores.get(meth.id, 0.5)
        weighted_sum += meth.weight * score
        total_weight += meth.weight
    
    return weighted_sum / total_weight
```

**3. JSON Canvas 导出** (1天，可选)
- [ ] 实现知识图谱导出为 Obsidian Canvas 格式
- [ ] 支持在 Obsidian 中可视化

**✅ Milestone 1.2**: 
- ✅ Agent Skills 规范兼容
- 15-20 个 Skills 种子库
- 方法论评分机制可用

---

### Week 3 (2/3 - 2/9): Skills 组合规划器

**开发任务**: `src/planner/skill_planner.py`

```python
class SkillPlanner:
    """Skills 组合规划器 (简化版 HTN)"""
    
    def plan(goal_effects: List[str], current_state: Set[str]) -> List[Skill]:
        """贪心搜索，返回执行序列"""
        pass
    
    def check_preconditions(skill: Skill, state: Set[str]) -> bool:
        """检查前置条件是否满足"""
        pass
    
    def apply_effects(skill: Skill, state: Set[str]) -> Set[str]:
        """应用 Skill 效果到状态"""
        pass
```

**规划流程**:
```
用户: "处理CSV并生成图表"
    ↓
LLM 解析目标 → ["has_dataframe", "has_chart"]
    ↓
当前状态: {"has_csv_file"}
    ↓
规划器搜索 → [Skill("CSV处理"), Skill("数据可视化")]
    ↓
返回执行计划
```

**✅ Milestone 1.3**: Skills 组合规划可用，能自动规划多步骤任务

---

### Week 4 (2/10 - 2/16): 可视化 + 导出功能

**开发任务**: `src/export/`

```python
# 1. JSON Canvas 导出 (Obsidian 兼容)
class CanvasExporter:
    def export_knowledge_graph(kb: KnowledgeBase) -> dict
    def export_skill_chain(skill_id: str) -> dict

# 2. Markdown 导出 (Agent Skills 规范)
class MarkdownExporter:
    def export_skill(skill: Skill) -> str
    def export_all_skills(kb: KnowledgeBase, output_dir: Path)
```

**可视化功能**:
- [ ] 知识图谱导出为 JSON Canvas
- [ ] 在 Obsidian 中可视化三层架构
- [ ] Skill 调用链可视化

**✅ Milestone 1.4**: 知识库可视化，支持 Obsidian 集成

---

### Week 5 (2/17 - 2/23): 向量搜索优化

**开发任务**: `src/knowledge_base/vector_store.py` 优化

- [ ] 上下文加权搜索
- [ ] 多集合联合查询
- [ ] 搜索结果缓存

```python
class VectorStore:
    def search_with_context(query: str, context: Context) -> List[Skill]:
        """带上下文的语义搜索"""
        # 1. 基础向量搜索
        # 2. 上下文加权调整
        # 3. 方法论评分排序
        pass
```

**✅ Milestone 1.5**: 向量搜索优化完成，首次命中率 > 80%

---

### Week 6 (2/24 - 3/2): 知识库整合 + Phase 1 验收

**开发任务**: 整合测试 + 文档完善

```python
def test_end_to_end():
    kb = KnowledgeBase()
    kb.load_seeds("seeds/")
    
    # 测试1: 语义搜索
    result = kb.query("帮我处理这个CSV文件")
    assert result.best_skill.name == "CSV文件处理"
    
    # 测试2: Skills 组合
    plan = kb.plan(["has_chart"], {"has_csv_file"})
    assert len(plan) >= 2
    
    # 测试3: 可视化导出
    canvas = kb.export_canvas()
    assert "nodes" in canvas
```

**🎯 Phase 1 验收标准**:
- ✅ 三层知识库结构完整
- ✅ Agent Skills 规范兼容
- ✅ 15-20 个 Skills 种子库
- ✅ 方法论评分机制
- ✅ Skills 组合规划
- ✅ Obsidian 可视化导出
- ✅ 端到端测试通过

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

**Skills 扩展** (5 → 30):

| 类别 | Skills |
|------|--------|
| 生活管理 | 任务分解、任务跟踪、日程规划、笔记整理、日复盘、周复盘 |
| 数据处理 | CSV处理、JSON处理、数据清洗、数据验证、数据转换、数据可视化 |
| 代码辅助 | Python脚本、函数重构、错误处理、代码审查 |
| 通用工具 | 文件读写、命令行调用、API请求、文本处理 |

**🎯 Phase 2 验收标准**:
- ✅ 用户输入 → Skills 匹配 → 执行 → 返回结果
- ✅ 首次命中率 > 80%
- ✅ 30个 Skills 可用
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

### Week 21 (6/9 - 6/15): 知识库可视化增强

**开发任务**: `src/ui/visualizer.py`

- [ ] 交互式知识图谱
- [ ] Skill 调用链可视化
- [ ] 实时更新

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
│  ├─ M1.1 (W1): 核心架构完成 ✅                                       │
│  ├─ M1.2 (W2): Agent Skills 规范 + 种子库 (进行中)                   │
│  ├─ M1.3 (W3): Skills 组合规划器                                     │
│  ├─ M1.4 (W4): 可视化导出                                            │
│  ├─ M1.5 (W5): 向量搜索优化                                          │
│  └─ M1.6 (W6): Phase 1 验收                                         │
├─────────────────────────────────────────────────────────────────────┤
│  Phase 2: 输入输出层 (Week 7-12)                                     │
│  ├─ M2.1 (W8): 意图识别完成                                          │
│  ├─ M2.2 (W10): 执行引擎完成                                         │
│  └─ M2.3 (W12): Phase 2 验收                                        │
├─────────────────────────────────────────────────────────────────────┤
│  Phase 3: 自我演化 (Week 13-18)                                      │
│  ├─ M3.1 (W14): 副产品提取完成                                        │
│  ├─ M3.2 (W16): Skills 生成完成                                      │
│  └─ M3.3 (W18): Phase 3 验收                                        │
├─────────────────────────────────────────────────────────────────────┤
│  Phase 4: UI 和体验 (Week 19-21)                                     │
│  └─ M4.1 (W21): UI 完成                                             │
├─────────────────────────────────────────────────────────────────────┤
│  Phase 5: 生产就绪 (Week 22-24)                                      │
│  └─ M5.1 (W24): v1.0.0 发布                                         │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 🔑 关键设计决策

### 技术栈

| 组件 | 开发阶段 | 生产阶段 |
|------|---------|---------|
| 图数据库 | NetworkX | Neo4j |
| 向量搜索 | Chroma | Chroma / Pinecone |
| LLM | Claude API | Claude API |
| Skill 格式 | Agent Skills (Markdown) | Agent Skills (Markdown) |
| UI | Gradio | Gradio / Web |

### 核心原则

1. **简单优先**: 先让它工作，再优化
2. **标准兼容**: 遵循 Agent Skills 规范
3. **渐进演化**: 从使用中学习
4. **用户控制**: 三级交互策略

---

## 📚 参考文档

- [Agent Skills Specification](https://agentskills.io/specification)
- [Obsidian Skills 调研](docs/research/obsidian_skills_analysis.md)
- [Skill 格式规范](docs/SKILL_FORMAT.md)
- [技术设计](docs/TECHNICAL_DESIGN.md)
- [开发进度](docs/PROGRESS.md)

---

**创建日期**: 2026-01-20  
**最后更新**: 2026-01-27  
**维护者**: [@damiangao](https://github.com/damiangao)
