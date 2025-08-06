import os
from dotenv import load_dotenv
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from langchain.chains import RetrievalQA

# ✅ LangChain 0.2+ compatible imports
from langchain_community.llms import OpenAI
from langchain_openai.embeddings import OpenAIEmbeddings

# ✅ Load .env file for API key
load_dotenv()


def load_documents_from_txt_folder(folder_path: str) -> list:
    """
    Load all .txt files from a folder into LangChain Document objects.

    Args:
        folder_path (str): Path to the folder containing plain text files.

    Returns:
        list: A list of LangChain Document objects.
    """
    documents = []
    for fname in os.listdir(folder_path):
        if fname.endswith(".txt"):
            with open(os.path.join(folder_path, fname), "r", encoding="utf-8") as f:
                text = f.read()
                documents.append(Document(page_content=text))
    return documents


def build_vector_store(documents: list, persist_path: str = "rag/knowledge_base") -> FAISS:
    """
    Build and persist a FAISS vector store from documents.

    Args:
        documents (list): A list of LangChain Document objects.
        persist_path (str): Directory to save the FAISS index.

    Returns:
        FAISS: A LangChain FAISS vector store object.
    """
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(documents)

    embeddings = OpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY"))
    db = FAISS.from_documents(chunks, embedding=embeddings)
    db.save_local(persist_path)

    return db


def load_vector_store(persist_path: str = "rag/knowledge_base") -> FAISS:
    """
    Load a FAISS vector store from disk.

    Args:
        persist_path (str): Directory where the FAISS index is stored.

    Returns:
        FAISS: A loaded FAISS vector store object.
    """
    embeddings = OpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY"))
    #return FAISS.load_local(persist_path, embeddings)
    return FAISS.load_local(
        persist_path,
        embeddings,
        allow_dangerous_deserialization=True  # ✅ You own the data, safe for dev/test
    )


def create_qa_chain(retriever: FAISS) -> RetrievalQA:
    """
    Create a LangChain RetrievalQA pipeline using a retriever and OpenAI LLM.

    Args:
        retriever (FAISS): A FAISS retriever object.

    Returns:
        RetrievalQA: A LangChain RetrievalQA pipeline for Q&A.
    """
    llm = OpenAI(temperature=0, api_key=os.getenv("OPENAI_API_KEY"))
    chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
    return chain


def load_knowledge_base(persist_path: str = "rag/knowledge_base") -> RetrievalQA:
    """
    Load the QA chain from a persisted FAISS vector store.

    Args:
        persist_path (str): Path to the FAISS index.

    Returns:
        RetrievalQA: A ready-to-use question answering chain.
    """
    retriever = load_vector_store(persist_path).as_retriever()
    return create_qa_chain(retriever)
