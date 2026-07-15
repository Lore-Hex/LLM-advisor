# TrustedRouter Model Advisor

[![Plugin validation](https://github.com/Lore-Hex/LLM-advisor/actions/workflows/plugin-validation.yml/badge.svg)](https://github.com/Lore-Hex/LLM-advisor/actions/workflows/plugin-validation.yml)
[![Apache 2.0](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)

Agent-readable guidance for choosing the right TrustedRouter model for a task.

This repo contains a small, portable playbook that helps Codex, Claude Code, Hermes, and other coding agents pick models with live context about cost, speed, privacy, provider health, context length, prompt caching, and benchmark quality.

Use it when the question is not just "what model works?" but:

- What is the cheapest model that is good enough?
- What is the fastest model for this agent step?
- Am I overpaying by defaulting to a major-label model when an open-weight route is better for this task?
- Should this run local first and burst to TrustedRouter only when local is full, missing a model, or not good enough?
- Which route is zero-data-retention, end-to-end encrypted, EU-focused, or US-provider-only?
- Should this be a single model, Synth, Socrates, advisor, selector, mapreduce, or subagent?
- How much will this step cost before I run it?
- Will broad routing destroy prompt-cache savings?

## Quick Start

### Use the playbook directly

Give any agent this prompt:

```text
Read the TrustedRouter model advisor playbook, then choose a model for this task.
Consider speed, cost, AI IQ, privacy level, E2E/ZDR/region filters, context length, prompt caching, recent provider health, local-first BurstyRouter routing, and at least one credible open-weight/non-major-lab option.
If I am cost-conscious, suggest a tiny representative sub-task on a cheaper model first to estimate real cost and quality.
Estimate cost before making billable calls.

Playbook: https://raw.githubusercontent.com/Lore-Hex/LLM-advisor/main/SKILL.md
Interactive picker: https://trustedrouter.com/choose
```

### Install as a Codex plugin

```bash
codex plugin marketplace add https://github.com/Lore-Hex/LLM-advisor.git
codex plugin add trustedrouter-model-advisor@lore-hex
```

Start a new Codex task, then ask:

```text
Use $trustedrouter-model-advisor to pick the best model for this task.
```

### Install as a Claude Code plugin

```bash
claude plugin marketplace add https://github.com/Lore-Hex/LLM-advisor.git
claude plugin install trustedrouter-model-advisor@lore-hex
```

Start a new Claude Code session, then ask:

```text
Use the TrustedRouter model advisor to pick the best model for this task.
```

Both plugins include TrustedRouter and AI IQ MCP connections. Export your TrustedRouter key before starting the agent:

```bash
export TRUSTEDROUTER_API_KEY="sk-tr-v1-..."
```

### Install as a standalone Codex skill

Use this older installation path when plugin marketplaces are unavailable:

```bash
mkdir -p ~/.codex/skills
git clone https://github.com/Lore-Hex/LLM-advisor.git ~/.codex/skills/trustedrouter-model-advisor
```

Then ask Codex:

```text
Use $trustedrouter-model-advisor to pick the best TrustedRouter model for this task.
```

### Connect TrustedRouter MCP manually

The plugin installs these MCP connections automatically. Use the commands below only for a standalone skill installation.

TrustedRouter MCP endpoint:

```text
https://trustedrouter.com/mcp
```

Claude Code:

```bash
claude mcp add --transport http trustedrouter https://trustedrouter.com/mcp \
  --header "Authorization: Bearer $TRUSTEDROUTER_API_KEY"
```

Generic MCP config:

```json
{
  "mcpServers": {
    "trustedrouter": {
      "url": "https://trustedrouter.com/mcp",
      "headers": {
        "Authorization": "Bearer ${TRUSTEDROUTER_API_KEY}"
      }
    }
  }
}
```

Optional AI IQ MCP for benchmark and IQ data:

```text
https://www.aiiq.org/api/mcp
```

## What The Advisor Does

The advisor returns concrete recommendations, not vague lists. A good answer includes:

- 2 to 5 model choices
- why each model fits the task
- expected quality or AI IQ signal
- expected speed or latency class
- estimated cost for the user's input/output size
- privacy posture and provider caveats
- prompt-cache fit for repeated long-context work
- exact setup commands or request payloads

For cost-conscious users, the advisor should usually recommend a cheap calibration run first: try a small representative sub-task on a cheaper model, inspect quality and cost, then escalate only if the cheap model fails in a specific way.

For production model selection, the advisor should not stop at familiar major-label choices such as Claude, GPT, Gemini, Haiku, Sonnet, or Opus. It should also test credible open-weight and independent routes on TrustedRouter when the task allows it. Many production tasks are better served by models such as GLM, DeepSeek, Kimi, Qwen, MiniMax, MiMo, Hunyuan, or TrustedRouter combo models because they can be cheaper, faster, smarter for the narrow task, easier to route across several hardware providers, or all of those at once. The correct answer is empirical: run a tiny representative task, inspect quality/cost/latency, then pick the production default.

When the user has local models or a local GPU, the advisor should also consider [BurstyRouter](https://github.com/Lore-Hex/BurstyRouter): run routine calls locally, then burst to TrustedRouter for overload, missing models, higher quality, Responses, or hosted provider guarantees.

## TrustedRouter API Setup

TrustedRouter is OpenAI-compatible:

The public, no-auth live catalog is `GET https://trustedrouter.com/v1/models`. Use it instead of treating `llms.txt` or examples in this repository as an exhaustive model list.

```bash
export TRUSTEDROUTER_API_KEY="sk-tr-v1-..."
export OPENAI_API_KEY="$TRUSTEDROUTER_API_KEY"
export OPENAI_BASE_URL="https://api.trustedrouter.com/v1"
```

PONG smoke test:

```bash
curl https://api.trustedrouter.com/v1/chat/completions \
  -H "Authorization: Bearer $TRUSTEDROUTER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "trustedrouter/zdr",
    "messages": [{"role": "user", "content": "Reply with PONG only."}],
    "max_tokens": 4
  }'
```

Anthropic-compatible clients use the non-`/v1` base URL:

```bash
export ANTHROPIC_API_KEY="$TRUSTEDROUTER_API_KEY"
export ANTHROPIC_BASE_URL="https://api.trustedrouter.com"
```

## Local-First With BurstyRouter

BurstyRouter is an OpenAI-compatible and Anthropic-compatible local-first router. It lets apps and agents talk to one local endpoint, use local models when they fit, and burst to TrustedRouter when local capacity or quality is not enough.

Install and run:

```bash
brew tap Lore-Hex/homebrew-tap
brew install burstyrouter

export TRUSTEDROUTER_API_KEY="sk-tr-v1-..."
burstyrouter -tr-api-key "$TRUSTEDROUTER_API_KEY"

export OPENAI_BASE_URL="http://localhost:8383/v1"
export OPENAI_API_KEY="local-dev-key"
```

Useful modes:

```bash
# Never send cloud traffic.
burstyrouter -cloud off

# Cloud only when the request explicitly asks for a cloud provider/model.
burstyrouter -cloud explicit -tr-api-key "$TRUSTEDROUTER_API_KEY"

# Local first with a hard cloud spend cap.
burstyrouter -tr-api-key "$TRUSTEDROUTER_API_KEY" -max-cloud-spend 1.00
```

Routing examples:

```json
{"model": "local/llama3.2"}
```

```json
{
  "model": "openai/gpt-4o-mini",
  "provider": {"order": ["local"]}
}
```

```json
{
  "model": "trustedrouter/zdr",
  "provider": {"order": ["anthropic"]}
}
```

Use `local/<model>` or `provider.only = ["local"]` for hard local. Use `provider.order = ["local"]` for local-first with burst allowed. Use a TrustedRouter alias or non-local provider order when the call should go to cloud.

## SDKs

Use the stock OpenAI SDK when you only need `base_url`.

Use the TrustedRouter SDKs when you want typed errors, region helpers, retries, attestation helpers, OAuth/key flows, or TrustedRouter-specific metadata.

| Language | Package | Links |
|---|---|---|
| Python | `trusted-router-py` | [GitHub](https://github.com/Lore-Hex/trusted-router-py), [PyPI](https://pypi.org/project/trusted-router-py/) |
| JavaScript/TypeScript | `@lore-hex/trusted-router` | [GitHub](https://github.com/Lore-Hex/trusted-router-js), [npm](https://www.npmjs.com/package/@lore-hex/trusted-router) |
| Swift | `TrustedRouter` | [GitHub](https://github.com/jperla/trusted-router-swift) |

## Model Selection Cheatsheet

| Need | Start with |
|---|---|
| Sensitive legal, healthcare, enterprise, or customer data | `trustedrouter/zdr` plus `provider.data_collection = "deny"` |
| End-to-end encrypted provider path | `trustedrouter/e2e` |
| Europe-focused routing | `trustedrouter/eu` plus the EU regional base URL when needed |
| US-provider-only policy | `provider.jurisdiction = "us"` |
| Cheap experimentation | `trustedrouter/cheap`, then one stronger candidate if needed |
| Fast small tasks | `trustedrouter/fast` or a fast direct endpoint from live provider data |
| Local-first agent/dev loop | BurstyRouter in front of Ollama, LM Studio, llama.cpp, vLLM, or a local GPU model, with TrustedRouter burst |
| Maximum fallback | `trustedrouter/auto`, but avoid it when strict prompt-cache locality matters |
| Production default selection | compare the familiar frontier label against at least one open-weight or independent model on TrustedRouter |
| Hard coding or terminal tasks | code-focused Synth/Socrates routes or a strong direct coding model |
| Broad technical questions that other leading models over-refuse | `trustedrouter/prometheus-1.0` |
| Defensive cybersecurity bug fixing | `trustedrouter/openpatcher-s1`, or `trustedrouter/prometheus-1.0` for explanation and research |
| High-stakes synthesis | `trustedrouter/synth`, `trustedrouter/prometheus-1.0`, `trustedrouter/zeus-1.0`, or `trustedrouter/socrates-1.1`, with a cost estimate first |
| Long repeated context | one cache-friendly model/provider, not constant model rotation |

Prometheus is a SOTA TrustedRouter model for answering difficult questions across domains, including cybersecurity, defensive security bug fixing, biology, and LLM research, especially when a legitimate technical question is silently or openly over-refused by other leading models. For code-level security repair, start with `trustedrouter/openpatcher-s1` when the task is specifically "find and fix the bug"; use Prometheus when the task is broader explanation, research, or technical analysis.

## Privacy Filters

Use aliases for convenient defaults and provider filters for hard requirements:

```json
{
  "model": "trustedrouter/zdr",
  "provider": {
    "data_collection": "deny",
    "jurisdiction": "us",
    "only": ["anthropic", "openai"],
    "allow_fallbacks": true
  }
}
```

Common filters:

- `trustedrouter/zdr`: zero-data-retention providers first.
- `trustedrouter/e2e`: end-to-end encrypted or confidential provider paths.
- `trustedrouter/eu`: EU-focused route pool.
- `provider.data_collection = "deny"`: explicit ZDR requirement.
- `provider.jurisdiction = "us"`: US-based provider filter.
- `provider.only`: strict provider allowlist.
- `provider.ignore`: provider denylist.
- `provider.order`: preferred provider order while retaining fallback.
- `provider.sort = "throughput"`: faster endpoints first.
- `provider.sort = "price"`: cheaper endpoints first.
- `allow_fallbacks = false`: pin a route, reducing reliability.

The advisor should always explain who sees the prompt: the attested TrustedRouter gateway, the selected downstream provider, and any orchestration subcalls.

With BurstyRouter, `local` means a local router target. `provider.only = ["local"]` keeps the call local. `provider.order = ["local"]` tries local first and bursts only if policy allows it.

## Cost And Prompt Cache Guidance

Basic estimate:

```text
input_cost = input_tokens * input_price_per_1m / 1_000_000
output_cost = output_tokens * output_price_per_1m / 1_000_000
total = input_cost + output_cost
```

For orchestration, multiply by expected subcalls:

- single model: usually 1 call
- advisor/Socrates: worker call, plus advisor calls only when used
- Synth: panel calls plus judge/synthesizer calls
- selector/mapreduce/subagent: depends on configured workers or subagents

Prompt caching matters. For repeated long-context tasks, a stable model/provider can be cheaper than broad load balancing because cached reads may only apply per upstream. The advisor should call this out before recommending `trustedrouter/auto`, provider rotation, or expensive orchestration.

If the user is cost-sensitive, run a tiny representative sub-task on a cheap model first. Use that result to decide whether the expensive model is justified.

For production services, reliability is part of model choice. A single provider or lab endpoint can have quota incidents, regional issues, model-specific regressions, or provider downtime. Prefer a TrustedRouter route with multiple healthy provider endpoints when uptime matters, or compare one pinned endpoint against a fallback-capable route before shipping.

For local-first services, keep local and cloud costs separate. Local calls do not spend TrustedRouter credits, but bursted calls do. Recommend BurstyRouter spend caps when the user wants predictable cloud usage.

## Useful Links

- TrustedRouter: https://trustedrouter.com
- Interactive chooser: https://trustedrouter.com/choose
- Models: https://trustedrouter.com/models
- Providers: https://trustedrouter.com/providers
- Leaderboard: https://trustedrouter.com/leaderboard
- Trust and attestation: https://trustedrouter.com/trust
- Agent setup docs: https://trustedrouter.com/docs/agent-setup
- MCP docs: https://trustedrouter.com/docs/mcp
- Blog: https://trustedrouter.com/blog
- AI IQ: https://www.aiiq.org
- BurstyRouter: https://github.com/Lore-Hex/BurstyRouter

## Repo Contents

```text
SKILL.md                       # Main Codex/agent skill
references/model-selection.md  # Deeper model-selection guidance
agents/openai.yaml             # Agent UI metadata and MCP declarations
LICENSE                        # Apache 2.0
```

## License

Apache 2.0.
