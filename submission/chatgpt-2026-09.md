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

Package prepared. Production endpoint, domain verification, walkthrough and
review submission remain to be verified. Update this section from actual
dashboard and production evidence, not planned actions.
