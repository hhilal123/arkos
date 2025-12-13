# agent.py

import os
import sys
from pydantic import BaseModel, create_model, Field
from typing import List, Tuple
import json
from enum import Enum


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from state_module.state_handler import StateHandler
from state_module.state import State, AgentState
from model_module.ArkModelNew import ArkModelLink, UserMessage, AIMessage, SystemMessage
from tool_module.tool import Tool
from memory_module.memory import Memory


MAX_ITER = 10


class Agent:
    def __init__(
        self, agent_id: str, flow: StateHandler, memory: Memory, llm: ArkModelLink
    ):
        self.agent_id = agent_id
        self.flow = flow
        self.memory = memory
        self.llm = llm
        self.current_state = self.flow.get_initial_state()
        self.context: Dict[str, Any] = {}

        self.tools = []
        self.tool_names = []

    def bind_tool(tool):

        self.tool.append(tool)

    def find_downloaded_tool(embedding):
        tool = Tool.pull_tool_from_registry(embedding)
        tool_name = tool.tool
        self.bind_tool(tool)
        self.tool_names.append(tool_name)

    def create_next_state_class(self, options: List[Tuple[str, str]]):
        """
        options: list of tuples (next_state, description of state)
        Returns a Pydantic model class with a single field 'next_state',
        whose value must be one of the provided state names.
        """

        # Dynamically build an Enum of allowed states
        enum_dict = {state: state for state, desc in options}

        # add desc into enum dict
        NextStateEnum = Enum("NextStateEnum", enum_dict)

        # Build the model with a single constrained field
        NextStateModel = create_model(
            "NextState",
            next_state=(NextStateEnum, Field(..., description="The chosen next state")),
        )

        return NextStateModel

    def call_llm(self, input=None, context=None, json_schema=None):
        """
        Agent's interface with chat model
        input: messages (list), json_schema (json)

        output: AI Message
        """

        chat_model = self.llm
        if context:

            llm_response = chat_model.generate_response(context, json_schema)

        else:
            messages = [SystemMessage(content=input)]
            llm_response = chat_model.generate_response(messages, json_schema)

        return AIMessage(content=llm_response)

    def choose_transition(self, transitions_dict, messages):

        prompt = "given the following state transitions, and the preceeding context. output the most reasonable next state. do not use tool result to determine the next state"
        transition_tuples = list(zip(transitions_dict["tt"], transitions_dict["td"]))

        # creates pydantic class and a model dump
        NextStates = self.create_next_state_class(transition_tuples)
        json_schema = {
            "type": "json_schema",
            "json_schema": {
                "name": "class_options",
                "schema": NextStates.model_json_schema(),
            },
        }

        context_text = [SystemMessage(content=prompt)] + messages
        output = self.call_llm(context=context_text, json_schema=json_schema)
        # print(output.content)
        
        # Check if LLM call failed (error message instead of valid response)
        if output.content and output.content.startswith("Error:"):
            raise RuntimeError(f"LLM connection failed - is the LLM server running on port 30000? Error: {output.content}")
        
        try:
            structured_output = json.loads(output.content)
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Failed to parse LLM response as JSON. Response was: '{output.content[:200]}'") from e

        # HANDLE ERROR GRACEFULL
        if "error" in output.content:
            raise ValueError("AGENT.PY FAILED LLM CALL")
        next_state_name = structured_output["next_state"]

        return next_state_name

    def step(self):
        """
        Runs the agent until reaching a terminal state or completion.
        Returns the last AIMessage produced.
        """

        print("recieved message")
        messages_list = self.context.get("messages", [])
        # if not self.current_state:
        #     print("GETTINT INITIAL")
        #     self.current_state = self.flow.get_initial_state()

        last_ai_message = None

        retry_count = 0
        print(self.current_state)
        print(self.current_state.is_terminal)

        while not self.current_state.is_terminal:
            ### DEBUGGING

            if retry_count > MAX_ITER:
                print("MAX ITER REACHED")
                break
            retry_count += 1

            ### DEBUGGING
            print(self.current_state)
            print("MSGS_LIST", messages_list[-1])
            update = self.current_state.run(messages_list, self)
            print("UPDATE", update)
            if update:
                messages_list.append(update)
                if isinstance(update, AIMessage):
                    last_ai_message = update

            if self.current_state.is_terminal:
                print("REACHED TERMINAL")
                break

            if self.current_state.check_transition_ready(messages_list):
                transition_dict = self.flow.get_transitions(
                    self.current_state, messages_list
                )
                transition_names = transition_dict["tt"]

                if len(transition_names) == 1:
                    next_state_name = transition_names[0]
                else:
                    next_state_name = self.choose_transition(
                        transition_dict, messages_list
                    )

                self.current_state = self.flow.get_state(next_state_name)

            else:
                print("REACHED NO NEXT STATE")
                break  # No transition ready, exit gracefully
        print("LAST_AI_MSG", last_ai_message)
        self.current_state = self.flow.get_state("agent_reply")
        return last_ai_message


if __name__ == "__main__":

    content = "how are you "

    # Resolve state graph path relative to this script's location (not CWD)
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    state_graph_path = os.path.join(
        os.path.dirname(script_dir),  # Go up to arkos root
        "state_module",
        "state_graph.yaml"
    )
    flow = StateHandler(yaml_path=state_graph_path)
    memory = Memory(agent_id="ark-agent")
    llm = ArkModelLink(
        base_url="http://localhost:30000/v1"
    )  # Your already OAI-compatible model
    test_agent = Agent(agent_id="ark-agent", flow=flow, memory=memory, llm=llm)
    context_msgs = []

    test_agent.context["messages"] = context_msgs

    context_msgs.append(UserMessage(content="My name is Bill"))

    context_msgs.append(AIMessage(content=test_agent.step().content))

    context_msgs.append(UserMessage(content="What is my name"))

    # print(test_agent.context["messages"])

    context_msgs.append(AIMessage(content=test_agent.step().content))

    # print(test_agent.context["messages"])
