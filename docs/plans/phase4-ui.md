# Phase 4: UI 和体验 (Week 19-21)

> **时间**: 2026-05-26 ~ 2026-06-15  
> **状态**: ⏳ 待开始

---

## Week 19-20 (5/26 - 6/8): Gradio 界面

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

## Week 21 (6/9 - 6/15): 知识库可视化增强

**开发任务**: `src/ui/visualizer.py`

- [ ] 交互式知识图谱
- [ ] Skill 调用链可视化
- [ ] 实时更新

**🎯 Phase 4 验收标准**:
- ✅ Gradio 界面完整
- ✅ 知识库可视化
- ✅ 用户体验流畅

---

**返回**: [开发计划总览](./README.md)
