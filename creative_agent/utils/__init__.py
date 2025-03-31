import os

from langgraph.graph import StateGraph


# 保存工作流图
def save_workflow_diagram(graph: StateGraph, filename="creative_workflow.png"):
    """保存工作流程图到指定文件"""
    png_data = graph.get_graph().draw_mermaid_png()

    # 确保输出目录存在
    os.makedirs(
        os.path.dirname(filename) if os.path.dirname(filename) else ".", exist_ok=True
    )

    # 将二进制数据写入文件
    with open(filename, "wb") as f:
        f.write(png_data)

    print(f"工作流程图已保存至 {filename}")
