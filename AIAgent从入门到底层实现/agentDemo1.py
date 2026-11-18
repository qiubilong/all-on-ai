# 运行方式：pip install openai
# 将 your-api-key 替换为你的 DeepSeek API Key，保存为 agent.py 后运行：python agent.py

from openai import OpenAI

client = OpenAI(
    base_url="https://api.deepseek.com",
    api_key="sk-9c041ae221654bd6a90ab15c3e58d189"
)

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
        model="deepseek-v4-flash",
        messages=messages
    )

    assistant_message = response.choices[0].message.content
    messages.append({"role": "assistant", "content": assistant_message})

    print(f"AI: {assistant_message}\n")
