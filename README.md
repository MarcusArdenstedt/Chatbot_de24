# Chatbot for Data Engineer
> This project is a chatbot design to answer question based on transcript from teachers YOUTUBE lectures in Data Engineer education program.

## Purpose of this project
- Using Pydantic to understand data validation and parsing. 
- Using FastAPI to build a web framework for creating API:s in Python.
- Using PydanticAI to build LLM-powered interaction and gain a basic understanding of how they work.
- Using Lancedb for creating vector database and learning about embeddings.
- Azure function apps is the bridge between backend and frontend.
- Terraform to create infrastructer code in Azure.
- Using Docker to build container image and push them to Azure.
- Using Azure to deploy and host the application.

## Features 
- Get answer on the content for Data Engineer education program.
- Create a chat session with the bot
- Retrieve chat history for a session


## Source
The transcript for this YouTube lecture are stored in this repository under the data directory. 
You can browse them here: https://github.com/MarcusArdenstedt/Chatbot_de24/tree/main/data 


## Installation

**This project uses uv for environment and package management**

1. Start by initialising uv in your project folder:
   
   Terminalen
   ```
   uv init
   ```
  
2. Add the required dependencies:
   
   Terminalen
   ```
   uv add pydantic ipykernel pydantic-ai google-generativeai lancedb fastapi beautifulsoup4 markdown python-dotenv pandas uvicorn streamlit
   ````

3. In pyproject.toml add:
   ```
   [build-system]
   requires = ["setuptools >= 68", "wheel"]
   build-backend = "setuptools.build_meta"

   [tool.setuptools.packages.find]
   where = ["."]
   ```
This will make it possible to build and distribute package in the project.

# Step to execute the project

## Create and ingest data to a vector database

- Create a constants file under backend. Here create path to data and knowledge_base: https://github.com/MarcusArdenstedt/Chatbot_de24/blob/main/backend/constants.py
  
- Convert transcript from markdown file to text-file. Here's exemple: https://github.com/MarcusArdenstedt/Chatbot_de24/blob/main/backend/md_to_text.py
  
- Before ingest the text-file to knowledge_base you need to have embedding the text that ingest and defining table schema. An enbedding is a numeric vector tha capture the sematic meaning of the transcript and makes it possible for the agent to do vector search.

<image src = "assets/embedding_defining.png">
- Ingestion the text-file to a vector database. Here's exemple: https://github.com/MarcusArdenstedt/Chatbot_de24/blob/main/backend/ingestion.py 

## Testing Fast API with Swagger UI
- Creating a RAG Agent with pydantic AI. Tool_plain decorator perform a vector search in lancedb for the user query and return top matching content to the agent.
https://github.com/MarcusArdenstedt/Chatbot_de24/blob/main/backend/rag.py
  
- In the api.py create a fast API endpoint to call to RAG-agent, code exemple: <image src = "assets/post_endpoint.png">
Initialize app with FastAPI(), then decorate it with GET-endpoint. async and await is just to make that computer dosen't need to wait for this function to be finish so the computer jumping back and forth until this is finish. Here you send in the prompt to RAG-agent and it will return the output. 

- Testing in swagger
  
  Terminal
  ```
    uv run uvicorn api:app --reload
    ```

http://127.0.0.1:8000/docs in browser url and this is what will:
<image src = "assets/swagger_ui.png">

And string is the prompt.

## Function apps

- Install [Azure Functions Core Tools](https://learn.microsoft.com/en-us/azure/azure-functions/functions-run-local?tabs=macos%2Cisolated-process%2Cnode-v4%2Cpython-v2%2Chttp-trigger%2Ccontainer-apps&pivots=programming-language-csharp) on your computer

- In extension install Azure Functions
  <image src = "assets/azure_function_extension.png">

- sign in with your azure subscription 
- click on workspace and create a local project
<image src = "assets/workspace.png">
- Added this in your host.json
  ```
    "extensions": {
    "http": {
        "routePrefix": ""
    }
    ```
- change the function_app.py to:
  ```
  import azure.functions as func
  import api

  app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

  @app.route(route="{*route}", methods= ["GET", "POST", "PUT", "DELETE", "OPTIONS"])
  async def fastapi_proxy(
    req: func.HttpRequest, context: func.Context
  ) -> func.HttpResponse:
    return await func.AsgiMiddleware(api.app).handle_async(req, context)
    ```
- change the url in frontend/app.py, so it linked to azuer function
- Deploy it to azure function.

## Create web app 
- Create resources container-registry, web-app-plan and web-app-server in the same resource group as function apps.
- create a image for frontend and push it to Azure container registry
- In Azure web-app create a environment variable with the same name you will have in frontend os.getenv(same-name)
<image src = "assets/url.png">


<image src = "assets/request_post.png">

- Now it linked to function apps.
