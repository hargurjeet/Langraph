import streamlit as st
import streamlit.components.v1 as components
from langgraph.graph import StateGraph, END
from langchain_core.messages import AnyMessage, SystemMessage, HumanMessage, ToolMessage
from langchain_openai import ChatOpenAI  # Add this import statement
from langchain_community.tools.tavily_search import TavilySearchResults
import os
from dotenv import load_dotenv
import matplotlib.pyplot as plt
from typing import TypedDict, Annotated
import operator

# Load environment variables from .env file
load_dotenv()

# Define the Agent class
class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]

class Agent:

    def __init__(self, model, tools, system=""):
        self.system = system
        graph = StateGraph(AgentState)
        graph.add_node("llm", self.call_openai)
        graph.add_node("action", self.take_action)
        graph.add_conditional_edges(
            "llm",
            self.exists_action,
            {True: "action", False: END}
        )
        graph.add_edge("action", "llm")
        graph.set_entry_point("llm")
        self.graph = graph.compile()
        self.tools = {t.name: t for t in tools}
        self.model = model.bind_tools(tools)

    def exists_action(self, state: AgentState):
        result = state['messages'][-1]
        return len(result.tool_calls) > 0

    def call_openai(self, state: AgentState):
        messages = state['messages']
        if self.system:
            messages = [SystemMessage(content=self.system)] + messages
        message = self.model.invoke(messages)
        return {'messages': [message]}

    def take_action(self, state: AgentState):
        tool_calls = state['messages'][-1].tool_calls
        results = []
        for t in tool_calls:
            print(f"Calling: {t}")
            if not t['name'] in self.tools:      # check for bad tool name from LLM
                print("\n ....bad tool name....")
                result = "bad tool name, retry"  # instruct LLM to retry if bad
            else:
                result = self.tools[t['name']].invoke(t['args'])
            results.append(ToolMessage(tool_call_id=t['id'], name=t['name'], content=str(result)))
        print("Back to the model!")
        return {'messages': results}

# Streamlit app
st.title("Agent Based Search Using LangGraph")

# Text input
user_input = st.text_area("Enter text:", placeholder="Type your query here...")

if st.button("Search with Agents"):
    if user_input:
        # Initialize AI agent
        tool = TavilySearchResults(max_results=4)
        prompt = """You are a smart research assistant. Use the search engine to look up information. 
        You are allowed to make multiple calls (either together or in sequence). 
        Only look up information when you are sure of what you want. 
        If you need to look up some information before asking a follow up question, you are allowed to do that!"""
        model = ChatOpenAI(model="gpt-3.5-turbo")
        abot = Agent(model, [tool], system=prompt)
        
        # Process user input
        messages = [HumanMessage(content=user_input)]
        result = abot.graph.invoke({"messages": messages})
        
        # Display final output
        st.subheader("Final Output")
        final_output = result['messages'][-1].content
        st.write(final_output)
        
        # Display detailed processing
        st.subheader("Detailed Processing")
        st.json(result)
    else:
        st.error("Please enter some text to generate the graph.")