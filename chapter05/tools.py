class ToolRegistry:
    def tool(self, name: str | None = None, description: str = ""):
        """
        装饰器：注入工具
        """
        def decorator(func):
            tool_name = name or func.__name__
            tool_desc = description or (func.__doc__ or "").strip()
            schema = self._build_schema(tool_name, tool_desc, func)
            self._tools[tool_name] = {
                "func": func,
                "schema": schema,
            }
            return func
        return decorator
    
    def _build_schema(self, tool_name: str, tool_desc, func) -> dict: