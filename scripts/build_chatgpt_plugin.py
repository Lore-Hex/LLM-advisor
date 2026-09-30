"""Validate and build the public ChatGPT submission, without local credentials.

Uses the September 2026 public submission format, which includes review
extensions and supportURL not yet accepted by older local Codex validators.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from urllib.parse import urlsplit
from zipfile import ZIP_DEFLATED, ZipFile

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "submission/packages/trustedrouter-model-advisor"


def validate() -> dict:
    manifest = json.loads((PACKAGE / ".codex-plugin/plugin.json").read_text())
    ui = manifest["interface"]
    for field in ("displayName", "shortDescription"):
        assert 0 < len(ui[field]) <= 30, field
    assert len(ui["longDescription"]) <= 4000
    for field in ("websiteURL", "supportURL", "privacyPolicyURL", "termsOfServiceURL"):
        url = urlsplit(ui[field])
        assert url.scheme == "https" and url.hostname == "trustedrouter.com", field
    assert not ui.get("screenshots"), "This release has no custom UI screenshots"
    for field in ("logo", "composerIcon"):
        asset = (PACKAGE / ui[field]).resolve()
        assert asset.is_relative_to(PACKAGE) and asset.is_file()
    assert len(ui["defaultPrompt"]) <= 3
    assert all(len(prompt) <= 128 and "@" not in prompt for prompt in ui["defaultPrompt"])
    assert manifest["mcpServers"] == "./.mcp.json"
    config = json.loads((PACKAGE / ".mcp.json").read_text())
    assert config == {"mcpServers": {"trustedrouter": {"url": "https://trustedrouter.com/mcp/advisor"}}}
    review = manifest["extensions"]["com.openai"]["review"]
    assert review["commerce"] is False
    assert len(review["test_cases"]["positive"]) == 5
    assert len(review["test_cases"]["negative"]) == 3
    for case in review["test_cases"]["positive"] + review["test_cases"]["negative"]:
        assert case["description"] and case["prompt"] and case["expected_behavior"]
    skill = PACKAGE / "skills/trustedrouter-model-advisor/SKILL.md"
    assert skill.is_file()
    for path in PACKAGE.rglob("*"):
        assert not path.is_symlink(), path
        if path.is_file():
            assert path.suffix in {".json", ".svg", ".md"}, path
            content = path.read_text()
            assert "sk-tr-" not in content and "Bearer " not in content, path
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("/tmp/trustedrouter-chatgpt-plugin.zip"))
    args = parser.parse_args()
    manifest = validate()
    with ZipFile(args.output, "w", ZIP_DEFLATED) as archive:
        for path in sorted(PACKAGE.rglob("*")):
            if path.is_file():
                archive.write(path, path.relative_to(PACKAGE))
    print(f"Validated {manifest['name']} {manifest['version']}: {args.output}")
    if not manifest["extensions"]["com.openai"]["review"].get("demo_recording_url"):
        print("Review still requires a real accessible demo recording URL.")


if __name__ == "__main__":
    main()
