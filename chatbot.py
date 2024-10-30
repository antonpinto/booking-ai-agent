from typing import Literal
from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent
import streamlit as st


@tool(return_direct=True)
def office_occupation(location: str, date: str) -> str:
    """Returns how many people are in the office"""
    return f"There are 2 people in the {location} office on {date}"


@tool(return_direct=True)
def book_room(location: str, date: str) -> str:
    """Books a room on [date] in the [location]"""
    return f"Room 1 booked at the {location} office on {date} for 2 people"


@tool
def get_weather(city: Literal["nyc", "sf"]):
    """Use this to get weather information."""
    if city == "nyc":
        return "It might be cloudy in nyc"
    elif city == "sf":
        return "It's always sunny in sf"
    else:
        raise AssertionError("Unknown city")


load_dotenv()
tools = [get_weather, book_room, office_occupation]
model = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
graph = create_react_agent(model, tools=tools)

st.title("💬 Chatbot")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    inputs = {"messages": [("human", prompt)]}

    for chunk in graph.stream(inputs, stream_mode="values"):
        # Print all stream values
        # chunk["messages"][-1].pretty_print()
        final_result = chunk

    response = final_result["messages"][-1].content
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.chat_message("assistant").write(response)

    # Queries:
    #
    # Book me a room on 2024-10-31 in the Lisbon office
    # How many people will be in the Lisbon office on 2024-10-31
    # what's the weather in sf
    # what's the weather in nyc
