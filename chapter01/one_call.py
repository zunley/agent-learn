#!/usr/bin/env python

"""
最小运行示例：进行一次 LLM 调用
1. 关注输入格式
2. 关注输出格式
"""

import os
import json
import requests

def call_llm(api_url: str, api_key: str, model: str, message: str):
    """
    进行 LLM HTTP API 调用
    """
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    # type(payload): dict
    # type(json.dumps(payload)): str
    # type(json.dumps(payload).encode('utf-8')): bytes
    payload = {
        "model": "mimo-v2.5",
        "messages": [
            {"role": "user", "content": message}
        ]
    }
    # debug
    print("输入：")
    print(json.dumps(payload,indent=4, ensure_ascii=False))

    response = requests.post(
        api_url,
        headers=headers,
        data=json.dumps(payload),
    )
    return response.json()

def main() -> None:
    api_url = os.getenv("LLM_API_URL")
    api_key = os.getenv("LLM_API_KEY")
    model = os.getenv("LLM_MODEL")
    if not api_key or not api_url:
        raise RuntimeError(
            "检查环境变量 LLM_API_URL, LLM_API_KEY, LLM_MODEL"
        )
    message = "你是谁？"
    response = call_llm(api_url, api_key, model, message)
    # indent=4 格式化
    # ensure_ascii=False 保持中文
    print("输出：")
    print(json.dumps(response, indent=4, ensure_ascii=False))

if __name__ == '__main__':
    main()