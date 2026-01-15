import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


from model_module.ArkModelNew import SystemMessage

from state_module.state import State


class StateTool(State):
    type = "tool"

    def __init__(self, name: str, config: dict):
        super().__init__(name, config)
        self.is_terminal = False

    def check_transition_ready(self, context):
        return True

    async def choose_tool(self, context, agent):
        """Subclasses override this to select tool + args."""
        raise NotImplementedError("Subclasses must implement choose_tool()")

    async def execute_tool(self, tool_name, tool_args, agent):
        """Execute a tool via MCP."""
        if not agent.tool_manager:
            return "Error: No tool manager available"

        try:
            result = await agent.tool_manager.call_tool(tool_name, tool_args)
            return str(result)
        except Exception as e:
            return f"Tool error: {str(e)}"

    async def run(self, context, agent=None):
        tool_name, tool_args = await self.choose_tool(context, agent)
        tool_result = await self.execute_tool(tool_name, tool_args, agent)
        return SystemMessage(content=f"Tool result: {tool_result}")
