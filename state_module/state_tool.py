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



    def choose_tool(self, context, Tool_Manager):
        """
        Chooses tool to use based on the context and server


        """



    def execute_tool(self, context, tool_registry):
        """
        Parses and fills args for chosen tool for tool call execution


        """







    def run(self, context, agent=None):


        # extract tool name 

        # extract tool parameters


        # call tool 
        

        # return tool msg
        print("TOOL RESULT PLACEHOLDER")
        return SystemMessage(content="Result: 3*6 is 18")

