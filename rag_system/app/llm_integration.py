from app import anthropic_llm
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from app.embeddings import load_faiss_index


def create_conversation_chain(vectored_data, prompt_template):
    qa = RetrievalQA.from_chain_type(
        llm=anthropic_llm,
        chain_type="stuff",
        retriever=vectored_data.as_retriever(
                search_type="similarity", search_kwargs={"k": 6}
        ),
        return_source_documents=True,
        chain_type_kwargs={"prompt": prompt_template},
    )

    return qa

def create_prompt_template():
    prompt_template = """
    Human: You are a Teaching Assistant that provides concise answers to the questions related to the text context given to you. Strictly answer the questions related to the following information 
    <context>
    {context}
    </context>
    to answer in a helpful manner. If you don't know the answer, just say that you don't know, don't try to make up an answer.

    Question: {question}

    Teaching Assistant:"""

    prompt = PromptTemplate(
        input_variables=["context", "question"], template=prompt_template
    )

    return prompt

def ask_llm(query):
    context = load_faiss_index(index_folder='models', index_name='faiss_index')
    prompt_template = create_prompt_template()
    conversation_chain = create_conversation_chain(context, prompt_template)
    response = conversation_chain.invoke({'query': query})

    return response['result']