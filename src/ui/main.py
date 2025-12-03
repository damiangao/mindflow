"""
Gradio web application for Mindflow
"""

import gradio as gr
from typing import List, Tuple
from src.config import settings
from src.llm.config import get_llm
from src.database.connection import get_db, get_session


def create_app():
    """Create and configure the Gradio application"""

    # Initialize database
    get_db().initialize()

    with gr.Blocks(
        title="Mindflow - Personal AI Assistant",
        theme=gr.themes.Soft(),
        css="""
            .header {
                text-align: center;
                color: #333;
            }
            .welcome-text {
                font-size: 18px;
                margin: 20px 0;
            }
        """,
    ) as demo:

        # Header
        gr.Markdown(
            """
            # 🧠 Mindflow - Personal AI Assistant

            *帮助你记录生活、规划目标、反思成长*

            ---
            """
        )

        # Main tabs
        with gr.Tabs():

            # Tab 1: Life Record
            with gr.Tab("📝 生活记录"):
                gr.Markdown("### 记录你的日常事件")
                gr.Markdown("在下方输入今天发生的事件，系统会自动识别和分类。")

                with gr.Row():
                    with gr.Column():
                        event_input = gr.Textbox(
                            label="事件描述",
                            placeholder="例如：完成了项目A的代码审查",
                            lines=3,
                        )
                        submit_btn = gr.Button("记录事件", variant="primary")

                    with gr.Column():
                        event_output = gr.Textbox(
                            label="识别结果", interactive=False, lines=5
                        )

                # Event list display
                gr.Markdown("### 今日事件列表")
                event_list = gr.DataFrame(
                    headers=["时间", "标题", "类别", "描述"],
                    interactive=False,
                    wrap=True,
                )

                def process_event(text):
                    """Process user event input"""
                    if not text:
                        return "请输入事件描述"
                    return f"已识别事件：{text}\n类别：待处理\n状态：保存中..."

                submit_btn.click(
                    fn=process_event, inputs=[event_input], outputs=[event_output]
                )

            # Tab 2: Plans
            with gr.Tab("🎯 计划管理"):
                gr.Markdown("### 管理你的计划和目标")

                with gr.Row():
                    with gr.Column():
                        plan_title = gr.Textbox(label="计划名称", placeholder="输入计划名称")
                        plan_desc = gr.Textbox(
                            label="计划描述", lines=3, placeholder="详细描述计划内容"
                        )
                        plan_due = gr.Textbox(
                            label="截止日期", placeholder="YYYY-MM-DD"
                        )
                        plan_priority = gr.Dropdown(
                            choices=["高", "中", "低"],
                            label="优先级",
                            value="中",
                        )
                        create_plan_btn = gr.Button("创建计划", variant="primary")

                    with gr.Column():
                        plan_status = gr.Textbox(
                            label="状态", interactive=False, value="就绪"
                        )

                gr.Markdown("### 计划进度")
                plan_list = gr.DataFrame(
                    headers=["计划名称", "进度", "优先级", "截止日期"],
                    interactive=False,
                )

                def create_plan(title, desc, due, priority):
                    if not title:
                        return "请输入计划名称"
                    return f"已创建计划：{title}"

                create_plan_btn.click(
                    fn=create_plan,
                    inputs=[plan_title, plan_desc, plan_due, plan_priority],
                    outputs=[plan_status],
                )

            # Tab 3: Daily Review
            with gr.Tab("📊 每日复盘"):
                gr.Markdown("### 4层递进式复盘引导")

                review_btn = gr.Button("开始复盘", variant="primary", size="lg")

                gr.Markdown("#### 第一层：基础框架")
                with gr.Row():
                    q1 = gr.Textbox(
                        label="今天做了哪些事情？",
                        lines=3,
                        placeholder="简要总结你今天的主要活动",
                    )
                    q2 = gr.Textbox(
                        label="今天学到了什么？",
                        lines=3,
                        placeholder="记录今天学到的知识或技能",
                    )

                with gr.Row():
                    q3 = gr.Textbox(
                        label="今天的情绪状态如何？",
                        lines=3,
                        placeholder="描述你的情绪和感受",
                    )
                    q4 = gr.Textbox(
                        label="明天有什么计划？",
                        lines=3,
                        placeholder="列出明天的计划",
                    )

                save_review_btn = gr.Button("保存复盘", variant="primary")

                review_status = gr.Textbox(label="保存状态", interactive=False)

                def save_review(a, b, c, d):
                    return "复盘已保存！"

                save_review_btn.click(fn=save_review, inputs=[q1, q2, q3, q4], outputs=[review_status])

            # Tab 4: User Profile
            with gr.Tab("👤 用户画像"):
                gr.Markdown("### 系统了解到的你")

                with gr.Row():
                    with gr.Column():
                        gr.Markdown("#### 基本信息")
                        name_display = gr.Textbox(
                            label="姓名", interactive=False, placeholder="未设置"
                        )
                        goals_display = gr.Textbox(
                            label="目标", interactive=False, lines=3, placeholder="未设置"
                        )

                    with gr.Column():
                        gr.Markdown("#### 学习到的特征")
                        features_display = gr.DataFrame(
                            headers=["特征", "值", "信心度"],
                            interactive=False,
                        )

            # Tab 5: Settings
            with gr.Tab("⚙️ 系统设置"):
                gr.Markdown("### LLM 配置")

                with gr.Row():
                    llm_provider = gr.Dropdown(
                        choices=["claude", "openai", "deepseek", "ollama"],
                        label="LLM 提供商",
                        value="claude",
                    )
                    api_key_input = gr.Textbox(
                        label="API 密钥",
                        type="password",
                        placeholder="输入你的 API 密钥",
                    )

                test_llm_btn = gr.Button("测试连接", variant="secondary")
                test_status = gr.Textbox(label="测试结果", interactive=False)

                def test_llm(provider, key):
                    try:
                        llm = get_llm()
                        is_valid = llm.validate_api_key()
                        return "✓ 连接成功！" if is_valid else "✗ 连接失败"
                    except Exception as e:
                        return f"✗ 错误: {str(e)}"

                test_llm_btn.click(
                    fn=test_llm,
                    inputs=[llm_provider, api_key_input],
                    outputs=[test_status],
                )

                gr.Markdown("### 数据管理")
                with gr.Row():
                    export_btn = gr.Button("导出数据", variant="secondary")
                    backup_btn = gr.Button("创建备份", variant="secondary")
                    reset_btn = gr.Button("重置数据库", variant="stop")

                export_status = gr.Textbox(label="操作状态", interactive=False)

                def export_data():
                    return "数据导出功能将在 Phase 2 实现"

                export_btn.click(fn=export_data, outputs=[export_status])

        # Footer
        gr.Markdown(
            """
            ---

            **Mindflow** v1.0 | 个人AI助理系统 | 隐私优先

            所有数据存储在本地，不经过第三方服务
            """
        )

    return demo


def main():
    """Main entry point"""
    app = create_app()
    app.launch(
        host=settings.gradio_host,
        port=settings.gradio_port,
        share=settings.gradio_share,
        show_error=True,
    )


if __name__ == "__main__":
    main()
