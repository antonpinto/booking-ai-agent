from typing import Literal
from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent
import streamlit as st
import requests


# Example prompts:
# ----------------
# Book me a desk on 2025-01-02 in the Lisbon office
# Who will be in the Lisbon office on 2025-01-02
# And how will be the weather like in Lisbon on 2025-01-02


@tool(return_direct=True)
def book_desk(location: str, date: str) -> str:
    """Books a desk in the [location] on [date]"""
    data = {'location': location, 'date': date, 'person': 'Antonio Pinto'}
    print(data)

    res = requests.post('http://localhost:8000/bookings', json=data)
    if res.status_code == 200:
        booking = res.json()
        return f"Desk {booking["desk"]} booked for you in the {booking["location"]} office on {booking["date"]}"
    else:
        return 'An error occurred.'


@tool(return_direct=True)
def get_office_occupation(location: str, date: str) -> str:
    """Returns who will be in the [location] on [date]"""
    res = requests.get(f'http://localhost:8000/requesters/?location={location}&date={date}')
    if res.status_code != 200:
        return 'An error occurred.'

    persons = res.json()
    if type(persons) is not list:
        return 'An error occurred.'

    count = len(persons)
    if count == 0:
        return f"No one will be there"
    elif count == 1:
        return f"One person will be there: {persons[0]}"

    return f"{count} persons will be there: {', '.join(persons)}"


@tool
def get_weather(city: Literal["nyc", "sf", "lisbon"]):
    """Use this to get weather information."""
    if city == "nyc":
        return "It might be cloudy in nyc"
    elif city == "sf":
        return "It's always sunny in sf"
    elif city == "lisbon":
        return "It will be Sunny changing to partly cloudy by nighttime. Most likely maximum day time temperature 22 degrees Celsius and highest possible is 23 degrees"
    else:
        raise AssertionError("Unknown city")


load_dotenv()
tools = [get_weather, book_desk, get_office_occupation]
model = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
graph = create_react_agent(model, tools=tools)

st.title("💬 Personal Assistant Bot")

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
