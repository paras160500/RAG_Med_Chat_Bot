from langchain_huggingface import HuggingFaceEndpoint
from langchain_core.prompts import ChatPromptTemplate
from langchain_chroma import Chroma
from pdf_ingestion import get_embedding_model , CHROMA_PATH
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import Runnable , RunnablePassthrough
from langchain_mistralai import ChatMistralAI
from dotenv import load_dotenv
import os 

load_dotenv()

CHROMA_PATH = CHROMA_PATH


#-----------------------------Embeddings model-----------------------------

def get_embeddings():
    return get_embedding_model()


#-----------------------------Embeddings model-----------------------------

def load_vector_db():
    embeddings = get_embeddings()
    db = Chroma(
        embedding_function=embeddings,
        persist_directory=CHROMA_PATH
    )
    return db 


#-----------------------------Retriver-----------------------------

def get_retriver():
    db = load_vector_db()
    retriver = db.as_retriever(
        search_type = "similarity",
        search_kwargs = {"k" : 3}
    )
    return retriver


#-----------------------------Loading llm-----------------------------

def load_llm():
    llm = ChatMistralAI(
        model_name="mistral-small-2506",
        api_key=os.getenv("MISTRAL_API_KEY"),
        temperature=0.3,
        max_tokens=512
    )
    return llm 


#-----------------------------Prompt Template-----------------------------

def get_prompt():
    prompt = ChatPromptTemplate.from_messages([
        ('system' , """
            You are a helpful AI assistant.
            Answer ONLY from the provided context.
            If the context does not contain the answer,
            say "I don't know from the provided documents.")""") , 
        ('human' ,  """
            Context:
            {context}

            Question:
            {question}
            """)
    ])
    return prompt


#-----------------------------Format Docs-----------------------------

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


#-----------------------------RAG Chain-----------------------------

def create_rag_chain():
    retriver = get_retriver()
    prompt = get_prompt()
    llm = load_llm()
    output_parser = StrOutputParser()

    chain = (
        {
            "context" : retriver | format_docs ,
            "question" : RunnablePassthrough()
        } 
        | prompt | llm | output_parser
    )

    return chain 

chain = create_rag_chain()

print(chain.invoke("What is Coagulation disorders? and which medicine i have to take?"))