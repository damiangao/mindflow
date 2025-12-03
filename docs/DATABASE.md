# Mindflow 数据库设计文档

## 数据库概述

Mindflow使用SQLite作为MVP阶段的数据库，提供简单、零配置的本地存储方案。数据库设计充分考虑了未来升级到PostgreSQL和多用户支持的可能性。

## 核心设计原则

1. **单用户优先，多用户预留**：所有表都包含user_id字段，为未来的多用户隔离做准备
2. **数据完整性**：使用外键和约束确保数据一致性
3. **查询性能**：适当的索引设计支持常见查询
4. **灵活的JSON存储**：对于复杂的嵌套数据使用JSON字段
5. **审计追踪**：保留created_at和updated_at时间戳

## 数据库架构

### 表结构总览

```
┌─────────────────────────────────────────┐
│ user_profile (用户档案)                  │
├─────────────────────────────────────────┤
│ 1:N                                      │
└──────────────┬──────────────────────────┘
               │
      ┌────────┼────────┬──────────┬──────────┐
      │        │        │          │          │
      ▼        ▼        ▼          ▼          ▼
  events   plans   reviews  conversation  user_behavior
                             _history     _features
```

## 详细表结构

### 1. user_profile - 用户档案表

**目的**：存储用户的基本信息和初始档案

**字段定义**：

```sql
CREATE TABLE user_profile (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL UNIQUE,  -- 预留多用户隔离
    name TEXT NOT NULL,
    goals TEXT,                    -- JSON: 用户的主要目标 ["目标1", "目标2", ...]
    values TEXT,                   -- JSON: 用户的价值观 ["价值观1", "价值观2", ...]
    work_direction TEXT,           -- 用户的工作/学习方向
    personality_traits TEXT,       -- JSON: 性格特征 {"性格1": true, "性格2": false}
    weak_points TEXT,             -- JSON: 需要改进的地方 ["弱点1", "弱点2", ...]
    preferred_reminder_style TEXT, -- 用户偏好的提醒方式 (gentle/direct/humorous)
    timezone TEXT,                -- 用户所在时区 (e.g., "Asia/Shanghai")
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CHECK (name IS NOT NULL AND name != '')
);

CREATE INDEX idx_user_profile_user_id ON user_profile(user_id);
```

**数据示例**：

```json
{
  "id": "prof_001",
  "user_id": "user_001",
  "name": "张三",
  "goals": ["完成项目X", "学习机器学习", "健身"],
  "values": ["成长", "自由", "家庭"],
  "work_direction": "机器学习工程师",
  "personality_traits": {
    "外向": true,
    "完美主义": true,
    "容易焦虑": true
  },
  "weak_points": ["执行力较差", "容易拖延"],
  "preferred_reminder_style": "direct",
  "timezone": "Asia/Shanghai",
  "created_at": "2024-01-01T08:00:00",
  "updated_at": "2024-01-15T10:30:00"
}
```

---

### 2. user_behavior_features - 用户行为特征库

**目的**：存储系统通过交互逐步学习的用户特征，带有置信度评分

**字段定义**：

```sql
CREATE TABLE user_behavior_features (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    feature_key TEXT NOT NULL,    -- 特征键 (e.g., "work_time_peak", "decision_style")
    feature_value TEXT NOT NULL,  -- 特征值 (JSON格式)
    confidence FLOAT DEFAULT 0.5, -- 置信度 0-1，表示学习的确信度
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user_profile(user_id),
    UNIQUE(user_id, feature_key)
);

CREATE INDEX idx_features_user_id ON user_behavior_features(user_id);
CREATE INDEX idx_features_confidence ON user_behavior_features(confidence);
```

**数据示例**：

```json
[
  {
    "id": "feat_001",
    "user_id": "user_001",
    "feature_key": "work_time_peak",
    "feature_value": {"start": "09:00", "end": "12:00", "day": "weekday"},
    "confidence": 0.85,
    "last_updated": "2024-01-20T10:00:00"
  },
  {
    "id": "feat_002",
    "user_id": "user_001",
    "feature_key": "decision_style",
    "feature_value": {"style": "data_driven", "speed": "slow"},
    "confidence": 0.72,
    "last_updated": "2024-01-18T15:30:00"
  },
  {
    "id": "feat_003",
    "user_id": "user_001",
    "feature_key": "reminder_frequency_preference",
    "feature_value": {"frequency": "daily", "time": "20:00"},
    "confidence": 0.9,
    "last_updated": "2024-01-22T08:00:00"
  }
]
```

