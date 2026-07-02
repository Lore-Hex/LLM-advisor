# TrustedRouter Model Advisor

Agent-readable guidance for choosing the right TrustedRouter model for a task.

This repo contains a small, portable playbook that helps Codex, Claude Code, Hermes, and other coding agents pick models with live context about cost, speed, privacy, provider health, context length, prompt caching, and benchmark quality.

Use it when the question is not just "what model works?" but:

- What is the cheapest model that is good enough?
- What is the fastest model for this agent step?
- Which route is zero-data-retention, end-to-end encrypted, EU-focused, or US-provider-only?
- Should this be a single model, Synth, Socrates, advisor, selector, mapreduce, or subagent?
- How much will this step cost before I run it?
- Will broad routing destroy prompt-cache savings?

## Quick Start

### Use the playbook directly

Give any agent this prompt:

```text
Read the TrustedRouter model advisor playbook, then choose a model for this task.
Consider speed, cost, AI IQ, privacy level, E2E/ZDR/region filters, context length, prompt caching, and recent provider health.
If I am cost-conscious, suggest a tiny representative sub-task on a cheaper model first to estimate real cost and quality.
Estimate cost before making billable calls.

Playbook: https://raw.githubusercontent.com/Lore-Hex/LLM-advisor/main/SKILL.md
Interactive picker: https://trustedrouter.com/choose
```

### Install as a Codex skill

```bash
mkdir -p ~/.codex/skills
git clone https://github.com/Lore-Hex/LLM-advisor.git ~/.codex/skills/trustedrouter-model-advisor
```

Then ask Codex:

```text
Use $trustedrouter-model-advisor to pick the best TrustedRouter model for this task.
```

### Connect TrustedRouter MCP

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

## TrustedRouter API Setup

TrustedRouter is OpenAI-compatible:

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
| Maximum fallback | `trustedrouter/auto`, but avoid it when strict prompt-cache locality matters |
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

## Repo Contents

```text
SKILL.md                       # Main Codex/agent skill
references/model-selection.md  # Deeper model-selection guidance
agents/openai.yaml             # Agent UI metadata and MCP declarations
LICENSE                        # Apache 2.0
```

## License

Apache 2.0.
