# Mindflow LLM 配置指南

## 概述

Mindflow设计了灵活的LLM配置系统，支持在多个LLM提供商之间快速切换，而无需修改业务逻辑代码。这种设计遵循策略模式，使得LLM的选择完全由环境配置驱动。

## 核心设计理念

### 为什么需要灵活的LLM配置？

1. **成本优化**：选择成本最低的合适模型
2. **隐私保护**：在国家政策限制下快速切换到允许的提供商
3. **功能对比**：不同任务可能需要不同模型
4. **故障转移**：主要提供商不可用时快速切换备选方案
5. **无缝迁移**：未来模型更新时不影响业务逻辑

## 支持的 LLM 提供商

### 1. Claude (推荐 - 默认)

**优势**：
- Claude Haiku 4.5 成本低，性能好
- 长上下文支持（200K tokens）
- 多轮对话质量高
- 指令遵循能力强

**配置**：
```bash
export LLM_PROVIDER=claude
export CLAUDE_API_KEY=your_api_key_here
export CLAUDE_MODEL=claude-3-5-haiku-20241022  # 默认值
```

**使用场景**：
- 生活事件提取和分类
- 用户画像学习
- 计划推动和复盘提示
- 整体MVP开发

**成本参考**（近似）：
- Haiku 4.5: 最经济，适合高频调用
- Sonnet 4.5: 中等成本，更强大
- Opus 4.5: 最强大，最贵

### 2. OpenAI (GPT 系列)

**优势**：
- 成熟稳定
- 多模态支持（GPT-4o可处理图片）
- 大量示例和文档
- 企业级可靠性

**配置**：
```bash
export LLM_PROVIDER=openai
export OPENAI_API_KEY=your_api_key_here
export OPENAI_MODEL=gpt-4o-mini  # 推荐成本/性能比较好
# 或 gpt-4o, gpt-3.5-turbo
```

**使用场景**：
- 多模态输入（知识库后续功能）
- 需要特定GPT能力的任务
- 有现有OpenAI配额的用户

**成本参考**（近似）：
- GPT-3.5 Turbo: 最便宜
- GPT-4o Mini: 性价比高
- GPT-4o: 更强大，较贵
- GPT-4 Turbo: 最贵

### 3. DeepSeek (国内友好)

**优势**：
- 支持国内用户
- 成本相对低
- 支持长上下文
- 中文能力强

**配置**：
```bash
export LLM_PROVIDER=deepseek
export DEEPSEEK_API_KEY=your_api_key_here
export DEEPSEEK_MODEL=deepseek-chat  # 默认值
```

**使用场景**：
- 国内用户（无需VPN）
- 中文处理为主
- 预算限制的用户

### 4. Ollama (本地 - 隐私优先)

**优势**：
- 完全本地运行
- 无隐私顾虑
- 无API成本
- 可离线使用

**配置**：
```bash
export LLM_PROVIDER=ollama
export OLLAMA_BASE_URL=http://localhost:11434
export OLLAMA_MODEL=llama2  # 或其他本地模型
# 常见本地模型: llama2, mistral, neural-chat, orca-mini
```

**使用场景**：
- 隐私敏感的用户
- 无网络环境
- 低成本部署
- 测试和开发

**安装本地模型**：
```bash
# 首先安装Ollama: https://ollama.ai
# 然后拉取模型
ollama pull llama2        # 通用模型
ollama pull mistral      # 性能更好，显存要求高
ollama pull neural-chat  # 对话优化
ollama pull orca-mini    # 轻量级
```

**硬件要求**：
- 最小：4GB RAM + 8GB存储（orca-mini）
- 推荐：16GB RAM + 30GB存储（llama2, mistral）
- 最佳：GPU支持（NVIDIA CUDA或AMD ROCm）

## 环境变量配置

### 完整配置示例

创建 `.env` 文件（参考 `.env.example`）：

```bash
# ============================================
# LLM 配置
# ============================================

# 选择LLM提供商: claude, openai, deepseek, ollama
LLM_PROVIDER=claude

# Claude API配置
CLAUDE_API_KEY=sk-ant-xxx
CLAUDE_MODEL=claude-3-5-haiku-20241022

# OpenAI API配置
OPENAI_API_KEY=sk-xxx
OPENAI_MODEL=gpt-4o-mini

# DeepSeek API配置
DEEPSEEK_API_KEY=sk-xxx
DEEPSEEK_MODEL=deepseek-chat

# Ollama本地配置
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama2

# ============================================
# 其他配置
# ============================================
DATABASE_URL=sqlite:///./data/mindflow.db
LOG_LEVEL=INFO
```

