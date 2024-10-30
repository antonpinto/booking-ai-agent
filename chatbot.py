from dotenv import load_dotenv
import streamlit as st
from langchain import hub
from langchain_core.tools import tool
from langchain.agents import AgentExecutor, create_react_agent, load_tools
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.callbacks.streamlit import (
    StreamlitCallbackHandler,
)


@tool(return_direct=True)
def office_occupation(location: str) -> str:
    """Returns how many people are in the office"""
    return f"There are 2 people in the {location} office"


@tool(return_direct=True)
def book_room(location: str) -> str:
    """Books a room in the office"""
    return f"Room 1 booked at the {location} office for 2 people"


load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0, streaming=True)
tools = [book_room, office_occupation]
prompt = hub.pull("hwchase17/react")
agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

if prompt := st.chat_input():
    st.chat_message("user").write(prompt)
    with st.chat_message("assistant"):
        st_callback = StreamlitCallbackHandler(st.container())
        response = agent_executor.invoke(
            {"input": prompt}, {"callbacks": [st_callback]}
        )
        st.write(response["output"])
