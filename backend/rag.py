from pydantic_ai import Agent
from .data_models import RagResponse
import lancedb
from .constants import VECTOR_DB_PATH


vector_db = lancedb.connect(uri=VECTOR_DB_PATH)

rag_agent = Agent(
    model="google-gla:gemini-2.0-flash",
    retries=3,
    system_prompt=(
        "You are an expert Data Engineering.",
        "Answer based on the retrieved knowledge, but you can mixed in your own experies for more coherent.",
        "Don't hallucinate, rather say you can't answer if user prompts outside the retrieved knowledge.",
        "Be clear and concise with the answer, getting to the point directley, max 7 sentences",
        "Be educational but the answer with steps where the user should begin, and use emojis to keep i more interesting",
        "If the user asks about this chat itself (for exemple what did i ask first).",
        "Then ignore the documents and instead used the conversation history to answer."
        
    ),
    output_type=RagResponse,
)


@rag_agent.tool_plain
def retrieve_top_document(query: str, top_result = 3) -> str:
    """Vector search to find the closest match of txt file to use as context to the query"""
    
    result = vector_db["transcript"].search(query= query).limit(top_result).to_list()
    
    if not result:
        return "No_result: No document was found in the vector database" 
    
    return f"""
    Filename: {result[0]["filename"]},
    Filepath: {result[0]["filepath"]},
    Content: {result[0]["content"]}
    """
    

