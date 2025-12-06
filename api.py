from fastapi import FastAPI
from backend.data_models import Prompt
from backend.rag import rag_agent

app = FastAPI()

@app.post("/rag/query")
async def query_yotubescript(query:Prompt):
    result =await rag_agent.run(query.prompt)
    return result.output 
    