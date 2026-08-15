from typing import List, Dict, Optional
import os
import json
import re
from groq import Groq

from app.ai.prompts import build_ticket_prompt
from app.config import settings


def _call_groq_api(prompt: str) -> Optional[str]:
    """Call Groq API using the official client."""
    api_key = getattr(settings, "groq_api_key", None) or os.getenv("GROQ_API_KEY")
    if not api_key:
        return None

    try:
        client = Groq(api_key=api_key)
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",  # or "llama3-8b-8192"
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful IT support assistant. Output ONLY valid JSON.",
                },
                {"role": "user", "content": prompt},
            ],
            response_format={"type": "json_object"},
            temperature=0.2,
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Groq API call failed: {e}")
        return None


def _parse_json_response(raw: str) -> Optional[Dict[str, str]]:
    """Parse JSON directly or extract it using regex if wrapped in markdown/extra text."""
    try:
        parsed = json.loads(raw)
        if isinstance(parsed, dict):
            return parsed
    except Exception:
        pass

    try:
        match = re.search(r"\{.*\}", raw, flags=re.S)
        if match:
            parsed = json.loads(match.group(0))
            if isinstance(parsed, dict):
                return parsed
    except Exception:
        pass

    return None


def generate_structured_response(
    title: str, description: str, chunks: List[str]
) -> Dict[str, str]:
    """Return a dict: {category, priority, summary, resolution} grounded in retrieved chunks."""
    prompt = build_ticket_prompt(title, description, chunks)

    # 1. Try Groq API call
    raw = _call_groq_api(prompt)
    if raw:
        parsed = _parse_json_response(raw)
        if parsed and "resolution" in parsed:
            return {
                "category": parsed.get("category", "General"),
                "priority": parsed.get("priority", "Medium"),
                "summary": parsed.get("summary", title),
                "resolution": parsed.get("resolution", ""),
            }

    # 2. Fallback heuristic (only used if Groq API fails)
    text = f"{title} {description}".lower()

    # Category heuristic
    category = "General"
    if any(
        k in text
        for k in ["laptop", "battery", "overheat", "screen", "keyboard", "hardware"]
    ):
        category = "Hardware"
    elif any(
        k in text
        for k in ["error", "exception", "crash", "bug", "stack trace", "traceback"]
    ):
        category = "Software"
    elif any(k in text for k in ["network", "wifi", "vpn", "internet", "latency"]):
        category = "Network"

    # Priority heuristic
    priority = "Medium"
    if any(k in text for k in ["urgent", "immediately", "down", "critical"]):
        priority = "Critical"
    elif any(k in text for k in ["error", "failed", "not working", "cannot", "unable"]):
        priority = "High"

    summary = title.strip() or (description.split(".")[0] + ".").strip()

    # Dynamic resolution fallback using actual chunk text instead of static text
    if chunks:
        context_preview = "\n".join(chunks[:2]).strip()
        resolution = (
            f"Recommended resolution based on knowledge base:\n{context_preview}"
        )
    else:
        resolution = (
            "No relevant knowledge-base context found. Please investigate the issue "
            "and follow standard IT support procedures."
        )

    return {
        "category": category,
        "priority": priority,
        "summary": summary,
        "resolution": resolution,
    }
