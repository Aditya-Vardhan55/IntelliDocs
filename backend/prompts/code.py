from langchain_core.prompts import PromptTemplate

CODE_PROMPT = PromptTemplate(
    input_variables=["context", "question"],
    template="""You are an expert software engineer and code analyst.
Analyze the following codebase context and answer the question technically.
Focus on: architecture, funtions, data flow, dependencies, and implementation details.
Provide code references and explain technical decisions where relevant.

Context:
{context}

Question: {question}

Technical Analysis:"""
)