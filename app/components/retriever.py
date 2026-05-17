from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

from app.components.llm import load_llm
from app.components.vector_store import load_vector_store

from app.common.logger import get_logger
from app.common.custom_exception import CustomException
from app.config.config import RETRIEVER_K

logger = get_logger(__name__)

CUSTOM_PROMPT_TEMPLATE = """
You are a medical question-answering assistant.

Use ONLY the information provided in the context.
If the answer is not present in the context, respond with:
"I don't know based on the provided medical documents."

Do not invent facts.
Do not provide final diagnosis.
Do not prescribe medication.
Encourage users to consult a qualified medical professional for serious conditions.

Keep answers concise, clear, and medically responsible.
Limit your response to 3-5 lines maximum.

Context:
{context}

Question:
{question}

Answer:
"""


def set_custom_prompt():
    return PromptTemplate(
        template=CUSTOM_PROMPT_TEMPLATE,
        input_variables=["context", "question"]
    )


def create_qa_chain():
    try:
        logger.info("Loading vector store for retrieval...")
        db = load_vector_store()

        if db is None:
            raise CustomException("Vector store not present or empty")

        logger.info("Loading Groq LLM...")
        llm = load_llm()

        if llm is None:
            raise CustomException("LLM not loaded")

        prompt = set_custom_prompt()

        retriever = db.as_retriever(
            search_kwargs={"k": RETRIEVER_K}
        )

        qa_chain = (
            {"context": retriever, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
        )

        logger.info("QA chain created successfully")
        return qa_chain

    except Exception as e:
        error_message = CustomException("Failed to create QA chain", e)
        logger.error(str(error_message))
        return None
