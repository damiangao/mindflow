# 开源知识图谱工具调研

> **调研日期**: 2026-01-26  
> **调研人**: MindFlow Team  
> **目标**: 学习开源知识图谱工具的设计，为 MindFlow 提供参考

---

## 📋 调研清单

| 项目 | 语言 | Stars | 开源 | 特点 | 调研状态 |
|------|------|-------|------|------|---------|
| **Logseq** | Clojure | 30k+ | ✅ | 大纲式、图谱、本地优先 | ⏳ 进行中 |
| **Foam** | TypeScript | 15k+ | ✅ | VSCode 插件、轻量级 | ⏳ 待开始 |
| **Dendron** | TypeScript | 6k+ | ✅ | 层级式笔记、发布系统 | ⏳ 待开始 |
| **Athens Research** | Clojure | 6k+ | ✅ | 类 Roam Research | ⏳ 待开始 |
| **TiddlyWiki** | JavaScript | 8k+ | ✅ | 单文件 Wiki、插件丰富 | ⏳ 待开始 |

---

## 🔍 Logseq 深度调研

### 基本信息

- **GitHub**: https://github.com/logseq/logseq
- **官网**: https://logseq.com/
- **许可**: AGPL-3.0
- **技术栈**: Clojure + ClojureScript + DataScript
- **Stars**: 30k+

### 核心架构

#### 1. 数据存储

```clojure
;; DataScript 图数据库
(def schema
  {:block/uuid {:db/unique :db.unique/identity}
   :block/parent {:db/valueType :db.type/ref}
   :block/page {:db/valueType :db.type/ref}
   :block/refs {:db/valueType :db.type/ref
                :db/cardinality :db.cardinality/many}})
```

**启发**:
- 使用内存图数据库 (DataScript) 提升查询性能
- MindFlow 可考虑 NetworkX (开发) + Neo4j (生产)

#### 2. 双向链接实现

```clojure
;; 链接解析
(defn parse-page-refs [content]
  "解析 [[页面名称]] 格式的链接"
  (re-seq #"\[\[([^\]]+)\]\]" content))

;; 反向链接查询
(defn get-backlinks [page-id db]
  (d/q '[:find ?block
         :in $ ?page
         :where
         [?block :block/refs ?page]]
       db page-id))
```

**启发**:
- 正则表达式解析 `[[链接]]` 语法
- 图数据库天然支持反向查询
- MindFlow 需要在 Artifact 中维护 `referenced_by` 字段

#### 3. 图谱可视化

**技术栈**: D3.js + Force-directed graph

```javascript
// 简化的图谱渲染逻辑
const simulation = d3.forceSimulation(nodes)
  .force("link", d3.forceLink(links).id(d => d.id))
  .force("charge", d3.forceManyBody().strength(-300))
  .force("center", d3.forceCenter(width / 2, height / 2));
```

**启发**:
- D3.js 是 Web 端图谱可视化的标准
- Python 生态可使用 pyvis (基于 vis.js)
- 需要支持导出为独立 HTML 文件

#### 4. 插件系统

```javascript
// Logseq 插件 API
logseq.Editor.registerSlashCommand('My Command', async () => {
  await logseq.Editor.insertAtEditingCursor('Hello World');
});
```

**启发**:
- 提供清晰的插件 API
- MindFlow 可设计 Python 插件接口
- 支持生命周期钩子 (on_skill_execute, on_artifact_created)

---

### 可复用的设计模式

#### 1. **Block-based 数据模型**

Logseq 的核心是 Block（块），所有内容都是 Block：

```
Page (Block)
├── Block 1
│   ├── Block 1.1
│   └── Block 1.2
└── Block 2
```

**对 MindFlow 的启发**:
- 统一的节点抽象 (Methodology, Skill, Artifact 都是 Node)
- 层级关系通过图边表示

#### 2. **查询语言**

Logseq 使用 Datalog 查询：

```clojure
[:find ?block
 :where
 [?block :block/content ?content]
 [(clojure.string/includes? ?content "TODO")]]
```

**对 MindFlow 的启发**:
- 提供类似的查询 DSL
- 例如: `kb.query("Skills that produce [[CSV File]]")`

