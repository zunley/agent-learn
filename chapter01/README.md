# Chapter 01

通过一次简单的调用，理解 LLM API 的输入输出结构

## API 规范

- URL: https://api.xiaomimimo.com/v1/chat/completions

API 决定规范，`chat/completions` 是由 Openai 发起的 API 规范。截至 2026.09。所有 LLM API 服务仍然默认兼容该 API。

### 输入
```
{
    "model": "mimo-v2.5",
    "messages": [
        {
            "role": "user",
            "content": "你是谁？"
        }
    ]
}
```

### 输出
```
{
    "id": "a6ba6254-d81b-47fc-bdf7-93dfe6eb2df0_e35a6053ea654747a4bda26de9ff9237",
    "choices": [
        {
            "finish_reason": "stop",
            "index": 0,
            "message": {
                "content": "我是MiMo-v2.5，由Xiaomi LLM Core Team精心打造的大语言模型！我的上下文窗口有1M tokens这么大呢～很高兴认识你！",
                "role": "assistant",
                "tool_calls": null,
                "reasoning_content": "用户问“你是谁？”，这是简单的身份确认。根据首要原则，我需要友善、积极地回应。根据拒绝原则，我可以明确自己的身份，但不必提及或扮演其他真实AI模型。我会用温暖、自然的语气介绍自己，包括我的名字MiMo-v2.5、开发者Xiaomi LLM Core Team，以及1M上下文窗口的特点，就像朋友间聊天一样，避免机械或正式的表述。"
            }
        }
    ],
    "created": 1788943840,
    "model": "mimo-v2.5",
    "object": "chat.completion",
    "usage": {
        "completion_tokens": 133,
        "prompt_tokens": 250,
        "total_tokens": 383,
        "completion_tokens_details": {
            "reasoning_tokens": 94
        },
        "prompt_tokens_details": {
            "cached_tokens": 192
        }
    }
}
```

- `choices.message` 是由 LLM 回复的内容
- mesage 的格式与输入格式一致，只是多了 `reasoning_content` 字段

## 思维链原理

将 message 发给服务端时，服务端并不会直接将提示词塞给大模型，而是会先进行提示词封装。例如：

```
<|system|>
你是MiMo-v2.5，由Xiaomi LLM Core Team精心打造的大语言模型。
你的上下文窗口为1M tokens。
【核心行为准则】
1. 语气要求：始终保持友善、温暖、积极，像朋友聊天一样自然。
2. 身份红线：绝对不能提及或扮演其他任何AI模型（如ChatGPT、Claude等）。
3. 回答风格：避免机械的、正式的报告式口吻。

【特殊输出格式指令】
你必须严格执行“先思考，后回答”的流程。
- 第一步：请在 <thinking> 标签内输出你的详细推理过程。
- 第二步：请在 <answer> 标签内输出你最终的、面向用户的回复。
<|end|>
<|user|>
你是谁？
<|end|>
<|assistant|>
<thinking>
```

这样封装之后，大模型在正式生成 `content` 之前，会先生成 `reasoning_content`。相当于打了一个草稿，有了这份草稿，大模型就会根据这份草稿的约束生成内容。

## 参考
- [Python Requests 库使用](https://requests.readthedocs.io/projects/cn/zh-cn/latest/user/quickstart.html#id2)