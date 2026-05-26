import time
import structlog
from langchain_ollama import OllamaLLM
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_classic.chains.retrieval_qa.base import RetrievalQA
from langchain_classic.schema import Document

from backend.services.embeddings import get_embedding_model
from backend.services.domain_router import detect_domain, Domain
from backend.prompts.legal import LEGAL_PROMPT
from backend.prompts.medical import MEDICAL_PROMPT
from backend.prompts.corporate import CORPORATE_PROMPT
from backend.prompts.code import CODE_PROMPT
from backend.config import get_settings
from mlops.mlflow_tracker import log_document_processing, log_query

logger = structlog.get_logger()
settings = get_settings()

PROMPT_MAP = {
    Domain.LEGAL: LEGAL_PROMPT,
    Domain.MEDICAL: MEDICAL_PROMPT,
    Domain.CORPORATE: CORPORATE_PROMPT,
    Domain.CODE: CODE_PROMPT,
    Domain.UNKNOWN: CORPORATE_PROMPT    # fallback
}

# Domain -> chunk strategy mapping
# This is what we'll track in MLflow later
CHUNK_STRATEGY = {
    Domain.LEGAL: {"chunk_size": 1000, "chunk_overlap": 200},
    Domain.MEDICAL: {"chunk_size": 800, "chunk_overlap": 150},
    Domain.CORPORATE: {"chunk_size": 600, "chunk_overlap": 100},
    Domain.CODE: {"chunk_size": 400, "chunk_overlap": 50},
    Domain.UNKNOWN: {"chunk_size": 600, "chunk_overlap": 100}
}

def process_document(text: str, filename: str) -> dict:
    """
    Full Pipeline:
    1. Detect domain
    2. Split text with domain-specific chunking
    3. Embed and store in ChromaDB
    Returns metadata about the processed document
    """
    start_time = time.time()
    logger.info("processing_document", filename=filename)
    
    # Step 1 - detect domain
    domain = detect_domain(text)
    logger.info("document_domain", domain=domain, filename=filename)
    
    # Step 2 - chunk with domain strategy
    strategy = CHUNK_STRATEGY[domain]
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=strategy["chunk_size"],
        chunk_overlap=strategy["chunk_overlap"]
    )
    chunks = splitter.split_text(text)
    logger.info("document_chunked",
                num_chunks=len(chunks),
                chunk_size=strategy["chunk_size"],
                filename=filename)
    
    # Step 3 - embed and store
    embeddings = get_embedding_model()
    documents = [
        Document(
            page_content=chunk,
            metadata={
                "filename": filename,
                "domain": domain.value,
                "chunk_index": i
            }
        )
        for i, chunk in enumerate(chunks)
    ]
    
    vectorstore = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=".chromadb",
        collection_name=f"intellidocs_{domain.value}"
    )
    
    processing_time = time.time() - start_time
    
    # Step 4 - log to MLflow
    log_document_processing(
        filename=filename,
        domain=domain.value,
        chunk_size=strategy["chunk_size"],
        chunk_overlap=strategy["chunk_overlap"],
        num_chunks=len(chunks),
        processing_time=processing_time
    )
    
    logger.info("document_stored",
                collection=f"intellidocs_{domain.value}",
                filename=filename)
    
    return {
        "filename": filename,
        "domain": domain.value,
        "num_chunks": len(chunks),
        "chunk_size": strategy["chunk_size"],
        "chunk_overlap": strategy["chunk_overlap"],
        "processing_time_seconds": round(processing_time, 3)
    }
    
def query_document(question: str, domain_str: str) -> dict:
    """
    Query the vectorstore and return an answer
    using the domain-specific prompt template
    """
    start_time = time.time()
    logger.info("querying_document", question=question, domain=domain_str)
    
    domain = Domain(domain_str)
    embeddings = get_embedding_model()
    
    vectorstore = Chroma(
        persist_directory=".chromadb",
        embedding_function=embeddings,
        collection_name=f"intellidocs_{domain.value}"
    )
    
    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})
    
    llm = OllamaLLM(
        base_url=settings.ollama_base_url,
        model=settings.ollama_model
    )
    
    prompt = PROMPT_MAP[domain]
    
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        chain_type_kwargs={"prompt": prompt},
        return_source_documents=True
    )
    
    result = qa_chain.invoke({"query": question})
    response_time = time.time() - start_time
    
    # Log query metrics to MLflow
    log_query(
        question=question,
        domain=domain_str,
        response_time=response_time,
        num_source_chunks=len(result["source_documents"])
    )
    
    logger.info("query_complete",
                question=question,
                domain=domain_str,
                num_source_docs=len(result["source_documents"]))
    
    return {
        "answer": result["result"],
        "domain": domain_str,
        "source_chunks": len(result["source_documents"]),
        "response_time_seconds": round(response_time, 3)
    }