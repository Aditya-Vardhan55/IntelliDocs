from langchain_core.prompts import PromptTemplate

MEDICAL_PROMPT = PromptTemplate(
    input_variables=["context", "question"],
    template="""You are an expert medical research analyst.
Analyze the following medical document context and answer the question accurately.
Focus on: methodology, findings, sample sizes, conclusions, and clinical implications.
Always cite specific data points or statistics when available.

Context:
{context}

Question: {question}

Medical Analysis:"""
)