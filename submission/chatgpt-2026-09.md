# ChatGPT Plugin Submission

The current public package lives in
`submission/packages/trustedrouter-model-advisor`. The existing
`plugins/trustedrouter-model-advisor` package remains the authenticated local
Claude Code/Codex integration; do not submit it as the public ChatGPT package.

## Product

TrustedRouter Model Advisor compares public catalog routes, estimates uncached
text-token cost from counts, checks source-linked privacy evidence, and plans a
three-prompt evaluation. It does not send inference, read accounts, collect API
keys, offer checkout, or change an agent's settings.

One no-auth MCP server: `https://trustedrouter.com/mcp/advisor`.
Five tools: search_models, compare_models, estimate_cost, get_provider, search_docs.
The source lives in the quill-router repository's `routes/mcp_advisor.py`.

## Build and Review

Run `python3 scripts/build_chatgpt_plugin.py --output /tmp/trustedrouter-chatgpt-plugin.zip`.
The package includes current logo, public listing URLs, five positive cases,
three negative cases, and instructions that distinguish upstream privacy from
ChatGPT processing. No screenshots are included because this release has no
custom UI. No demo URL is invented: add the actual recording before submission.

The September 2026 [official submission format](https://developers.openai.com/plugins/deploy/submission)
supports `extensions.com.openai.review` and `interface.supportURL`. Older local
Codex validators reject those newer fields; the builder checks the public
format, and the OpenAI dashboard is the final submission validator.

Submit under the verified Lore Hex Corp identity at
https://platform.openai.com/plugins. Verify domain ownership with the portal's
exact challenge token. Never overwrite another plugin's challenge or put keys
in the ZIP. Complete MCP setup, upload the actual walkthrough, run the listed
test cases, resolve required findings, then submit for review. Uploading a
draft is not submitting or publication. Record the actual state below.

## Status

Backend [PR 1440](https://github.com/Lore-Hex/quill-router/pull/1440) and package
[PR 3](https://github.com/Lore-Hex/LLM-advisor/pull/3) are merged.
The standard [GCP rollout](https://github.com/Lore-Hex/quill-router/actions/runs/36784751228)
completed successfully at revision `8b99a320`, including the public service.
AWS and Azure were not changed by this release.

Verification:
- 60 focused tests passed locally; Ruff and mypy passed.
- Full CI and the coverage gate passed (87% coverage on the backend PR).
- The duplicate full local suite was interrupted because of severe laptop
  resource contention; full-suite verification is from CI, not a claimed local pass.
- Six production walkthrough scenarios and 13 real MCP calls passed.
- Anonymous access to the existing authenticated `/mcp` still returns 401.
- OpenAI verified the public domain challenge. Metadata and skill checks passed.

The [walkthrough and actual MCP receipts](https://github.com/Lore-Hex/LLM-advisor/releases/tag/chatgpt-model-advisor-v1.1.1)
contain public metadata only. The video is a developer harness, not a simulated
ChatGPT UI or a claim of directory approval.

OpenAI draft: `plugin_asdk_app_6abd7c6a72608191ac7256939794d793`, under verified
Lore Hex Corp. Tool discovery, final review submission and publication still
need confirmation in the portal; a draft upload is not a submitted review.
