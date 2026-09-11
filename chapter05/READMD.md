# Chapter 05

实现一个规范的 Agent

1. 代码规范
2. 必要的工具
    - 读文件
    - 写文件
    - 执行 shell

## 文件结构
```
 chapter05/
 ├── init.py
 ├── llm_client.py      # LLM 通信层（环境配置、API 调用）                                                                                 
 ├── tool_registry.py   # 工具注册与调度（装饰器注册、schema 自动生成、dispatch）
 ├── agent.py           # Agent 核心（system prompt、tool loop、消息管理）                             
 └── main.py            # 入口（组装 agent，启动交互） 
```
## 实现策略
1. 实现调度流程
2. 
