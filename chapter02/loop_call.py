#!/usr/bin/env python

"""
循环调用
1. 关注 messages 组装
"""

import os
import json
import requests

def add_system_message(messages):
    return

def add_user_message(messages: list[dict], user_message: str):
    messages.append({"role": "user", "content": user_message})

def add_assistant_message(messages: list[dict], assistant_message: dict):
    messages.append(assistant_message)

def show_assistant_message(assistant_message: dict):
    print(json.dumps(assistant_message, indent=4, ensure_ascii=False))

def print_messages(messages):
    for i, msg in enumerate(messages):
        role = msg.get("role", "unknown")
        content = msg.get("content", "")
        if isinstance(content, list):
            content = " | ".join(
                item.get("text", f"[{item.get('type')}]")
                if isinstance(item, dict) else str(item)
                for item in content
            )
        print(f"[{i}]\t{role.upper()}:\t {content}")

def call_llm(api_url: str, api_key: str, model: str, messages: list[dict]) -> dict:

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    payload = {
        "model": model,
        "messages": messages
    }

    resp = requests.post(
        api_url,
        headers=headers,
        data=json.dumps(payload),
    )
    data = resp.json()
    return data["choices"][0]["message"]

def main() -> None:
    # 环境初始化
    #----------
    api_url = os.getenv("LLM_API_URL")
    api_key = os.getenv("LLM_API_KEY")
    model = os.getenv("LLM_MODEL")
    if not api_key or not api_url or not model:
        raise RuntimeError(
            "检查环境变量 LLM_API_URL, LLM_API_KRY, LLM_MODEL"
        )
    #----------
    messages = []
    add_system_message(messages)
    loop_num = 0
    while True:
        # user_message example: 'Hello'
        user_message = input("You: ").strip()

        # 控制消息
        match user_message:
            case "/exit":
                print("Bye!")
                break
        
        # 1. 追加用户消息
        add_user_message(messages, user_message)
        # 2. 调用大模型
        # llm_message example: '{"role": "assistant", content: "", "reasoning_content": ""}'
        assistant_message = call_llm(api_url, api_key, model, messages)
        # 3. 追加助手消息
        add_assistant_message(messages, assistant_message)
        loop_num += 1
        print(f"---------------------- LOOP {loop_num} ----------------------------------")
        print_messages(messages)
        print()
        
if __name__ == '__main__':
    main()