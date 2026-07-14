# TrustedRouter Model Advisor Listing

## Publisher

- Name: Lore Hex Corp
- Product: TrustedRouter Model Advisor
- Category: Developer Tools
- Repository: https://github.com/Lore-Hex/LLM-advisor
- Website: https://trustedrouter.com/choose
- Support: https://trustedrouter.com/support
- Privacy: https://trustedrouter.com/privacy
- Terms: https://trustedrouter.com/terms
- Security: https://trustedrouter.com/security
- Contact: security@trustedrouter.com
- License: Apache-2.0

## Short Description

Choose the right AI model using live pricing, speed, quality, privacy, context, and provider health.

## Long Description

TrustedRouter Model Advisor helps developers choose a production model for a specific task instead of defaulting to the most familiar name. It compares current model availability, provider routes, token pricing, measured speed, context length, privacy posture, fallback options, and public quality evidence.

The advisor returns a small set of concrete choices with reasons, an estimated cost for the expected input and output, and a representative evaluation plan. It compares frontier models with credible open-weight and independent alternatives, considers local-first routing through BurstyRouter, and applies explicit ZDR, end-to-end encrypted, regional, and provider constraints when required.

The bundled skill works without a paid call. TrustedRouter MCP provides public catalog and provider tools without authentication. A TrustedRouter API key enables workspace credit metadata, generation metadata, and short billable test messages. The skill requires cost estimation and user approval before billable calls.

## Starter Prompts

1. Choose the best model for this task and estimate its cost before running anything.
2. Compare a frontier model with cheaper open-weight alternatives for this production workload.
3. Design a small model evaluation that measures quality, latency, cost, privacy, and reliability.

## Release Notes

Initial public submission. This release includes one model-selection skill, live TrustedRouter catalog and provider tools, AI IQ benchmark guidance, cost estimation, privacy-aware routing, local-first BurstyRouter guidance, and production evaluation workflows.

## Availability

All countries and regions supported by the submission directory where TrustedRouter and its selected downstream provider routes are legally available. Individual models and providers may have narrower regional availability, which the advisor must disclose from live catalog data.

## Data Handling

- Public catalog, provider, documentation, and health lookups do not require a user API key.
- Authenticated tools receive a TrustedRouter API key only as an authorization header.
- API keys must never be placed in prompts, source files, logs, or tool results.
- The skill does not store prompts or outputs.
- A short model test is billable and must not run without the user's approval.
- Provider privacy varies. The advisor must inspect live provider metadata and apply the requested privacy constraints before recommending a route.