#### 3. **本地优先 + 同步**

- 数据存储在本地 Markdown 文件
- 可选云同步服务
- 支持 Git 版本控制

**对 MindFlow 的启发**:
- 保持 JSON + 文件的本地存储
- 未来可添加 Git 集成

---

### 性能优化

#### 1. **增量索引**

```clojure
(defn index-block [db block]
  "只索引变更的 Block"
  (when (block-changed? block)
    (update-index! db block)))
```

**对 MindFlow 的启发**:
- 向量索引支持增量更新
- 避免每次都重建整个索引

#### 2. **懒加载**

- 只加载当前页面的 Block
- 图谱视图按需加载节点

**对 MindFlow 的启发**:
- 大规模知识库时，按需加载 Skills
- 图谱可视化支持局部渲染

---

### 调研总结

| 维度 | Logseq 方案 | MindFlow 借鉴 |
|------|------------|--------------|
| **数据库** | DataScript (内存) | NetworkX → Neo4j |
| **链接语法** | `[[页面]]` | `[[节点名称]]` |
| **图谱渲染** | D3.js | pyvis / networkx |
| **插件系统** | JavaScript API | Python 钩子 |
| **存储格式** | Markdown | JSON + 文件 |

**下一步行动**:
- [ ] 实现 `[[链接]]` 解析器
- [ ] 选择 Python 图谱可视化库
- [ ] 设计插件接口规范

---

## 🔍 Foam 调研

> **状态**: ⏳ 待开始  
> **预计时间**: Week 2 Day 3-4

### 调研重点

1. VSCode 插件架构
2. Markdown 链接解析
3. Graph View 实现
4. 与 Obsidian 的兼容性

---

## 🔍 Dendron 调研

> **状态**: ⏳ 待开始  
> **预计时间**: Week 2 Day 5

### 调研重点

1. 层级式笔记组织
2. 发布系统设计
3. 多 Vault 管理

---

## 🔍 Athens Research 调研

> **状态**: ⏳ 待开始  
> **预计时间**: Week 2 (可选)

### 调研重点

1. Roam Research 的开源实现
2. 双向链接的高级用法
3. 查询语言设计

---

## 📊 对比总结

### 技术栈对比

| 项目 | 前端 | 后端 | 数据库 | 可视化 |
|------|------|------|--------|--------|
| Logseq | ClojureScript | Clojure | DataScript | D3.js |
| Foam | TypeScript | - | VSCode API | - |
| Dendron | TypeScript | Node.js | 文件系统 | - |
| Athens | ClojureScript | Clojure | DataScript | D3.js |
| **MindFlow** | Python | Python | NetworkX/Neo4j | pyvis |

### 设计理念对比

| 维度 | Logseq | Foam | Dendron | MindFlow |
|------|--------|------|---------|----------|
| **数据模型** | Block-based | Page-based | Hierarchy | Graph-based |
| **本地优先** | ✅ | ✅ | ✅ | ✅ |
| **开源** | ✅ | ✅ | ✅ | ✅ |
| **目标用户** | 个人知识管理 | 开发者 | 团队协作 | AI Agent |

---

## 💡 关键启发

### 1. **图谱可视化是核心功能**

所有成功的知识图谱工具都提供了图谱可视化：
- Logseq: 交互式图谱
- Foam: 静态图谱
- Dendron: 层级树状图

**MindFlow 必须实现**: Week 2 优先级提升

### 2. **双向链接是标准语法**

`[[链接]]` 语法已成为事实标准：
- 简单直观
- 易于解析
- 支持自动补全

**MindFlow 必须支持**: Week 2 实现

### 3. **本地优先 + 开放格式**

用户最关心的是数据所有权：
- 本地存储
- 开放格式 (Markdown, JSON)
- 支持导出

**MindFlow 已满足**: 继续保持

### 4. **插件生态是长期竞争力**

- Logseq: 数百个社区插件
- VSCode: 强大的插件生态

**MindFlow 未来方向**: Phase 3-4 考虑插件系统

---

## 📝 调研产出

### 代码示例

#### 1. 链接解析器 (参考 Logseq)

