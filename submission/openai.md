# OpenAI Universal Plugin Submission

## Submission Type

- Type: With MCP
- Contents: MCP-backed app plus one bundled skill
- Plugin name: TrustedRouter Model Advisor
- Publisher: Lore Hex Corp
- Category: Developer Tools

## Public Listing

- Website: https://trustedrouter.com/choose
- Support: https://trustedrouter.com/support
- Privacy: https://trustedrouter.com/privacy
- Terms: https://trustedrouter.com/terms
- Source: https://github.com/Lore-Hex/LLM-advisor
- Logo: https://github.com/Lore-Hex/LLM-advisor/releases/download/trustedrouter-model-advisor--v1.0.0/trustedrouter-model-advisor-logo-512.png
- Skill bundle: https://github.com/Lore-Hex/LLM-advisor/releases/download/trustedrouter-model-advisor--v1.0.0/trustedrouter-model-advisor-skill-1.0.0.zip

Use the descriptions, starter prompts, release notes, availability statement, and data-handling disclosure in `listing.md`.

## MCP Server

- URL: https://trustedrouter.com/mcp
- Transport: Streamable HTTP JSON-RPC
- Authentication: Public catalog and documentation tools work without authentication. Account and billable tools accept an optional TrustedRouter bearer token.
- Browser-side UI: None
- Content Security Policy: No browser-side widget resources or fetch domains are required.
- Domain challenge: Complete the generated `/.well-known/openai-apps-challenge` verification if the portal requests it.

The server advertises explicit `readOnlyHint`, `openWorldHint`, and `destructiveHint` annotations for every tool. `chat-send` is write-capable and billable. All other submitted tools are read-only.

## Reviewer Access

The five positive and three negative cases in `openai-test-cases.md` use public catalog data and require no credentials. If review requires a live `chat-send` call, provide a dedicated, model-restricted, spend-capped reviewer key through the portal credential field. Do not put that key in this repository.

## Review Notes

This is the initial submission. The plugin helps users select and evaluate production AI models using live pricing, route availability, privacy metadata, provider health, context limits, and benchmark evidence. It estimates cost before paid evaluation and requires user approval before billable inference.

No raw API key, BYOK credential, prompt, or model output is returned by catalog tools. TrustedRouter does not durably store prompt or output content by default. Provider data handling depends on the route selected by the user and is disclosed in live provider metadata.