### 在Python中加载环境变量

```python
from dotenv import load_dotenv
import os

load_dotenv()

llm_provider = os.getenv('LLM_PROVIDER', 'claude')
api_key = os.getenv(f'{llm_provider.upper()}_API_KEY')
model = os.getenv(f'{llm_provider.upper()}_MODEL')
```

## LLM 提供商实现

### 架构设计

```
src/llm/
├── provider.py      # 抽象基类 BaseLLMProvider
├── claude.py        # Claude实现
├── openai.py        # OpenAI实现
├── deepseek.py      # DeepSeek实现
├── ollama.py        # Ollama本地实现
└── config.py        # LLM配置管理
```

### 基础类定义

```python
# src/llm/provider.py
from abc import ABC, abstractmethod
from typing import Optional

class BaseLLMProvider(ABC):
    """LLM提供商的抽象基类"""

    @abstractmethod
    def complete(
        self,
        prompt: str,
        max_tokens: Optional[int] = None,
        temperature: float = 0.7,
        **kwargs
    ) -> str:
        """生成文本补全"""
        pass

    @abstractmethod
    def chat_complete(
        self,
        messages: list,
        max_tokens: Optional[int] = None,
        temperature: float = 0.7,
        **kwargs
    ) -> str:
        """聊天补全（多轮对话）"""
        pass
```

### 使用示例

```python
# src/llm/config.py
from .provider import BaseLLMProvider
from .claude import ClaudeProvider
from .openai import OpenAIProvider
from .deepseek import DeepSeekProvider
from .ollama import OllamaProvider

def get_llm_provider() -> BaseLLMProvider:
    """根据环境变量获取LLM提供商实例"""
    provider_name = os.getenv('LLM_PROVIDER', 'claude').lower()

    if provider_name == 'claude':
        return ClaudeProvider()
    elif provider_name == 'openai':
        return OpenAIProvider()
    elif provider_name == 'deepseek':
        return DeepSeekProvider()
    elif provider_name == 'ollama':
        return OllamaProvider()
    else:
        raise ValueError(f"Unsupported LLM provider: {provider_name}")

# 在业务逻辑中使用
llm = get_llm_provider()
response = llm.chat_complete([
    {"role": "user", "content": "你好"}
])
```

## 成本估算

### 按使用场景计算

假设系统月度使用场景：

| 场景 | 调用次数 | 平均tokens | 总tokens | Claude成本 | GPT成本 | DeepSeek成本 |
|------|---------|-----------|---------|----------|---------|------------|
| 事件提取 | 150次 | 800 | 120K | $0.36 | $0.30 | $0.20 |
| 用户画像 | 30次 | 2000 | 60K | $0.18 | $0.15 | $0.10 |
| 计划推动 | 30次 | 1500 | 45K | $0.14 | $0.11 | $0.07 |
| 复盘生成 | 30次 | 2500 | 75K | $0.23 | $0.19 | $0.12 |
| **总计** | **240次** | **1700** | **300K** | **$0.91** | **$0.75** | **$0.49** |

*注：成本仅供参考，实际成本取决于具体调用量和模型参数*

## 切换 LLM 的步骤

### 快速切换

1. **修改.env文件**
```bash
# 从Claude切换到OpenAI
export LLM_PROVIDER=openai
export OPENAI_API_KEY=your_key
export OPENAI_MODEL=gpt-4o-mini
```

2. **重启应用**
```bash
# 如果使用Docker
docker-compose restart

# 如果直接运行Python
# 重新启动Python应用即可
```

3. **验证切换成功**
- 查看日志输出中的LLM提供商
- 尝试调用LLM功能，验证响应正常

### 在运行时切换（高级）

对于需要根据情况动态选择提供商的场景：

```python
# 示例：基于任务类型选择不同LLM
def get_task_specific_llm(task_type: str) -> BaseLLMProvider:
    if task_type == 'event_extraction':
        return get_llm_provider()  # 使用默认
    elif task_type == 'image_processing':
        return OpenAIProvider()  # 需要多模态
    elif task_type == 'privacy_critical':
        return OllamaProvider()  # 隐私优先
```

