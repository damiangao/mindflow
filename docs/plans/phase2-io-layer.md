# Phase 2: 输入输出层 (Week 7-12)

> **时间**: 2026-03-03 ~ 2026-04-13  
> **状态**: ⏳ 待开始

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

## Week 11-12 (3/31 - 4/13): 对话管理 + Skills 扩展

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

**返回**: [开发计划总览](./README.md)
