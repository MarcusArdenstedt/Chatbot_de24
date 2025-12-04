from pydantic import BaseModel, Field
from lancedb.embeddings import get_registry
from lancedb.pydantic import LanceModel, Vector
from dotenv import load_dotenv

load_dotenv()

embedding_model = get_registry().get("gemini-text").create(name= "gemini-embedding-001")

EMBEDDINNG_DIM = 3072


class YoutubeScript(LanceModel):
    doc_id: str
    filepath: str 
    filename: str = Field(description="the stem of the file, i. e without the suffix ")
    content: str = embedding_model.SourceField()
    embedding: Vector(EMBEDDINNG_DIM) = embedding_model.VectorField()
    