## API 密钥管理

### 安全建议

1. **不要提交API密钥到Git**
   - 使用 `.env` 文件（已在 `.gitignore` 中）
   - 参考 `.env.example` 作为模板

2. **使用强大的密钥**
   - 定期轮换API密钥
   - 为不同环境使用不同密钥

3. **权限限制**
   - 如果支持，限制API密钥的权限范围
   - 限制IP白名单

4. **监控使用**
   - 定期检查API使用成本
   - 设置成本告警

### 本地开发

```bash
# 创建 .env.local（仅本地使用）
cp .env.example .env.local
# 编辑.env.local，添加你的API密钥
# 在.gitignore中确保 .env.local 被忽略
```

## 性能和延迟考虑

### 响应时间

| 模型 | 平均延迟 | 峰值延迟 | 成本 | 注释 |
|------|---------|---------|------|------|
| Claude Haiku 4.5 | 500ms | 1s | 最低 | 推荐 |
| GPT-4o Mini | 600ms | 1.5s | 低 | 稳定 |
| DeepSeek | 800ms | 2s | 最低 | 国内快 |
| Ollama (本地) | 1-3s | 5-10s | 免费 | 硬件依赖 |

### 优化建议

1. **缓存**：对相同的输入缓存LLM响应
2. **异步调用**：对非关键路径使用异步LLM调用
3. **批量处理**：合并多个请求到一个API调用
4. **降级方案**：提供备选响应当LLM不可用时

## 故障排除

### 常见问题

**问题：LLM API超时**
```
解决方案：
1. 检查网络连接
2. 增加超时限制
3. 切换到另一个提供商
```

**问题：API密钥无效**
```
解决方案：
1. 验证密钥是否正确复制
2. 检查密钥是否过期
3. 确认有足够的配额
```

**问题：响应质量差**
```
解决方案：
1. 尝试不同的提示词
2. 增加temperature参数
3. 使用更强大的模型
4. 检查输入数据质量
```

**问题：成本过高**
```
解决方案：
1. 减少API调用频率
2. 使用成本更低的模型
3. 切换到Ollama本地模型
4. 实现缓存机制
```

## 最佳实践

### 1. 为不同任务选择合适的模型

```python
# 简单任务用轻量级模型
# 复杂推理用强大模型
# 隐私任务用本地模型
```

### 2. 实现重试和降级逻辑

```python
def call_llm_with_fallback(prompt, primary='claude', fallback='ollama'):
    try:
        provider = get_provider(primary)
        return provider.complete(prompt)
    except Exception as e:
        logger.warning(f"Primary LLM failed: {e}, using fallback")
        provider = get_provider(fallback)
        return provider.complete(prompt)
```

### 3. 监控和日志

```python
import logging

logger = logging.getLogger(__name__)
logger.info(f"Using LLM provider: {llm_provider}")
logger.debug(f"LLM request tokens: {input_tokens}")
logger.debug(f"LLM response tokens: {output_tokens}")
```

### 4. 定期审查和优化

- 每月分析LLM使用成本和性能
- 根据需要调整模型选择
- 测试新发布的模型
- 收集用户反馈

## 参考资源

### API文档
- [Claude API文档](https://docs.anthropic.com)
- [OpenAI API文档](https://platform.openai.com/docs)
- [DeepSeek API文档](https://deepseek.com/docs)
- [Ollama文档](https://ollama.ai/docs)

### 获取API密钥
- Claude: https://console.anthropic.com
- OpenAI: https://platform.openai.com/account/api-keys
- DeepSeek: https://platform.deepseek.com
- Ollama: 本地无需密钥

## 常见命令

```bash
# 测试Claude连接
python -c "from src.llm.config import get_llm_provider; llm = get_llm_provider(); print(llm.complete('Hello'))"

# 切换到OpenAI
export LLM_PROVIDER=openai
export OPENAI_API_KEY=your_key

# 切换到本地Ollama
export LLM_PROVIDER=ollama
# 确保Ollama服务运行: ollama serve

# 查看当前配置
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print(os.getenv('LLM_PROVIDER'))"
```
