from backend.constants import DATA_PATH
from markdown import markdown
from bs4 import BeautifulSoup


def convert_md_text(path_md):
    
    with open(path_md, "r", encoding= "utf-8") as file:
        md_text = file.read()
        
        html = markdown(md_text)
        soup = BeautifulSoup(html, "html.parser")
        
        return soup.get_text()
         
         
def export_text_to_txt(text, path_file):
    
    with open(path_file, "w", encoding= "utf-8") as f:
        f.write(text)

if __name__=="__main__":
    for md_path in DATA_PATH.glob("*.md"):
        md_text =  convert_md_text(md_path)
        
        filename = f"{md_path.stem.casefold()}.txt"
        
        export_text_to_txt(text= md_text, path_file= DATA_PATH/filename)