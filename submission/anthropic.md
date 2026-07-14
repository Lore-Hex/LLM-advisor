# Anthropic Official Marketplace Submission

- Plugin name: TrustedRouter Model Advisor
- Plugin identifier: `trustedrouter-model-advisor`
- Marketplace identifier: `lore-hex`
- Version: `1.0.0`
- Repository: https://github.com/Lore-Hex/LLM-advisor
- Release: https://github.com/Lore-Hex/LLM-advisor/releases/tag/trustedrouter-model-advisor--v1.0.0
- Publisher: Lore Hex Corp
- Contact: security@trustedrouter.com
- Category: Development
- License: Apache-2.0

## Submission Description

TrustedRouter Model Advisor helps Claude Code choose a model for a specific production task using current price, speed, quality, privacy, context, provider-health, and fallback information. It estimates cost before billable calls, compares familiar frontier models with credible open-weight alternatives, applies explicit privacy and regional constraints, and proposes a small representative evaluation before a production commitment.

The plugin bundles one skill and two MCP integrations. TrustedRouter MCP supplies live model, endpoint, provider, documentation, credit, generation, and short test-message tools. AI IQ MCP supplies public benchmark context. A TrustedRouter API key is optional for public catalog guidance and required for account metadata or billable test messages.

## Verification

- `claude plugin validate --strict .` passes.
- A clean public HTTPS marketplace installation discovers one skill and two MCP servers.
- GitHub Actions validates the packaged skill against the canonical source and checks both runtime manifests.
- No credential or secret is included in the repository.