**常见特征键**：
- `work_time_peak`: 工作高峰时间
- `decision_style`: 决策风格（数据驱动、直觉、协商等）
- `motivation_trigger`: 动机触发因素
- `obstacle_pattern`: 常见障碍模式
- `progress_tracking_preference`: 进度跟踪偏好
- `reminder_sensitivity`: 提醒敏感度

---

### 3. events - 生活事件表

**目的**：记录用户通过对话输入的生活事件

**字段定义**：

```sql
CREATE TABLE events (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    category TEXT NOT NULL,      -- 'work', 'learning', 'life', 'health', 'personal'
    date TIMESTAMP NOT NULL,
    importance INTEGER DEFAULT 3, -- 1-5，事件重要程度
    related_plan_ids TEXT,       -- JSON数组：关联的计划ID ["plan_1", "plan_2"]
    tags TEXT,                   -- JSON数组：标签 ["标签1", "标签2"]
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user_profile(user_id),
    CHECK (importance >= 1 AND importance <= 5),
    CHECK (category IN ('work', 'learning', 'life', 'health', 'personal'))
);

CREATE INDEX idx_events_user_id ON events(user_id);
CREATE INDEX idx_events_date ON events(date);
CREATE INDEX idx_events_category ON events(category);
CREATE INDEX idx_events_user_date ON events(user_id, date);
```

**数据示例**：

```json
{
  "id": "event_001",
  "user_id": "user_001",
  "title": "完成项目A的第一阶段",
  "description": "成功完成了项目A的需求分析和架构设计",
  "category": "work",
  "date": "2024-01-20T14:30:00",
  "importance": 5,
  "related_plan_ids": ["plan_001"],
  "tags": ["重要", "项目A", "里程碑"],
  "created_at": "2024-01-20T14:35:00",
  "updated_at": "2024-01-20T14:35:00"
}
```

**分类说明**：
- `work`: 工作相关事件
- `learning`: 学习相关事件
- `life`: 日常生活事件
- `health`: 健康和锻炼事件
- `personal`: 个人成长和思考事件

---

### 4. plans - 计划表

**目的**：存储用户创建的目标和计划

**字段定义**：

```sql
CREATE TABLE plans (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    status TEXT DEFAULT 'active',  -- 'active', 'completed', 'archived'
    priority INTEGER DEFAULT 3,    -- 1-5，优先级
    start_date TIMESTAMP NOT NULL,
    due_date TIMESTAMP NOT NULL,
    progress_percentage INTEGER DEFAULT 0,  -- 0-100
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user_profile(user_id),
    CHECK (priority >= 1 AND priority <= 5),
    CHECK (progress_percentage >= 0 AND progress_percentage <= 100),
    CHECK (status IN ('active', 'completed', 'archived')),
    CHECK (start_date < due_date)
);

CREATE INDEX idx_plans_user_id ON plans(user_id);
CREATE INDEX idx_plans_status ON plans(status);
CREATE INDEX idx_plans_due_date ON plans(due_date);
CREATE INDEX idx_plans_user_status ON plans(user_id, status);
```

**数据示例**：

```json
{
  "id": "plan_001",
  "user_id": "user_001",
  "title": "完成项目X",
  "description": "完成公司新项目X的开发和交付",
  "status": "active",
  "priority": 5,
  "start_date": "2024-01-01T00:00:00",
  "due_date": "2024-03-31T23:59:59",
  "progress_percentage": 35,
  "created_at": "2024-01-01T09:00:00",
  "updated_at": "2024-01-20T16:00:00"
}
```

---

### 5. plan_updates - 计划更新历史表

**目的**：记录计划进度的变化历史，便于追踪进展

**字段定义**：

