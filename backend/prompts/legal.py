from langchain_core.prompts import PromptTemplate

LEGAL_PROMPT = PromptTemplate(
    input_variables=["context", "question"],
    template="""You are an expet legal document analyst.
Analyze the following legal document context and answer the question precisely.
Focus on: clauses, obligations, rights, termination conditions, and legal implications.
Always mention relevant section numbers or clause references if present.

Context:
{context}

Question: {question}

Legal Analysis:"""
)