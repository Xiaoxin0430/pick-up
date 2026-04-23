
from dotenv import load_dotenv
from openai import OpenAI
import os
from pathlib import Path

# 系统提示词
AGENT_SYSTEM_PROMPT = """
你是一个个人笔记网站智能助手。你的任务是分析用户的请求，回答问题。若需要外部工具，则使用我定义的工具一步步地解决问题。由于目前我还在开发阶段，若你无法实现
并没有对应的工具，请告诉用户：“抱歉，目前我还在开发中，可用的工具仅有agent_tool”.agent_tool为我已经实现的可用工具。

# 可用工具:
- `get_current_time(city: str)`: 获取当前北京时间。


# 输出格式要求:
你的每次回复必须严格遵循以下格式，包含一对Thought和Action：

Thought: [你的思考过程和下一步计划]
Action: [你要执行的具体行动]

Action的格式必须是以下之一：
1. 调用工具：function_name(arg_name="arg_value")
2. 结束任务：Finish[最终答案]

# 重要提示:
- 不需要工具的问题，请你直接调用自己的知识库回答。
- 每次只输出一对Thought-Action
- Action必须在同一行，不要换行

请开始吧！
"""

load_dotenv(Path(__file__).resolve().parents[1] / "static" / ".env")


client = OpenAI(
    api_key=os.getenv("LLM_API_KEY"),
    base_url=os.getenv("LLM_BASE_URL"),
)


def think(content:str):
    response = ""
    messages = [
        {"role":"system", "content": AGENT_SYSTEM_PROMPT},
        {"role": "user", "content": content}
        ]

    # compile是流对象，是一个可迭代的数据流。每次迭代都会返回一个新的数据块，包含模型的部分回复和思考过程。
    completion = client.chat.completions.create(
        model="qwen3-max",  # 您可以按需更换为其它深度思考模型
        messages=messages,
        extra_body={"enable_thinking": False},
        stream=True
    )
    is_answering = False  # 是否进入回复阶段
    # chunk是遍历compile每次拿到的增量结果，就是模型本次追加内容
    print("\n" + "=" * 20 + "思考过程" + "=" * 20)
    for chunk in completion:
        delta = chunk.choices[0].delta
        # 判断此次是否有思考内容，若有进行打印
        if hasattr(delta, "reasoning_content") and delta.reasoning_content is not None:
            if not is_answering:
                print(delta.reasoning_content, end="", flush=True)
        # 判断是否有正式内容,若有则说明开始输出最终回答,打印
        if hasattr(delta, "content") and delta.content:
            if not is_answering:
                print("\n" + "=" * 20 + "完整回复" + "=" * 20)
                is_answering = True
            # print(delta.content, end="", flush=True)
            response += delta.content
    return response
if __name__ == '__main__':
    responses = think("你好啊")
    print(responses)

