from langchain_community.document_loaders import PyPDFLoader , DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
import os 


DATA_PATH = "data/"
CHROMA_PATH = "chroma_db"

#-----------------------------Loading the file-----------------------------

def load_pdf_file(data):
    loader = DirectoryLoader(path = data , glob="*.pdf" , loader_cls=PyPDFLoader , show_progress=True)
    documents = loader.load()
    return documents


#-----------------------------Chunking the file-----------------------------

def create_chunks(document):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 500 , 
        chunk_overlap = 50
    ) 
    chunks = text_splitter.split_documents(document)
    return chunks 


#-----------------------------Embeddings Model-----------------------------

def get_embedding_model():
    embeggings = HuggingFaceEmbeddings(
        model_name = "sentence-transformers/all-MiniLM-L6-v2"
    )
    return embeggings


#-----------------------------Chroma Database-----------------------------

def store_into_chroma_db(chunks):
    embeddings = get_embedding_model()
    db = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_PATH
    )
    db.persist()
    print("Data Stored Successfully.")


#-----------------------------Final Calling-----------------------------

def fetch_and_store_pdf():
    if os.path.exists(CHROMA_PATH):
        print("Database already there")
        return 
    documents = load_pdf_file(data=DATA_PATH)
    chunks = create_chunks(document=documents)
    print(f"Total Number of Chunks :- {len(chunks)}")
    store_into_chroma_db(chunks=chunks)


fetch_and_store_pdf()