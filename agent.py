from datetime import datetime
from dotenv import load_dotenv
from langgraph.prebuilt import create_react_agent
from langchain_google_genai import ChatGoogleGenerativeAI


def office_occupation(location: str) -> str:
    """Returns how many people are in the office"""
    return f"Theres are 2 people in the {location} office"


def book_room(location: str) -> str:
    """Books a room in the office"""
    return f"Room 1 booked at the {location} office for 2 people"


if __name__ == '__main__':
    load_dotenv()

    # Book a room in the Lisbon office
    # How many people are in the Lisbon office
    # bye

    tools = [book_room, office_occupation]
    model = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
    graph = create_react_agent(model, tools=tools)

    while True:
        query = input('Query: ')
        if query == 'bye':
            break
        inputs = {"messages": [("user", query)]}
        for s in graph.stream(inputs, stream_mode="values"):
            message = s["messages"][-1]
            if isinstance(message, tuple):
                print(message)
            else:
                message.pretty_print()
