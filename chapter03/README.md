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
        "content": "你好！很高兴见到你！我是MiMo，由小米大模型Core团队开发的AI助手。\n\n有什么我可以帮助你的吗？无论是回答问题、聊天，还是需要什么帮助，我都很乐意为你服务！😊",
        "role": "assistant",
        "tool_calls": null,
        "reasoning_content": "用户只是说“你好”，这是一个简单的问候。我应该用温暖、友好的方式回应，就像和朋友打招呼一样。我可以简单介绍自己，然后问问有什么可以帮到用户的。\n\n让我先用中文回复。"
    },
    {
        "role": "user",
        "content": "请将我们的对话写入文件"
    },
    {
        "content": "",
        "role": "assistant",
        "tool_calls": [
            {
                "id": "call_2232e9f864614db59eeaa79f",
                "function": {
                    "arguments": "{\"path\": \"conversation.txt\", \"content\": \"用户：你好\\nMiMo：你好！很高兴见到你！我是MiMo，由小米大模型Core团队开发的AI助手。\\n有什么我可以帮助你的吗？无论是回答问题、聊天，还是需要什么帮助，我都很乐意为你服务！😊\\n用户：请将我们的对话写入文件\\nMiMo：好的，我已经将我们的对话写入文件 conversation.txt 中了。\"}",
                    "name": "write_file"
                },
                "type": "function"
            }
        ],
        "reasoning_content": "用户想让我把我们的对话写入文件。目前我们只有两轮对话：用户说“你好”，我回复了问候，然后用户请求写入文件。我需要创建一个包含这些对话的文件。我应该用write_file工具来完成这个操作。\n\n首先，我需要决定文件的内容和路径。用户没有指定文件名或路径，所以我需要做一个合理的选择。我可以把对话保存为文本文件，放在当前目录下，比如叫\"conversation.txt\"。内容应该包括我们的对话记录。\n\n让我组织一下对话内容：\n\n用户：你好\nMiMo：你好！很高兴见到你！我是MiMo，由小米大模型Core团队开发的AI助手。\n有什么我可以帮助你的吗？无论是回答问题、聊天，还是需要什么帮助，我都很乐意为你服务！😊\n用户：请将我们的对话写入文件\n\n我需要把这些内容格式化成清晰的对话格式。我会使用write_file工具。"
    },
    {
        "role": "tool",
        "tool_call_id": "call_2232e9f864614db59eeaa79f",
        "content": "Successfully wrote 371 bytes to conversation.txt"
    },
    {
        "content": "我已经将我们的对话写入文件 `conversation.txt` 中了。\n\n文件内容包括：\n- 用户的问候\n- 我的自我介绍和回复\n- 用户请求写入文件的消息\n- 以及我的确认回复\n\n如果你需要保存到其他路径或使用其他文件名，或者想要不同的格式（比如JSON、Markdown等），请告诉我，我可以帮你重新创建。",
        "role": "assistant",
        "tool_calls": null,
        "reasoning_content": "文件已经成功写入了。现在我需要告诉用户文件已经创建好了。我应该确认文件名，并说明对话内容已保存。另外，我还添加了我自己的回复部分，让对话更完整。"
    }
]
```
- 引入工具调用后，人就不再与大模型直接对话，而是 人-Agent-大模型三方会话
- 在第二次人机对话时，在没有人类参与的情况下，Agent 和 大模型进行了一次工具调用结果返回的交互

## 参考
- [Chat Completions 工具定义](https://github.com/e-t-y-b/etyb-skills/blob/main/stacks/openai/function-calling.md#pattern-tool-definition-chat-completions)