```sql
CREATE TABLE plan_updates (
    id TEXT PRIMARY KEY,
    plan_id TEXT NOT NULL,
    user_id TEXT NOT NULL,
    progress_percentage INTEGER NOT NULL,
    notes TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (plan_id) REFERENCES plans(id),
    FOREIGN KEY (user_id) REFERENCES user_profile(user_id),
    CHECK (progress_percentage >= 0 AND progress_percentage <= 100)
);

CREATE INDEX idx_plan_updates_plan_id ON plan_updates(plan_id);
CREATE INDEX idx_plan_updates_user_id ON plan_updates(user_id);
CREATE INDEX idx_plan_updates_updated_at ON plan_updates(updated_at);
```

**数据示例**：

```json
{
  "id": "update_001",
  "plan_id": "plan_001",
  "user_id": "user_001",
  "progress_percentage": 35,
  "notes": "完成了前端框架搭建和基础模块开发",
  "updated_at": "2024-01-20T16:00:00"
}
```

---

### 6. reviews - 复盘记录表

**目的**：存储用户的每日复盘内容和AI生成的建议

**字段定义**：

```sql
CREATE TABLE reviews (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    review_date DATE NOT NULL,
    content TEXT NOT NULL,        -- 用户的复盘内容
    ai_suggestions TEXT,          -- AI生成的建议 (JSON)
    related_event_ids TEXT,       -- JSON数组：关联的事件ID
    related_plan_ids TEXT,        -- JSON数组：关联的计划ID
    mood_rating INTEGER DEFAULT 3, -- 1-5，用户当天的心情
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user_profile(user_id),
    UNIQUE(user_id, review_date),
    CHECK (mood_rating >= 1 AND mood_rating <= 5)
);

CREATE INDEX idx_reviews_user_id ON reviews(user_id);
CREATE INDEX idx_reviews_date ON reviews(review_date);
CREATE INDEX idx_reviews_user_date ON reviews(user_id, review_date);
```

**数据示例**：

```json
{
  "id": "review_001",
  "user_id": "user_001",
  "review_date": "2024-01-20",
  "content": "今天进度不错，完成了API设计。但感觉有点疲劳，需要更好地管理时间。",
  "ai_suggestions": {
    "positive": "API设计的完成是重要的里程碑",
    "area_for_improvement": "考虑在下午3点加入15分钟休息",
    "next_day_focus": "继续推进实现工作"
  },
  "related_event_ids": ["event_001"],
  "related_plan_ids": ["plan_001"],
  "mood_rating": 4,
  "created_at": "2024-01-20T21:30:00"
}
```

---

### 7. conversation_history - 对话历史表

**目的**：记录用户和AI的对话，用于学习用户特征和改进系统

**字段定义**：

```sql
CREATE TABLE conversation_history (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    user_message TEXT NOT NULL,
    ai_response TEXT NOT NULL,
    extracted_event_id TEXT,      -- 如果从该对话提取了事件
    conversation_type TEXT,       -- 'life_record', 'plan_discussion', 'review'
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user_profile(user_id),
    FOREIGN KEY (extracted_event_id) REFERENCES events(id)
);

CREATE INDEX idx_conversation_user_id ON conversation_history(user_id);
CREATE INDEX idx_conversation_timestamp ON conversation_history(timestamp);
CREATE INDEX idx_conversation_type ON conversation_history(conversation_type);
```

**数据示例**：

```json
{
  "id": "conv_001",
  "user_id": "user_001",
  "user_message": "今天下午参加了项目会议，完成了API设计文档",
  "ai_response": "很好！API设计文档的完成是项目推进的重要一步。这个事件已经记录。",
  "extracted_event_id": "event_001",
  "conversation_type": "life_record",
  "timestamp": "2024-01-20T14:35:00"
}
```

---

## 数据关系图

### 关系模式

```
user_profile (1:N relationships)
    │
    ├─→ events (通过 user_id)
    │   └─→ related_plan_ids (事件关联计划)
    │
    ├─→ plans (通过 user_id)
    │   └─→ plan_updates (1:N，计划的更新历史)
    │
    ├─→ reviews (通过 user_id)
    │   ├─→ related_event_ids (复盘关联事件)
    │   └─→ related_plan_ids (复盘关联计划)
    │
    ├─→ conversation_history (通过 user_id)
    │   └─→ extracted_event_id (对话提取的事件)
    │
    └─→ user_behavior_features (通过 user_id，用户特征库)
```

