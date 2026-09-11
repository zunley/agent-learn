from dataclasses import dataclass, asdict

@dataclass
class Message:
    role: str
    content: str | None = None
    reasoning_content: str | None = None
    # 工具
    tools_calls: list[ToolCall]
    tool_call_id: str


@dataclass
class ToolCall:
    id: str
    type: str
    function: str
