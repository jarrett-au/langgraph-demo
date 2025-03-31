from typing import Any, Dict, Literal

from langgraph.types import Command

from creative_agent.utils.llm import get_model
from creative_agent.utils.state import AgentState
from creative_agent.utils.tools import (
    complete_workflow,
    transfer_to_idea_creator,
    transfer_to_idea_evaluator,
    transfer_to_storyboard_creator,
)

model = get_model()


# 创意生成专家
def idea_creator(
    state: AgentState, config: Dict[str, Any]
) -> Command[Literal["idea_evaluator", "__end__"]]:
    system_prompt = """你是一位古风回合制游戏广告创意专家。
    根据用户需求，创造吸引人的游戏广告创意概念。
    创意应包含：核心卖点、情感诉求、视觉风格和叙事框架。
    请考虑以下广告类型：角色展示、玩法演示、世界观、福利活动等。
    完成创意后，请转交给评估专家进行评估。"""

    messages = [{"role": "system", "content": system_prompt}] + state["messages"]
    ai_msg = model.bind_tools([transfer_to_idea_evaluator]).invoke(messages)

    if len(ai_msg.tool_calls) > 0:
        tool_call = ai_msg.tool_calls[-1]
        tool_call_id = tool_call["id"]
        tool_msg = {
            "role": "tool",
            "content": "创意已生成，正在转交评估",
            "tool_call_id": tool_call_id,
        }

        if tool_call["name"] == "transfer_to_idea_evaluator":
            return Command(
                goto="idea_evaluator", update={"messages": [ai_msg, tool_msg]}
            )
        else:
            return {"messages": [ai_msg, tool_msg]}

    return {"messages": [ai_msg]}


# 评估专家
def idea_evaluator(
    state: AgentState,
) -> Command[Literal["idea_creator", "storyboard_creator", "__end__"]]:
    system_prompt = """你是一位游戏广告创意评估专家。
    评估维度包括：
    1. 新颖性：创意是否独特，区别于市场同类产品
    2. 可实现性：考虑AI生成和素材剪辑的难度
    3. 目标受众吸引力：创意是否能引起目标用户兴趣
    4. 时长适配：是否适合30s/60s广告格式
    
    给出1-10分的评分和具体改进建议。
    如需修改创意，请转交回创意专家；
    如创意合格，请转交给分镜脚本专家。"""

    messages = [{"role": "system", "content": system_prompt}] + state["messages"]
    ai_msg = model.bind_tools(
        [
            transfer_to_idea_creator,
            transfer_to_storyboard_creator,
        ]
    ).invoke(messages)

    if len(ai_msg.tool_calls) > 0:
        tool_call = ai_msg.tool_calls[-1]
        tool_call_id = tool_call["id"]
        tool_msg = {
            "role": "tool",
            "content": "评估完成",
            "tool_call_id": tool_call_id,
        }

        if tool_call["name"] == "transfer_to_idea_creator":
            return Command(goto="idea_creator", update={"messages": [ai_msg, tool_msg]})
        elif tool_call["name"] == "transfer_to_storyboard_creator":
            return Command(
                goto="storyboard_creator", update={"messages": [ai_msg, tool_msg]}
            )
        else:
            return {"messages": [ai_msg, tool_msg]}

    return {"messages": [ai_msg]}


# 分镜脚本专家
def storyboard_creator(
    state: AgentState, config: Dict[str, Any]
) -> Command[Literal["idea_evaluator", "__end__"]]:
    system_prompt = """你是一位游戏广告分镜脚本专家。
    将创意转化为详细分镜脚本，包含以下元素：
    1. 镜号：场景编号
    2. 景别：全景、中景、特写等
    3. 运镜：固定、推拉摇移跟等
    4. 场景：具体环境描述
    5. 视角：主观/客观视角
    6. 内容描述：画面中发生的动作和事件
    7. 台词/文案：角色台词或画面文字
    8. 时长：各镜头时长，总时长控制在30s或60s
    
    完成后可转交给评估专家再次评估，或完成工作流。"""

    messages = [{"role": "system", "content": system_prompt}] + state["messages"]
    ai_msg = model.bind_tools([transfer_to_idea_evaluator, complete_workflow]).invoke(
        messages
    )

    if len(ai_msg.tool_calls) > 0:
        tool_call = ai_msg.tool_calls[-1]
        tool_call_id = tool_call["id"]
        tool_msg = {
            "role": "tool",
            "content": "分镜脚本已生成",
            "tool_call_id": tool_call_id,
        }

        if tool_call["name"] == "transfer_to_idea_evaluator":
            return Command(
                goto="idea_evaluator", update={"messages": [ai_msg, tool_msg]}
            )
        else:
            return {"messages": [ai_msg, tool_msg]}

    return {"messages": [ai_msg]}