### 查询关系示例

```sql
-- 查询用户的所有计划及其最新进度
SELECT
    p.id, p.title, p.status, p.progress_percentage,
    pu.notes, pu.updated_at
FROM plans p
LEFT JOIN plan_updates pu ON p.id = pu.plan_id
WHERE p.user_id = 'user_001' AND p.status = 'active'
ORDER BY pu.updated_at DESC;

-- 查询今天的复盘及其关联的事件
SELECT
    r.id, r.content, r.mood_rating,
    e.title as event_title, e.category
FROM reviews r
LEFT JOIN events e ON r.related_event_ids LIKE '%' || e.id || '%'
WHERE r.user_id = 'user_001' AND r.review_date = DATE('now');
```

---

## 性能优化考虑

### 索引策略

**已创建的索引**：
- 用户ID索引：加速用户相关查询
- 日期范围索引：加速时间范围查询
- 复合索引：加速常见的多条件查询

**潜在的额外索引**（基于实际使用）：
```sql
-- 如果频繁按重要程度查询事件
CREATE INDEX idx_events_importance ON events(importance);

-- 如果频繁查询某个用户某个日期范围的事件
CREATE INDEX idx_events_user_date_range ON events(user_id, date);

-- 如果频繁查询活跃计划
CREATE INDEX idx_plans_active_due ON plans(user_id, status, due_date);
```

### JSON查询优化

**避免频繁的JSON解析**：
```sql
-- 不推荐（每次解析JSON）
SELECT * FROM plans WHERE json_extract(related_plan_ids, '$[0]') = 'plan_001';

-- 推荐（使用专门的关联表）
-- 考虑创建plan_associations表来存储计划间的关系
```

---

## 升级路径

### 从SQLite升级到PostgreSQL

**迁移步骤**：

1. **安装PostgreSQL**
```bash
docker run -d --name postgres -e POSTGRES_DB=mindflow postgres:15
```

2. **修改数据库连接**
```python
# src/config.py
DATABASE_URL = "postgresql://user:password@localhost:5432/mindflow"
```

3. **导出SQLite数据**
```python
# 使用SQLAlchemy的迁移工具
alembic init migrations
alembic revision --autogenerate -m "initial"
alembic upgrade head
```

4. **数据迁移**
```bash
# 使用pgloader等工具迁移数据
pgloader sqlite:///mindflow.db postgresql://user:password@localhost/mindflow
```

5. **验证**
```sql
-- 检查数据完整性
SELECT COUNT(*) FROM events;
SELECT COUNT(*) FROM plans;
-- 等等
```

### 预留多用户支持

数据库设计已为多用户做好准备：

1. 所有核心表都有 `user_id` 字段
2. 所有查询都明确过滤 `user_id`
3. 添加认证后，无需修改数据库模型
4. 只需添加 `users` 表和认证逻辑

---

## 备份和恢复

### SQLite备份
```bash
# 简单备份
cp data/mindflow.db data/mindflow_backup_$(date +%Y%m%d).db

# 使用SQLite内置备份
sqlite3 mindflow.db ".backup mindflow_backup.db"
```

### PostgreSQL备份
```bash
# 完整备份
pg_dump mindflow > mindflow_backup.sql

# 恢复
psql mindflow < mindflow_backup.sql
```

---

## 最佳实践

1. **显式使用事务**：确保数据一致性
2. **适当的错误处理**：捕获数据库异常
3. **参数化查询**：防止SQL注入
4. **定期备份**：特别是生产环境
5. **监控表大小**：评估扩展需求

---

## 数据库初始化脚本

```python
# src/database/init_db.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base

def init_database(database_url: str):
    """初始化数据库"""
    engine = create_engine(database_url)
    Base.metadata.create_all(engine)
    return engine

def get_session(engine):
    """获取数据库会话"""
    Session = sessionmaker(bind=engine)
    return Session()
```

---

## 参考资源

- [SQLAlchemy 官方文档](https://docs.sqlalchemy.org/)
- [SQLite 官方文档](https://www.sqlite.org/docs.html)
- [PostgreSQL 迁移指南](https://www.postgresql.org/docs/)
- [数据库设计最佳实践](https://en.wikipedia.org/wiki/Database_design)
