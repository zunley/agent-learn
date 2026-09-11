class Agent:
    """
    Agent 核心类
    维护 messages 结构
    """

    def __init__(self):
    def run(self, user_input:str):
        """
        单轮对话: 用户输入 -> Agent 回复
        自动执行 tool loop，直到 LLM 不再调用工具
        """
        while True:
            
        return 

    def chat(self):
        """
        交互式对话
        """
        while True:
            user_input = input("You: ")
            self.run(user_input)

    