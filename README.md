# Booking AI Agent - A proof of concept

This is a web application that uses LangChain🦜🔗 and Streamlit to create a chatbot to work as your personal assistant.
This is just a proof of concept to explore AI Agents. In this case the agent knows how to book a desk for you in your
office.

## Environment Variables

To run this project, you will need to add the following environment variable to your .env file

`GOOGLE_API_KEY`

## Run Locally

Clone the project

```bash
git clone https://github.com/antonpinto/booking-ai-agent.git
```

Go to the project directory

```bash
cd booking-ai-agent
```

Install dependencies and activate this project's virtualenv

```bash
pipenv install
pipenv shell
```

Start the FastAPI service and Streamlit app

```bash
uvicorn api:app
streamlit run chatbot.py
```

Now interact with the chatbot app in your browser

```bash
http://localhost:8501
```

## 🔗 Links

[![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/antpinto/)
[![twitter](https://img.shields.io/badge/twitter-1DA1F2?style=for-the-badge&logo=twitter&logoColor=white)](https://x.com/antonspinto)
