import lancedb 
from backend.constants import DATA_PATH, VECTOR_DB_PATH
from backend.data_models import TranScript
from pathlib import Path
import time 

def setup_vector_db(path):
    
    # Create a vector database if not exists
    Path(VECTOR_DB_PATH).mkdir(exist_ok=True)
    
    vector_db = lancedb.connect(uri=path)
    vector_db.create_table("transcript", schema=TranScript, exist_ok=True)
    
    return vector_db
    
    
def ingested_txt_to_vector_db(table_name):
    
    for filepath in DATA_PATH.glob("*.txt"):
        with open(filepath, "r", encoding= "utf-8") as f:
            content = f.read()
            

        doc_id = filepath.stem 
        table_name.delete(f"doc_id = '{doc_id}'")
    
        table_name.add([
           {
               "doc_id": doc_id,
               "filepath": str(filepath),
               "filename": filepath.stem,
               "content": content,
           }
       ])
        
        print(table_name.to_pandas()["filename"])
        time.sleep(20)

    
    
if __name__=="__main__":
    
    
    vector_db = setup_vector_db(VECTOR_DB_PATH)
    ingested_txt_to_vector_db(vector_db["transcript"])
    