# 运行方式：pip install openai python-dotenv
# 将 .env.example 复制为 .env 并填入 API Key，然后运行：python agentDemo1.py
import os
import sys
from dotenv import load_dotenv
from openai import OpenAI

sys.stdout.reconfigure(line_buffering=True)

# 从 .env 文件加载环境变量，避免把 API Key 硬编码进代码（防止随 git 提交泄露）
load_dotenv()

client = OpenAI(
    # base_url="https://api.deepseek.com",
    base_url="https://open.bigmodel.cn/api/paas/v4/",
    api_key=os.getenv("API_KEY"),
)

if not client.api_key:
    raise RuntimeError("未读取到 API_KEY，请将 .env.example 复制为 .env 并填入你的 API Key")

messages = []

print("=== AI Agent 对话程序 ===")
print("输入消息开始对话，输入 exit 或 quit 退出")
print("-" * 40)
print()

while True:
    user_input = input("你: ").strip()

    if not user_input or user_input.lower() in ("exit", "quit"):
        print("再见！")
        break

    messages.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="glm-5.3",
        messages=messages
    )

    assistant_message = response.choices[0].message.content
    messages.append({"role": "assistant", "content": assistant_message})

    print(f"AI: {assistant_message}\n")
