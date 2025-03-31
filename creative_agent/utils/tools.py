from langchain_core.tools import tool


@tool
def transfer_to_idea_creator():
    """将任务转交给创意生成专家"""
    return


@tool
def transfer_to_idea_evaluator():
    """将任务转交给创意评估专家"""
    return


@tool
def transfer_to_storyboard_creator():
    """将任务转交给分镜脚本专家"""
    return


@tool
def complete_workflow():
    """完成当前工作流，输出最终结果"""
    return
