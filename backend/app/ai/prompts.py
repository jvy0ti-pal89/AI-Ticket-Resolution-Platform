from typing import List, Optional


def build_ticket_prompt(
    title: str, description: str, chunks: Optional[List[str]] = None
) -> str:
    """Build a prompt asking the LLM to return a grounded ticket enrichment JSON."""
    context = "\n\n".join(chunks) if chunks else "No relevant context available."

    prompt = (
        "You are an assistant that classifies support tickets and proposes a grounded resolution.\n"
        "Given the ticket title, description, and relevant company knowledge, return a JSON object with these exact keys:\n"
        "  - category: a short category label (e.g. Hardware, Software, Network, Account, Billing, General)\n"
        "  - priority: one of Critical, High, Medium, Low\n"
        "  - summary: a single concise sentence summarizing the issue\n"
        "  - resolution: a practical, grounded resolution recommendation based on the provided context\n\n"
        "Output MUST be valid JSON and NOTHING but the JSON object.\n\n"
        f"Title: {title}\n\n"
        f"Description: {description}\n\n"
        f"Context:\n{context}\n\n"
        "If the context is unavailable, still provide a helpful resolution based on the ticket details.\n"
        "Use the context where possible to make the resolution grounded in existing documentation or policies.\n"
    )

    return prompt
