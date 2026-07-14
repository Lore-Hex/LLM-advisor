#!/usr/bin/env python3
"""Validate the dual-runtime plugin package without external dependencies."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "trustedrouter-model-advisor"
VERSION_PATTERN = re.compile(r"^\d+\.\d+\.\d+$")


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def main() -> int:
    errors: list[str] = []
    required_paths = [
        PLUGIN / ".codex-plugin" / "plugin.json",
        PLUGIN / ".claude-plugin" / "plugin.json",
        PLUGIN / ".mcp.json",
        PLUGIN / "skills" / "trustedrouter-model-advisor" / "SKILL.md",
        ROOT / ".agents" / "plugins" / "marketplace.json",
        ROOT / ".claude-plugin" / "marketplace.json",
    ]
    for path in required_paths:
        require(path.is_file(), f"missing required file: {path.relative_to(ROOT)}", errors)

    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors), file=sys.stderr)
        return 1

    codex = load_json(required_paths[0])
    claude = load_json(required_paths[1])
    claude_mcp = load_json(required_paths[2])
    codex_market = load_json(required_paths[4])
    claude_market = load_json(required_paths[5])

    name = "trustedrouter-model-advisor"
    require(codex.get("name") == name, "Codex plugin name is incorrect", errors)
    require(claude.get("name") == name, "Claude plugin name is incorrect", errors)
    require(codex.get("version") == claude.get("version"), "plugin versions differ", errors)
    version = str(codex.get("version", ""))
    require(bool(VERSION_PATTERN.fullmatch(version)), "plugin version is not strict semver", errors)

    source_pairs = [
        (ROOT / "SKILL.md", PLUGIN / "skills" / name / "SKILL.md"),
        (
            ROOT / "references" / "model-selection.md",
            PLUGIN / "skills" / name / "references" / "model-selection.md",
        ),
        (ROOT / "agents" / "openai.yaml", PLUGIN / "skills" / name / "agents" / "openai.yaml"),
    ]
    for source, packaged in source_pairs:
        require(source.read_bytes() == packaged.read_bytes(), f"packaged copy is stale: {packaged.relative_to(ROOT)}", errors)

    codex_servers = codex.get("mcpServers", {})
    require(isinstance(codex_servers, dict), "Codex mcpServers must be an object", errors)
    if isinstance(codex_servers, dict):
        trustedrouter = codex_servers.get("trustedrouter", {})
        require(
            isinstance(trustedrouter, dict)
            and trustedrouter.get("bearer_token_env_var") == "TRUSTEDROUTER_API_KEY",
            "Codex TrustedRouter MCP must read TRUSTEDROUTER_API_KEY",
            errors,
        )
        require("aiiq" in codex_servers, "Codex AI IQ MCP is missing", errors)

    claude_tr = claude_mcp.get("trustedrouter", {})
    require(
        isinstance(claude_tr, dict)
        and claude_tr.get("headers", {}).get("Authorization") == "Bearer ${TRUSTEDROUTER_API_KEY}",
        "Claude TrustedRouter MCP must read TRUSTEDROUTER_API_KEY",
        errors,
    )
    require("aiiq" in claude_mcp, "Claude AI IQ MCP is missing", errors)

    codex_entries = codex_market.get("plugins", [])
    claude_entries = claude_market.get("plugins", [])
    require(any(entry.get("name") == name for entry in codex_entries), "Codex marketplace entry is missing", errors)
    claude_entry = next((entry for entry in claude_entries if entry.get("name") == name), None)
    require(claude_entry is not None, "Claude marketplace entry is missing", errors)
    if claude_entry is not None:
        require(claude_entry.get("version") == version, "Claude marketplace version differs", errors)

    for path in PLUGIN.rglob("*"):
        if path.is_file():
            require(b"[TODO:" not in path.read_bytes(), f"placeholder remains in {path.relative_to(ROOT)}", errors)

    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors), file=sys.stderr)
        return 1
    print(f"Validated {name} {version} for Claude Code and Codex")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
