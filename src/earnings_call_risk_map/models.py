"""Shared constants and lightweight helpers."""

from __future__ import annotations

SAFETY_NOTICE = (
    "Educational research review only. This tool does not provide personalized "
    "investment, legal, accounting, tax, buy, sell, or hold advice. Verify "
    "source materials and note that stale/static data may no longer reflect "
    "current conditions."
)

SOURCE_BOUNDARIES = {
    "management_claims": "source-provided company statements or prepared remarks; verify against filings and transcripts",
    "analyst_questions": "source-provided questions or prompts; they are not treated as factual claims",
    "user_synthesis": "user-authored notes, tags, and deterministic tool scores; review prompts, not advice",
}

RISK_KEYWORDS = {
    "decline": 3,
    "delay": 2,
    "delayed": 2,
    "headwind": 2,
    "risk": 2,
    "weak": 2,
    "weakness": 2,
    "pressure": 2,
    "margin compression": 4,
    "churn": 3,
    "regulatory": 3,
    "investigation": 4,
    "supply": 2,
    "guidance cut": 5,
    "miss": 3,
}

OPPORTUNITY_KEYWORDS = {
    "growth": 3,
    "accelerate": 3,
    "accelerated": 3,
    "tailwind": 2,
    "opportunity": 2,
    "record": 2,
    "expand": 2,
    "expansion": 2,
    "margin improvement": 4,
    "beat": 3,
    "raised guidance": 5,
    "pipeline": 2,
    "launch": 2,
}

REQUIRED_TOP_LEVEL = ("company", "ticker", "as_of", "data_cutoff")
