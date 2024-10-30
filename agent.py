from datetime import datetime
from dotenv import load_dotenv
from langgraph.prebuilt import create_react_agent
from langchain_google_genai import ChatGoogleGenerativeAI


def office_occupation(location: str, date: str) -> str:
    """Returns how many people are in the office"""
    return f"There will be 2 people in the {location} office on {date}"


def book_room(location: str, date: str) -> str:
    """Books a room on [date] in the [location]"""
    return f"Room 1 booked at the {location} office on {date} for 2 people"


if __name__ == '__main__':
    load_dotenv()

    # Book a room on 2024-10-31 in the Lisbon office
    # How many people will be in the Lisbon office on 2024-10-31
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
