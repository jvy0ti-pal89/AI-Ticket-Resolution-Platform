from typing import List, Dict, Optional
import os
import json
import re
import urllib.request
import urllib.error

from app.ai.prompts import build_ticket_prompt
from app.config import settings


def _call_groq_api(prompt: str) -> Optional[str]:
    """Attempt to call a Groq-like API if credentials are provided.

    This is defensive: if no API key and endpoint are configured, callers should fallback.
    """
    api_key = settings.groq_api_key or os.getenv("GROQ_API_KEY")
    endpoint = settings.groq_endpoint or os.getenv("GROQ_ENDPOINT")
    if not api_key or not endpoint:
        return None

    url = endpoint.rstrip("/") + "/responses"
    payload = {"input": prompt}
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.read().decode("utf-8")
    except urllib.error.URLError:
        return None


def _parse_json_response(raw: str) -> Optional[Dict[str, str]]:
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
    """Return a dict: {category, priority, summary, resolution}."""
    prompt = build_ticket_prompt(title, description, chunks)

    # Try remote Groq-like API first
    raw = _call_groq_api(prompt)
    if raw:
        parsed = _parse_json_response(raw)
        if parsed:
            return {
                "category": parsed.get("category", "General"),
                "priority": parsed.get("priority", "Medium"),
                "summary": parsed.get("summary", ""),
                "resolution": parsed.get("resolution", ""),
            }

    # Fallback heuristic: keyword matching
    text = f"{title} {description}".lower()
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

    priority = "Medium"
    if any(k in text for k in ["urgent", "immediately", "down", "critical"]):
        priority = "Critical"
    elif any(k in text for k in ["error", "failed", "not working", "cannot", "unable"]):
        priority = "High"

    summary = title.strip() or (description.split(".")[0] + ".").strip()
    resolution = (
        f"Based on the ticket, investigate the issue, verify relevant system state, and follow standard support procedures to resolve it."
        if not chunks
        else f"Review the relevant documentation and apply the recommended steps from the provided context to resolve this issue."
    )

    return {
        "category": category,
        "priority": priority,
        "summary": summary,
        "resolution": resolution,
    }