```python
# src/knowledge_base/link_parser.py
import re
from typing import List, Dict, Optional

class LinkParser:
    """解析 [[链接]] 语法"""
    
    LINK_PATTERN = r'\[\[([^\]]+)\]\]'
    
    @staticmethod
    def parse_links(content: str) -> List[str]:
        """提取所有 [[name]] 链接"""
        return re.findall(LinkParser.LINK_PATTERN, content)
    
    @staticmethod
    def resolve_links(links: List[str], kb: 'KnowledgeBase') -> Dict[str, Optional['Node']]:
        """解析链接到实际节点"""
        result = {}
        for link in links:
            node = kb.get_node_by_name(link)
            result[link] = node
        return result
    
    @staticmethod
    def replace_links_with_html(content: str, kb: 'KnowledgeBase') -> str:
        """将 [[链接]] 替换为 HTML 链接"""
        def replace(match):
            name = match.group(1)
            node = kb.get_node_by_name(name)
            if node:
                return f'<a href="#{node.id}">{name}</a>'
            else:
                return f'<span class="broken-link">{name}</span>'
        
        return re.sub(LinkParser.LINK_PATTERN, replace, content)
```

#### 2. 图谱可视化 (参考 Logseq)

```python
# src/ui/graph_visualizer.py
from pyvis.network import Network
from typing import Optional

class GraphVisualizer:
    """知识图谱可视化"""
    
    def __init__(self, kb: 'KnowledgeBase'):
        self.kb = kb
    
    def render_graph(self, focus_node: Optional[str] = None, depth: int = 2) -> Network:
        """
        渲染知识图谱
        
        Args:
            focus_node: 聚焦节点 ID
            depth: 显示深度
        
        Returns:
            pyvis Network 对象
        """
        net = Network(height="750px", width="100%", bgcolor="#222222", font_color="white")
        
        # 配置物理引擎 (类似 D3.js force-directed)
        net.barnes_hut(
            gravity=-80000,
            central_gravity=0.3,
            spring_length=250,
            spring_strength=0.001,
            damping=0.09
        )
        
        # 添加节点
        for node in self.kb.get_all_nodes():
            color = self._get_node_color(node)
            size = self._get_node_size(node)
            net.add_node(
                node.id,
                label=node.name,
                color=color,
                size=size,
                title=node.description  # 悬停提示
            )
        
        # 添加边
        for edge in self.kb.get_all_edges():
            net.add_edge(
                edge.source,
                edge.target,
                label=edge.relation,
                color=self._get_edge_color(edge.relation)
            )
        
        return net
    
    def _get_node_color(self, node) -> str:
        """节点颜色"""
        colors = {
            'Methodology': '#A88BFA',  # 紫色
            'Skill': '#3B82F6',        # 蓝色
            'Artifact': '#22C55E'      # 绿色
        }
        return colors.get(node.type, '#6B7280')
    
    def _get_node_size(self, node) -> int:
        """节点大小 (根据使用频率)"""
        base_size = 20
        usage_factor = getattr(node, 'usage_count', 0) * 2
        return min(base_size + usage_factor, 50)
    
    def _get_edge_color(self, relation: str) -> str:
        """边颜色"""
        colors = {
            'guides': '#9CA3AF',      # 灰色虚线
            'produces': '#10B981',    # 绿色实线
            'depends_on': '#F59E0B'   # 橙色箭头
        }
        return colors.get(relation, '#6B7280')
    
    def export_to_html(self, output_path: str, focus_node: Optional[str] = None):
        """导出为独立 HTML 文件"""
        net = self.render_graph(focus_node)
        net.save_graph(output_path)
        print(f"图谱已导出到: {output_path}")
```

---

## 🎯 下一步行动

### Week 2 任务

- [ ] **Day 1-2**: 完成 Logseq 核心代码阅读
- [ ] **Day 3-4**: 调研 Foam 和 Dendron
- [ ] **Day 5**: 实现链接解析器原型
- [ ] **Day 6-7**: 实现图谱可视化原型

### 产出物

- [x] 本调研文档
- [ ] 链接解析器代码
- [ ] 图谱可视化代码
- [ ] 技术选型报告

---

**最后更新**: 2026-01-26  
**维护者**: MindFlow Team
