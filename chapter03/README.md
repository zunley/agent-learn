# Chapter 03

AI Agent 工具调用

工具的工作流程如下：

1. Agent 向大模型提供工具定义
2. 大模型决策是否采用工具
3. Agent 执行工具，反馈执行结果

这里需要明确规范的有：
1. Agent 工具定义规范
2. 大模型工具调用工具规范
3. Agent 工具结果反馈规范

## Agent 工具定义规范

```
tools=[{
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
      "additionalProperties": false
    },
    "strict": true
  }
}]

payload={
    "model": "mimo-v2.5",
    "messages": messages,
    "tools": tools,
    "tool_choice": "auto"
}
```

## 大模型调用工具规范

```
{
  "role": "assistant",
  "tool_calls": [
    {
      "id": "call_abc123xyz",
      "type": "function",
      "function": {
        "name": "write_file",
        "arguments": "{\"path\": \"test.txt\", \"content\": \"Hello World!\"}"
      }
    }
  ]
}
```

## Agent 工具结果反馈规范

```
{
  "role": "tool",
  "tool_call_id": "call_abc123xyz",
  "content": "Successfully wrote to test.txt"
}
```

## 示例
```
---------------------- LOOP 1 ----------------------------------
[
    {
        "role": "user",
        "content": "你好"
    },
    {
        "content": "你好！很高兴见到你！😊 我是MiMo，由小米大模型Core团队开发的AI助手。有什么我可以帮你的吗？无论是回答问题、协助解决问题，还是简单的聊天，我都很乐意帮助你！",
        "role": "assistant",
        "tool_calls": null,
    },
    {
        "role": "user",
        "content": "将我们的对话写入一个文件"
    },
    {
        "content": "",
        "role": "assistant",
        "tool_calls": [
            {
                "id": "call_d4e393df84344fb28c603b6c",
                "function": {
                    "arguments": "{\"path\": \"对话记录.txt\", \"content\": \"用户：你好\\nMiMo：你好！很高兴见到你！😊 我是MiMo，由小米大模型Core团队开发的AI助手。有什么我可以帮你的吗？无论是回答问题、协助解决问题，还是简单的聊天，我都很乐意帮助你！\\n用户：将我们的对话写入一个文件\"}",
                    "name": "write_file"
                },
                "type": "function"
            }
        ],
    },
    {
        "role": "tool",
        "tool_call_id": "call_d4e393df84344fb28c603b6c",
        "content": "Successfully wrote 294 bytes to 对话记录.txt"
    },
    {
        "content": "我已经将我们的对话记录写入了文件\"对话记录.txt\"中。📝\n\n这个文件包含了我们目前为止的对话内容：\n1. 你打招呼说\"你好\"\n2. 我回复了问候\n3. 你要求将对话写入文件\n\n如果你需要继续对话或者有其他问题，随时告诉我！",
        "role": "assistant",
        "tool_calls": null,
    }
]
```
- 引入工具调用后，人就不再与大模型直接对话，而是 人-Agent-大模型三方会话
- 在第二次人机对话时，在没有人类参与的情况下，Agent 和 大模型进行了一次工具调用结果返回的交互

## 参考
- [Chat Completions 工具定义](https://github.com/e-t-y-b/etyb-skills/blob/main/stacks/openai/function-calling.md#pattern-tool-definition-chat-completions)