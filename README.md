# Booking AI Agent - A proof of concept

This is a web application that uses LangChain🦜🔗 and Streamio to create a chatbot to work as your personal assistant.
This is just a proof of concept to explore what can be done already with AI Agents.

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

Install dependencies

```bash
pipenv install
```

Start the Streamio server

```bash
pipenv shell
streamlit run chatbot.py
```

Start the FastAPI service

```bash
uvicorn api:app
```

## 🔗 Links

[![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/antpinto/)
[![twitter](https://img.shields.io/badge/twitter-1DA1F2?style=for-the-badge&logo=twitter&logoColor=white)](https://x.com/antonspinto)
