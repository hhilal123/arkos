import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


from model_module.ArkModelNew import ArkModelLink, UserMessage, AIMessage, SystemMessage

from state_module.state import State
from state_module.state_registry import register_state


@register_state
class StateTool(State):
    type = "tool"

    def __init__(self, name: str, config: dict):
        super().__init__(name, config)
        self.is_terminal = False

    def check_transition_ready(self, context):
        return True



    def choose_tool(self, context, agent):
        """
        Chooses tool to use based on the context and server

        
        """

        raise NotImplementedError


        prompt="based on the above user request, choose the tool and arguments for the tool which will satisfy the users request"


        all_tools = agent.tool_manager.list_all_tools()

        

    def execute_tool(self, tool_call, agent):
        """
        Parses and fills args for chosen tool for tool call execution


        """

        raise NotImplementedError

        tool_name = tool_args['tool_name']
        tool_args= tool_call['tool_args']

        tool_result = agent.tool_manager.call_tool(tool_name=tool_name, arguments=tool_args)












    def run(self, context, agent=None):


        tool_arg_dict = self.choose_tool(context, agent)

        tool_result = self.execute_tool(context, agent)

        return SystemMessage(content=tool_result)

