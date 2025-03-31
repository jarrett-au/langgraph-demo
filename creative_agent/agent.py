from langgraph.graph import START, StateGraph

from creative_agent.utils.nodes import idea_creator, idea_evaluator, storyboard_creator
from creative_agent.utils.state import AgentState

# 构建工作流图
builder = StateGraph(AgentState)
builder.add_node("idea_creator", idea_creator)
builder.add_node("idea_evaluator", idea_evaluator)
builder.add_node("storyboard_creator", storyboard_creator)

# 定义工作流边缘
builder.add_edge(START, "idea_creator")

# 编译图
creative_workflow = builder.compile()
