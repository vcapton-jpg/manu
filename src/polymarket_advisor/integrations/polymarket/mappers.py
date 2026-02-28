"""Mappers JSON Gamma -> domain/db."""
from __future__ import annotations

import json
from typing import Any

from polymarket_advisor.integrations.polymarket.schemas import MarketEvent, TokenInfo


def event_to_market_row(event: MarketEvent) -> dict:
    """Map Gamma event to market row dict."""
    return {
        "slug": event.get("slug"),
        "question": event.get("title") or event.get("question"),
        "end_date_iso": event.get("endDate") or event.get("end_date_iso"),
        "raw": event,
    }


def _ensure_list(value: Any) -> list:
    """If value is a JSON string representing a list, parse it. If it's already a list, return it."""
    if value is None:
        return []
    if isinstance(value, list):
        return value
    if isinstance(value, str):
        s = value.strip()
        if not s:
            return []
        # If it's JSON encoded list/dict, parse it
        if s[0] in "[{":
            try:
                parsed = json.loads(s)
                if isinstance(parsed, list):
                    return parsed
                # Some APIs may return a dict with a nested list
                if isinstance(parsed, dict):
                    # best-effort: look for common nested arrays
                    for k in ("tokens", "outcomes", "data", "items"):
                        if isinstance(parsed.get(k), list):
                            return parsed[k]
                    return []
            except Exception:
                # Not valid JSON -> treat as a single token name
                return [{"name": value}]
        # Non-JSON string -> treat as single token name
        return [{"name": value}]
    # Unknown type -> ignore
    return []


def token_from_market(market: dict) -> list[TokenInfo]:
    """
    Extract tokens from a Gamma market.

    IMPORTANT:
    - Some Gamma fields are JSON-encoded strings -> we parse them.
    - We keep the raw token dict as-is so we can later extract clobTokenId / tokenId etc.
    """
    tokens_raw = market.get("tokens")
    if tokens_raw is None:
        tokens_raw = market.get("outcomes")

    tokens_list = _ensure_list(tokens_raw)

    out: list[TokenInfo] = []
    for t in tokens_list:
        if isinstance(t, dict):
            out.append(t)
        else:
            out.append({"name": str(t)})
    return out


def token_identifiers(token: dict) -> dict:
    """
    Best-effort extraction of IDs used by different endpoints.
    We'll store ONE "token_id" in DB as the CLOB tradeable id when available.
    """
    # Common names seen across variants:
    # - clobTokenId / clob_token_id
    # - tokenId / token_id
    # - outcomeTokenId
    # - id
    for key in ("clobTokenId", "clob_token_id", "tokenId", "token_id", "outcomeTokenId", "id"):
        val = token.get(key)
        if val is not None and str(val).strip() != "":
            return {"token_id": str(val)}
    return {"token_id": None}