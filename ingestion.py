import lancedb 
from backend.constants import DATA_PATH, VECTOR_DB_PATH
from backend.data_models import YoutubeScript
from pathlib import Path

def setup_vector_db(path):
    
    
    # Create a vector database if not exists
    Path(VECTOR_DB_PATH).mkdir(exist_ok=True)
    
    vector_db = lancedb.connect(uri=path)
    vector_db.create_table("youtubescript", schema=YoutubeScript, exist_ok=True)
    
    return vector_db
    
    
    
    
if __name__=="__main__":
    
    vector_db = setup_vector_db(VECTOR_DB_PATH)
    