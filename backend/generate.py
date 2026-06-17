from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from .llm import get_llm


# Prompt template
RAG_PROMPT = ChatPromptTemplate.from_template("""
You are a helpful assistant for answering questions based on provided context.
Use only the information in the context to answer the question. 
If you don't know the answer, say a helpful message.

CONTEXT:
{context}

QUESTION:
{question}

ANSWER:
""")


def generate(question, chunks):
    llm = get_llm()

    # Build chain
    chain = RAG_PROMPT | llm | StrOutputParser()

    # Format context from chunks
    context = "\n\n---\n\n".join([c["text"] for c in chunks])

    # Run
    answer = chain.invoke({
        "context": context,
        "question": question
    })

    return answer