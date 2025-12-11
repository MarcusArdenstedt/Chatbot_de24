# Chatbot for Data Engineer
> This project is a chatbot design to answer question based on transcript from teachers YOUTUBE lectures in Data Engineer education program.

## How to run
- Install uv
- Install dependencies
- Convert data
- Ingest embedding
- Run API
- Run frontend


**Install dependecies**
```
   "azure-functions>=1.24.0",
    "bs4>=0.0.2",
    "fastapi>=0.123.8",
    "google-generativeai>=0.8.5",
    "ipykernel>=7.1.0",
    "lancedb>=0.25.3",
    "markdown>=3.10",
    "pandas>=2.3.3",
    "pydantic>=2.12.5",
    "pydantic-ai>=1.26.0",
    "python-dotenv>=1.2.1",
    "streamlit>=1.52.1",
    "uvicorn>=0.38.0",
```

**Data flow**

Youtube transcript -> markdown convert to text -> Embedding -> Lancedb (Vector database) -> FastAPI RAG-endpoint -> Azure Function Proxy -> Frontend (stremalit)


***Embedding***

Embedding is to defining table schema, enbedding is a numeric vector the capture the sematic meaning of the transcript and makes it possible for agent to do vector search.

<br>

<image src = "assets/embedding_defining.png" width = 300> 

<br>

***Rag Agent***

Create a RAG agent with pydnatic AI. Tool_plain decorater perform a vector search in lancedb for the use query and return top matching content.

<br>

<image src = "assets/rag_agent.png" width = 300>

<br>

<image src = "assets/tool_plain.png" width = 300>


***Pydantic***

Create classe with pydantic to perform datavalidation and dataparsing to secure datastructure.

<br>

<image src = "assets/pydantic.png" width = 300>  

***FastAPI and Azure Functions***

FastAPI defines the API endpoints, and Azure Functions run the application as a HTTP-trigger. With AsgiMiddleware adapt Azure Functions HTTP-request/response to FastAPI:s ASGI-interface, allowing the application to be exposed publicly.

<br>

<image src = "assets/swagger_ui.png" width = 300>

<br>

***Frontend and Azure web app***

- Build the Docker image for the frontend and push it to Azure container registry  
- Update the API URL in streamlit frontend so it points to Azure Functions HTTP endpoin. This allows frontend to communicate with the backend through the Azure Functions HTTP proxy.
  
<br>

<image src = "assets/chatbot_1.png" width = 300>

<br>

<image src = "assets/ask_first_question.png" width = 300>