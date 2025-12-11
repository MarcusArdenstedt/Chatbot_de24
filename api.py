from fastapi import FastAPI, HTTPException
from backend.data_models import Prompt, YoutubeDescription
from backend.rag import rag_agent
from backend.ingestion import open_vector_database
from typing import List

app = FastAPI()

def get_transcript_content(doc_id):
    table = open_vector_database()
    df = table.to_pandas()
        
    records: List[dict] = df.to_dict(orient= "records")

    for r in records:
        if r["doc_id"] == doc_id:
            r.pop("embedding", None)
            return r["content"]

    raise HTTPException(status_code=404, detail= "Transcript do not exists")

last_result = None

session: list[dict] = []

@app.post("/rag/query")
async def query_youtubetranscript(query: Prompt):
    global last_result

    messages_history = last_result.all_messages() if last_result else None

    result = await rag_agent.run(query.prompt, message_history=messages_history)

    last_result = result

    session.append({"role": "user", "content": query.prompt})
    session.append({"role": "assistant", "content": result.output.answer})

    return {"answer": result.output.answer}


@app.get("/rag/history")
async def get_session() -> list[dict]:

    return session



@app.get("/rag/{doc_id}/description")
async def summary_content(doc_id: str):
  transcript_text = get_transcript_content(doc_id)
  
  prompt = (f"Write a summary for the {transcript_text}.",
            "Keep it short and interesting, 2-4 sentences.",
            )
  
  result = await rag_agent.run(prompt)
  
  return YoutubeDescription(
      doc_id= doc_id,
      description= result.output.answer
      )
  
