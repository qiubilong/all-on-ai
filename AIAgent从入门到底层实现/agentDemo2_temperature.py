# temperature 是最常用的生成参数，控制 LLM 输出的随机性：
# temperature=0    # 每次都选最可能的词，输出稳定、确定 --------   适合：代码生成、数据提取、分类
# temperature=0.7  # 有一定随机性，输出自然、多样（默认值） ----   适合：对话、写作、翻译
# temperature=1.5  # 高度随机，输出发散、创意强         ------  适合：头脑风暴、创意写作

import os
import sys
from dotenv import load_dotenv
from openai import OpenAI

sys.stdout.reconfigure(line_buffering=True)
# 从 .env 文件加载环境变量，避免把 API Key 硬编码进代码（防止随 git 提交泄露）
load_dotenv()

# 初始化客户端，连接 DeepSeek API
client = OpenAI(
    base_url="https://open.bigmodel.cn/api/paas/v4/",
    api_key=os.getenv("API_KEY"),
)

# System Prompt — 定义 AI 的角色和行为规则
SYSTEM_PROMPT = """你是一个智能助手。回答要简洁直接。
如果用户的问题你不确定，就说"我不确定"，不要编造答案。"""

# 初始化 messages 列表，第一条是 system 消息
messages = [
    {"role": "system", "content": SYSTEM_PROMPT}
]

print("=== AI Agent 对话程序 ===")
print("输入消息开始对话，输入 exit 或 quit 退出")
print("-" * 40)
print()

# 对话主循环
while True:
    user_input = input("你: ").strip()

    # 输入为空或输入 exit/quit 则退出循环
    if not user_input or user_input.lower() in ("exit", "quit"):
        print("再见！")
        break

    # 将用户消息添加到对话历史
    messages.append({"role": "user", "content": user_input})

    # 调用 Chat Completion API，传入完整对话历史
    response = client.chat.completions.create(
        model="glm-5.3",
        messages=messages,
        temperature=0.7
    )

    # 提取 AI 回复并添加到对话历史
    assistant_message = response.choices[0].message.content
    messages.append({"role": "assistant", "content": assistant_message})

    print(f"AI: {assistant_message}\n")

    # 显示本次请求的 Token 消耗
    usage = response.usage
    print(f"[本次消耗: 输入 {usage.prompt_tokens} + 输出 {usage.completion_tokens} = {usage.total_tokens} tokens]")
    print(f"[对话历史: {len(messages)} 条消息]\n")
