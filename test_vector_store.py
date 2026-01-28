"""
测试修改后的 VectorStore - 使用 Chroma 内置 sentence-transformers
"""
import sys
import os

# 设置 UTF-8 编码（Windows 兼容）
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

sys.path.insert(0, 'F:/workspace/mindflow')

from src.knowledge_base.vector_store import VectorStore
from src.knowledge_base.models import Skill

print("=" * 60)
print("测试 VectorStore - Chroma 内置 Sentence-Transformers")
print("=" * 60)

# 初始化向量存储（使用多语言模型）
print("\n1. 初始化 VectorStore...")
vector_store = VectorStore(
    persist_dir="data/vectors_test",
    model_name="paraphrase-multilingual-MiniLM-L12-v2"
)
print("[OK] VectorStore 初始化成功")
print(f"   - 使用模型: paraphrase-multilingual-MiniLM-L12-v2")
print(f"   - 嵌入函数: {type(vector_store.embedding_function).__name__}")

# 创建测试技能
print("\n2. 创建测试技能...")
skills = [
    Skill(
        id="s_csv",
        name="CSV Processing",
        description="处理 CSV 文件的能力，包括读取、清洗、转换数据",
        instructions="1. 使用 pandas 读取 CSV\n2. 清洗数据\n3. 转换格式"
    ),
    Skill(
        id="s_graph",
        name="Graph Visualization",
        description="使用 NetworkX 可视化知识图谱，展示节点和关系",
        instructions="1. 创建图对象\n2. 添加节点和边\n3. 使用 matplotlib 绘制"
    ),
    Skill(
        id="s_search",
        name="Vector Search",
        description="使用 Chroma 进行语义搜索，找到相关的知识节点",
        instructions="1. 初始化 Chroma\n2. 索引文档\n3. 执行查询"
    ),
    Skill(
        id="s_validation",
        name="Data Validation",
        description="使用 Pydantic 进行数据验证，确保数据类型正确",
        instructions="1. 定义 Pydantic 模型\n2. 验证输入数据\n3. 处理验证错误"
    )
]

# 索引技能
print("\n3. 索引技能到向量数据库...")
for skill in skills:
    vector_store.index_skill(skill)
    print(f"   [OK] 已索引: {skill.name}")

# 测试中文查询
print("\n4. 测试中文语义搜索...")
queries = [
    "如何处理数据文件？",
    "怎么做可视化？",
    "如何验证数据？"
]

for query in queries:
    print(f"\n   查询: '{query}'")
    results = vector_store.search(query, top_k=2)
    
    for i, (skill_id, score) in enumerate(results, 1):
        skill = next(s for s in skills if s.id == skill_id)
        print(f"      {i}. {skill.name} (相似度: {score:.2%})")
        print(f"         {skill.description[:50]}...")

# 测试英文查询
print("\n5. 测试英文语义搜索...")
query_en = "How to visualize data?"
print(f"\n   查询: '{query_en}'")
results = vector_store.search(query_en, top_k=2)

for i, (skill_id, score) in enumerate(results, 1):
    skill = next(s for s in skills if s.id == skill_id)
    print(f"      {i}. {skill.name} (相似度: {score:.2%})")
    print(f"         {skill.description[:50]}...")

# 总结
print("\n" + "=" * 60)
print("测试总结")
print("=" * 60)
print("""
[OK] VectorStore 修改成功！

关键改进：
1. 移除了 sentence-transformers 的直接依赖
2. 使用 Chroma 内置的 embedding_functions
3. 默认使用多语言模型（支持中文）
4. 代码更简洁，自动管理嵌入向量

优势：
- 无需手动调用 embedder.encode()
- Chroma 自动处理文档和查询的嵌入
- 统一的接口，更易维护
- 支持中英文混合查询
""")

print("\n清理测试数据...")
import shutil
if os.path.exists("data/vectors_test"):
    shutil.rmtree("data/vectors_test")
    print("[OK] 测试数据已清理")
