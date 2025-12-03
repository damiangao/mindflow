#!/bin/bash

# Mindflow 技术栈文档快速查看脚本

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║         Mindflow 技术栈学习文档快速导航                        ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
echo "选择要查看的文档："
echo ""
echo "1) 快速参考 - TECH_STACK_SUMMARY.md"
echo "   └─ 一页纸快速查询，适合快速了解"
echo ""
echo "2) 详细指南 - TECH_STACK_LEARNING.md"
echo "   └─ 完整的学习指南，包含所有细节"
echo ""
echo "3) 项目索引 - INDEX.md"
echo "   └─ 所有项目文档的导航"
echo ""
echo "4) 系统架构 - docs/ARCHITECTURE.md"
echo "   └─ 理解项目的整体设计"
echo ""
echo "5) 开发指南 - docs/DEVELOPMENT.md"
echo "   └─ Phase 1-6的详细检查清单"
echo ""
echo "6) 数据库设计 - docs/DATABASE.md"
echo "   └─ 7个表的完整设计"
echo ""
echo "7) 项目规划 - PLAN.md"
echo "   └─ 完整的产品规划和需求分析"
echo ""
echo "8) 版本管理 - planning/README.md"
echo "   └─ 项目版本管理系统"
echo ""
echo "0) 退出"
echo ""
read -p "请选择 (0-8): " choice

case $choice in
    1)
        cat TECH_STACK_SUMMARY.md | less
        ;;
    2)
        cat TECH_STACK_LEARNING.md | less
        ;;
    3)
        cat INDEX.md | less
        ;;
    4)
        cat docs/ARCHITECTURE.md | less
        ;;
    5)
        cat docs/DEVELOPMENT.md | less
        ;;
    6)
        cat docs/DATABASE.md | less
        ;;
    7)
        cat PLAN.md | less
        ;;
    8)
        cat planning/README.md | less
        ;;
    0)
        echo "再见！"
        ;;
    *)
        echo "无效选择，请重试"
        ;;
esac
