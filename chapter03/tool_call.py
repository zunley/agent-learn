#!/usr/bin/env python

"""
循环调用
1. 关注 messages 组装
"""

import os
import json
import requests
from pathlib import Path

def add_system_message(messages):
    return

def add_user_message(messages: list[dict], user_message: str):
    messages.append({"role": "user", "content": user_message})

def add_assistant_message(messages: list[dict], assistant_message: dict):
    messages.append(assistant_message)

def add_tool_message(messages: list[dict], tool_call_id: str, tool_message: str):
    messages.append({"role": "tool", "tool_call_id": tool_call_id, "content": tool_message})

def show_assistant_message(assistant_message: dict):
    print(json.dumps(assistant_message, indent=4, ensure_ascii=False))

def show_messages(messages: dict):
    print(json.dumps(messages, indent=4, ensure_ascii=False))

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

# 工具定义
def build_tools() -> list[dict]:
    write_file_tool={
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Write content to a file at the specified path. Use when the user asks to save or create a file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Path to the file to write"
                    },
                    "content": {
                        "type": "string",
                        "description": "Content to write to the file"
                    }
                },
                "required": ["path", "content"],
                "additionalProperties": False
            },
        "strict": True
        }
    }
    return [write_file_tool]

TOOL_FUNCTIONS = {}
def register_tool(name):
    def decorator(func):
        TOOL_FUNCTIONS[name] = func
        return func
    return decorator

# write file 工具
@register_tool("write_file")
def tool_function_write_file(path: str, content: str):
    """
    将 content 写入指定 path 的文件
    """
    try:
        target = Path(path).resolve()
        # 确保父目录存在
        target.parent.mkdir(parents=True, exist_ok=True)
        # 写入文件
        encoded = content.encode("utf-8")
        target.write_text(content, encoding="utf-8")
        return f"Successfully wrote {len(encoded)} bytes to {path}"
    except Exception as e:
        return f"Error: {type(e).__name__}: {e}"

def dispatch_tool_call(tool_call: dict) -> str:
    name = tool_call["function"]["name"]
    func = TOOL_FUNCTIONS[name]
    args = json.loads(tool_call["function"]["arguments"])
    # 字典解包
    result = func(**args)
    return result

def call_llm(api_url: str, api_key: str, model: str, messages: list[dict], tools: list[dict]) -> dict:
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    payload = {
        "model": model,
        "messages": messages,
        "tools": tools
    }

    resp = requests.post(
        api_url,
        headers=headers,
        data=json.dumps(payload),
    )
    data = resp.json()
    return data["choices"][0]["message"]

# -----------环境初始化 ----------
api_url = os.getenv("LLM_API_URL")
api_key = os.getenv("LLM_API_KEY")
model = os.getenv("LLM_MODEL")
if not api_key or not api_url or not model:
   raise RuntimeError(
        "检查环境变量 LLM_API_URL, LLM_API_KRY, LLM_MODEL"
        )
#-------------------------------

def agent_run_once(messages: list[dict]):
    MAX_TOOL_ROUNDS = 10
    tool_loop_num = 0
    while True:
        if tool_loop_num > MAX_TOOL_ROUNDS:
            print("Assistant: [达到工具调用上限，停止本轮]")
            break
        assistant_message = call_llm(api_url, api_key, model, messages, build_tools())
        add_assistant_message(messages, assistant_message)
        show_messages(messages)
        # 处理工具调用
        tool_calls = assistant_message.get("tool_calls")
        # 如果不需要调用工具，说明大模型直接给出回复，直接结束本次对话，交由用户控制
        if not tool_calls:
            break
        for tool_call in tool_calls:
            result = dispatch_tool_call(tool_call)
            add_tool_message(messages, tool_call.get("id"), result)

def main() -> None:
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
        agent_run_once(messages)
        
        loop_num += 1
        print(f"---------------------- LOOP {loop_num} ----------------------------------")
        print_messages(messages)
        print()
        
if __name__ == '__main__':
    main()