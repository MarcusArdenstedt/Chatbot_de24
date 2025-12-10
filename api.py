from fastapi import FastAPI
from backend.data_models import Prompt
from backend.rag import rag_agent

app = FastAPI()

last_result = None

session = []

@app.post("/rag/query")
async def query_youtubescript(query:Prompt):
    global last_result
    
    messages_history = last_result.all_messages() if last_result else None
    
    result =await rag_agent.run(query.prompt, message_history= messages_history)

    last_result = result
    return {"answer": result.output.answer}
    

@app.post("/rag/history")
async def create_history(query:Prompt):
    
    session.append(query.history)
    
    return session

# @app.get("rag/history/{id}")
# async def get_session(session_id: int) -> Prompt:
#     if session_id < len(session):
#         return session[session_id]
#     else:
#         raise HTTPException(status_code= 404, detail= f"Item {session_id} not found")
        
    
    
    