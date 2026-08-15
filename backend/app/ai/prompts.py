from typing import List, Optional


def build_ticket_prompt(
    title: str, description: str, chunks: Optional[List[str]] = None
) -> str:
    """Prompt for automated ticket classification and grounded resolution enrichment."""
    context = "\n\n".join(chunks) if chunks else "No relevant context available."

    prompt = (
        "You are an enterprise IT support assistant that classifies support tickets "
        "and proposes grounded resolutions.\n\n"
        "Given the ticket title, description, and relevant company knowledge, "
        "return a JSON object with these exact keys:\n"
        "- category: a short category label such as Hardware, Software, Network, "
        "Account, Billing, or General\n"
        "- priority: one of Critical, High, Medium, Low\n"
        "- summary: a single concise sentence summarizing the issue\n"
        "- resolution: a practical resolution recommendation grounded in the "
        "provided knowledge-base context\n\n"
        "IMPORTANT RULES:\n"
        "1. Use the provided context whenever relevant.\n"
        "2. Do not invent company-specific policies, procedures, or troubleshooting steps.\n"
        "3. If the context does not contain relevant information, clearly state that "
        "no relevant knowledge-base information was found.\n"
        "4. The response must be valid JSON.\n"
        "5. Output ONLY the JSON object. Do not include markdown or explanations outside JSON.\n\n"
        f"Title: {title}\n\n"
        f"Description: {description}\n\n"
        f"Knowledge Base Context:\n{context}\n"
    )

    return prompt


def build_rag_question_prompt(question: str, chunks: Optional[List[str]] = None) -> str:
    """Prompt for standalone Document Q&A (Ask AI feature in Knowledge Base)."""
    context = "\n\n---\n\n".join(chunks) if chunks else "No relevant context available."

    prompt = (
        "You are an enterprise IT knowledge-base assistant.\n\n"
        "Answer the user's question using ONLY the provided knowledge-base context.\n\n"
        "Rules:\n"
        "1. Do not invent information or use outside knowledge.\n"
        "2. If the answer is not present in the context, say 'I could not find this information in the knowledge base.'\n"
        "3. Keep the answer clear, practical, and concise.\n\n"
        f"Knowledge Base Context:\n{context}\n\n"
        f"User Question:\n{question}\n"
    )

    return prompt
