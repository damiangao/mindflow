# Phase 3: 自我演化 (Week 13-18)

> **时间**: 2026-04-14 ~ 2026-05-25  
> **状态**: ⏳ 待开始

---

## Week 13-14 (4/14 - 4/27): 副产品提取

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

## Week 15-16 (4/28 - 5/11): Skills 自动生成

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

## Week 17-18 (5/12 - 5/25): 用户交互 + 审核机制

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

**返回**: [开发计划总览](./README.md)
