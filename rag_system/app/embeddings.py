from app import bedrock_embeddings
from langchain_community.vectorstores import FAISS

def create_embeddings(text_chunks):
    """Creates embeddings for a list of text chunks."""
    vectorstore_faiss = FAISS.from_documents(
        documents=text_chunks,
        embedding=bedrock_embeddings,
    )

    return vectorstore_faiss

def load_faiss_index(index_folder, index_name):
    """
    Searches the FAISS index for the top k relevant results.
    """
    vectored_data = FAISS.load_local(index_folder, bedrock_embeddings, index_name=index_name,
                                     allow_dangerous_deserialization=True)

    return vectored_data