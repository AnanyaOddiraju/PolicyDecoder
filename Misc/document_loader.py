from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader,TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import tempfile
import os

def load_split_document(file):
    #save uploaded file temporarily
    ftype = os.path.splitext(file.name)[1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=ftype) as tmp:
        tmp.write(file.read())
        tmp_path= tmp.name
    
    #load document based on file type
    if ftype =='pdf':
        loader = PyPDFLoader(tmp_path)
    elif ftype in ['.docx','.doc']:
        loader = Docx2txtLoader(tmp_path)
    elif ftype in ['.txt','.md']:
        loader = TextLoader(tmp_path)
    else:
        raise ValueError("Unsupported file type : {ftype}")
    
    documents = loader.load()
    os.unlink(tmp_path) #delete temp file

    #split the document into chunks
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(documents)
    return chunks