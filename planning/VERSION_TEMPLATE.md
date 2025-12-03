# 版本创建模板

本文件是创建新版本时的参考模板。当需要创建新版本（如v1.0.1）时，按以下步骤操作。

## 📋 创建新版本的完整流程

### Step 1: 准备工作
```bash
# 创建版本文件夹
mkdir -p planning/v1.0.1

# 复制最新的PLAN.md
cp PLAN.md planning/v1.0.1/PLAN.md

# 创建时间戳
date > planning/v1.0.1/TIMESTAMP.txt
```

### Step 2: 复制模板文件（下面的内容）
使用以下模板创建：
- `SUMMARY.md` - 版本总结
- `CHANGES.md` - 相比上一版本的变更

### Step 3: 填写内容
根据你的实际完成情况填写各个文件

### Step 4: 更新索引
```bash
# 更新 planning/VERSIONS.md
# 添加新版本的信息

# 创建git tag
git tag -a v1.0.1 -m "Phase 1 completed: Framework setup verified"
```

---

## 📄 SUMMARY.md 模板

```markdown
# Mindflow vX.X 版本总结

**版本号**: vX.X
**发布日期**: YYYY-MM-DD
**阶段**: [描述这个版本的阶段]

---

## 📌 版本目标

[描述这个版本的主要目标，3-5个要点]

例如：
- 完成Phase 1的框架搭建
- 验证LLM配置层的可行性
- 建立基础的Gradio应用

## ✅ 完成情况

### 功能完成
- ✅ [功能1]: 简要描述
- ✅ [功能2]: 简要描述
- ✅ [功能3]: 简要描述

### 技术验证
- ✅ [技术1]: 验证结果摘要
- ✅ [技术2]: 验证结果摘要

### 性能指标
- ✅ [指标1]: 数值
- ✅ [指标2]: 数值

## 📊 统计数据

| 指标 | 数值 |
|------|------|
| 新增代码行数 | xxx |
| 完成的任务项 | xx/xx |
| 修复的问题 | xx |
| 性能提升 | xx% |

## 🔄 关键工作

[描述这个版本中最重要的工作和决策]

## ⚠️ 遇到的问题

[记录开发过程中遇到的主要问题和解决方案]

例如：
1. **问题**: LLM调用超时
   **解决**: 添加了超时控制和重试机制

2. **问题**: 数据库连接池不稳定
   **解决**: 升级到最新版本的SQLAlchemy

## 💡 经验教训

[记录这个版本中学到的内容]

例如：
- Gradio的特性和限制
- LangGraph的最佳实践
- 数据库性能优化方法

## 🚀 下一步计划

[描述后续的工作计划]

- [ ] Phase 2: 生活记录系统
- [ ] 优化Phase 1的性能
- [ ] 增加单元测试覆盖

## 📈 版本对比

相比v1.0的主要改进：

| 指标 | v1.0 | vX.X | 变化 |
|------|------|------|------|
| 代码行数 | 100 | 500 | +400 |
| 功能数 | 2 | 5 | +3 |
| 性能 | 基准 | 1.5x | +50% |

## 🎯 质量评估

- 代码质量: ⭐⭐⭐⭐⭐ (5/5)
- 文档完整度: ⭐⭐⭐⭐☆ (4/5)
- 测试覆盖: ⭐⭐⭐☆☆ (3/5)
- 生产就绪: ⭐⭐⭐⭐☆ (4/5)

## 📝 待办项

- [ ] [任务1] - 预计何时完成
- [ ] [任务2] - 预计何时完成
- [ ] [已知问题1] - 修复方案

## 📚 相关文件

- `PLAN.md` - 该版本的完整规划
- `CHANGES.md` - 详细的变更说明
- `TIMESTAMP.txt` - 版本创建时间

---

**版本创建日期**: YYYY-MM-DD
**预计下一个版本**: vX.X ([描述])
```

---

## 📄 CHANGES.md 模板

