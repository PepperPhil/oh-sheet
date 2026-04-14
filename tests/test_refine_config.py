"""Sanity checks on the refine-stage settings surface."""
from __future__ import annotations

from backend.config import Settings


def test_refine_defaults(monkeypatch) -> None:
    # Make the test deterministic regardless of the developer's local .env —
    # BaseSettings auto-reads it, so a dev with a real key configured would
    # see ``anthropic_api_key is None`` fail without ``_env_file=None``.
    monkeypatch.delenv("OHSHEET_ANTHROPIC_API_KEY", raising=False)
    s = Settings(_env_file=None)
    assert s.refine_enabled is True
    assert s.refine_model == "claude-sonnet-4-6"
    assert s.refine_max_searches == 5
    assert s.refine_budget_sec == 300
    assert s.refine_call_timeout_sec == 120
    assert s.anthropic_api_key is None


def test_refine_env_overrides(monkeypatch) -> None:
    monkeypatch.setenv("OHSHEET_REFINE_ENABLED", "false")
    monkeypatch.setenv("OHSHEET_REFINE_MODEL", "claude-haiku-4-5-20251001")
    monkeypatch.setenv("OHSHEET_REFINE_MAX_SEARCHES", "3")
    monkeypatch.setenv("OHSHEET_REFINE_BUDGET_SEC", "600")
    monkeypatch.setenv("OHSHEET_REFINE_CALL_TIMEOUT_SEC", "90")
    monkeypatch.setenv("OHSHEET_ANTHROPIC_API_KEY", "sk-test-key")
    s = Settings()
    assert s.refine_enabled is False
    assert s.refine_model == "claude-haiku-4-5-20251001"
    assert s.refine_max_searches == 3
    assert s.refine_budget_sec == 600
    assert s.refine_call_timeout_sec == 90
    assert s.anthropic_api_key == "sk-test-key"