```markdown
# vX.X 变更说明

本文件记录相比vX.X-1的所有变更。

---

## 📝 变更摘要

[用一句话总结主要变更]

例如：
"Phase 1完成，Gradio框架和LLM配置层实现完成"

---

## 🆕 新增

### 功能
- [ ] [功能名称]: [简要描述]
  - 实现细节
  - 相关文件

- [ ] [功能名称]: [简要描述]

### 文件
- [ ] `src/llm/provider.py` - LLM提供商抽象层
- [ ] `src/llm/claude.py` - Claude API实现
- [ ] `src/llm/config.py` - LLM配置管理

### 文档
- [ ] `docs/LLM_CONFIG.md` - LLM配置指南
- [ ] `docs/ARCHITECTURE.md` - 系统架构说明

### 依赖
- [ ] `langchain>=0.1.0`
- [ ] `gradio>=4.0.0`

---

## ✏️ 修改

### 功能改进
- [ ] [原有功能]: 从 [旧行为] 改为 [新行为]
  - 原因: [为什么要改]
  - 影响: [会影响哪些部分]

- [ ] [原有功能]: 优化了 [方面]
  - 性能提升: [数值]
  - 代码行数: [变化]

### 代码优化
- [ ] `src/database/models.py`: 重构ORM模型
  - 从 [旧设计] 改为 [新设计]
  - 性能改进 xx%

### 文档更新
- [ ] `PLAN.md`: 更新了 [章节]
- [ ] `README.md`: 添加了 [内容]

### 配置变更
- [ ] `.env.example`: 添加了新的环境变量
  ```
  LLM_PROVIDER=claude
  CLAUDE_API_KEY=your_key
  ```

---

## 🗑️ 删除

- [ ] [已删除项]: 原因说明
  - 替代方案: [如果有的话]

- [ ] `src/llm/deprecated_provider.py` - 已被新的provider.py替代

---

## 📊 数据库变更

### 新表
```sql
CREATE TABLE [新表名] (
  ...
);
```

### 新字段
```sql
ALTER TABLE events ADD COLUMN category TEXT;
```

### 数据迁移
```sql
-- 迁移脚本
UPDATE events SET category = 'work' WHERE ...;
```

### 性能变更
- 添加索引在 `user_id, date` 上
- 性能提升: 查询时间从 xx ms 降到 xx ms

---

## 🧪 测试

### 单元测试
- [ ] `test_llm_provider.py` - 提供商测试
- [ ] `test_gradio_ui.py` - UI测试
- [ ] 覆盖率: 80%

### 集成测试
- [ ] 完整的事件提取流程
- [ ] LLM配置切换测试
- [ ] 数据库连接和查询

### 性能测试
- [ ] 并发请求: 10个/秒
- [ ] 数据库查询: <100ms
- [ ] API响应时间: <500ms

---

## 🔀 兼容性

### 向后兼容
- ✅ 兼容v1.0的所有功能
- ✅ 数据库schema可自动迁移
- ✅ API接口保持不变

### 破坏性变更
- ❌ [如果有的话列出]
  - 迁移步骤: [如何升级]

---

## 📈 性能变化

| 指标 | v1.0 | vX.X | 变化 |
|------|------|------|------|
| [指标1] | [值] | [值] | [变化] |
| [指标2] | [值] | [值] | [变化] |

---

## ⚠️ 已知问题

- [ ] [问题1]: [描述]
  - 状态: [待修复/已识别]
  - 影响: [低/中/高]
  - 预计修复时间: vX.X

- [ ] [问题2]: [描述]

---

## 🔗 相关PR/Issue

- #123 - [PR标题]
- #456 - [Issue标题]

---

## 📋 升级指南

### 对于用户
1. 备份现有数据
2. 运行迁移脚本（如果有）
3. 更新环境变量
4. 重启应用

### 对于开发者
1. 拉取最新代码
2. 安装新的依赖: `pip install -r requirements.txt`
3. 运行数据库迁移: `python src/database/init_db.py`
4. 运行测试: `pytest`

---

## 🙏 贡献者

- [@developer1] - 功能A实现
- [@developer2] - 功能B实现

---

**版本号**: vX.X
**发布日期**: YYYY-MM-DD
**相比上一版本**: vX.X-1
```

---

## 📋 检查清单

在创建新版本前，请检查以下项目：

### 文件准备
- [ ] PLAN.md 已更新
- [ ] 新建版本文件夹：`planning/vX.X/`
- [ ] 复制 PLAN.md：`planning/vX.X/PLAN.md`
- [ ] 创建 SUMMARY.md：参考上面的模板
- [ ] 创建 CHANGES.md：参考上面的模板
- [ ] 创建 TIMESTAMP.txt：`date > planning/vX.X/TIMESTAMP.txt`

### 文档更新
- [ ] 更新 `planning/VERSIONS.md` 添加新版本信息
- [ ] 更新 `planning/README.md` 的"当前版本"部分
- [ ] 如有需要，更新 docs/ 中的相关文档

### Git操作
- [ ] 提交所有更改：`git add planning/`
- [ ] 创建提交：`git commit -m "Release vX.X: [描述]"`
- [ ] 创建标签：`git tag -a vX.X -m "[描述]"`
- [ ] 推送到远程：`git push origin --tags`

### 通知
- [ ] 通知团队成员新版本发布
- [ ] 更新项目状态页面
- [ ] 发送版本说明邮件

---

## 💡 提示

### SUMMARY.md 的目的
- 快速了解版本的内容
- 对比不同版本
- 追踪项目进度

### CHANGES.md 的目的
- 详细记录每个变更
- 便于代码审查
- 作为升级指南

### 何时更新版本
- Phase 完成时
- 有重大功能更新时
- 修复关键bug后
- 性能有显著提升时

### 版本号的含义
- 主版本号变化（如v1→v2）：大型功能或架构变化
- 次版本号变化（如v1.0→v1.1）：新功能或显著改进
- 修订版本号变化（如v1.0→v1.0.1）：bug修复

---

## 相关命令速查

```bash
# 创建新版本文件夹
mkdir -p planning/v1.0.1

# 复制PLAN
cp PLAN.md planning/v1.0.1/PLAN.md

# 创建时间戳
date > planning/v1.0.1/TIMESTAMP.txt

# 查看所有版本
ls -la planning/v*/

# 对比两个版本
diff planning/v1.0/PLAN.md planning/v1.0.1/PLAN.md

# 创建git tag
git tag -a v1.0.1 -m "Phase 1 completed"

# 查看所有tags
git tag -l

# 推送tags到远程
git push origin --tags
```

---

**最后更新**: 2024-12-03
