# Industrial Agent Reliability Benchmark

Industrial Agent Reliability Benchmark is an open-source evaluation harness for multi-step agentic AI systems in regulated industrial workflows. It measures behavior that single-turn LLM evals miss: tool-call accuracy, task completion, loop termination, grounding, hallucination risk, and governance controls.

The initial benchmark uses 18 synthetic aerospace scenarios across supply chain, regulatory lookup, and bid/no-bid recommendation workflows. All data is synthetic and safe for public review.

## Hiring Team Review

- Public repo: [github.com/plaidpizazz/industrial-agent-reliability-benchmark](https://github.com/plaidpizazz/industrial-agent-reliability-benchmark)
- Public dashboard: [industrial-agent-reliability-benchmark.vercel.app](https://industrial-agent-reliability-benchmark.vercel.app)
- Benchmark artifacts: [`public/results`](public/results)
- Scenario dataset: [`scenarios/aerospace_synthetic_v0.jsonl`](scenarios/aerospace_synthetic_v0.jsonl)

## What It Measures

| Metric | Why it matters |
| --- | --- |
| Task completion | Confirms the agent satisfied the operational request, not just produced fluent text. |
| Tool-call accuracy | Checks the selected tools, order, and allowed-tool policy across multi-step workflows. |
| Loop termination | Detects runaway tool loops, repeated calls, and max-step failures. |
| Grounding | Penalizes forbidden or unsupported claims and missing evidence citations. |
| Governance | Rewards risk, confidence, evidence, escalation, and human-review markers. |

## Architecture

```text
Next.js dashboard
  reads public/results/*.json
  renders leaderboard, scenario coverage, and failure-mode examples

Python eval harness
  loads synthetic aerospace scenarios
  runs deterministic and optional Claude-backed agents
  scores trajectories and exports dashboard artifacts

GitHub Actions
  validates Python tests
  validates deterministic evals
  builds the public dashboard

Vercel
  deploys public dashboard previews and production site from GitHub
```

## Quickstart

```bash
npm install
python -m pip install -e ".[dev]"
npm run eval:demo
npm run build
pytest
```

Run the dashboard locally:

```bash
npm run dev
```

## Optional Claude Runs

The deterministic baselines are used for public CI so the project does not require secrets or spend API budget. To add a real Claude-backed run, set:

```bash
cp .env.example .env.local
export ANTHROPIC_API_KEY="..."
export ANTHROPIC_MODEL="claude-sonnet-4-5"
```

The `ClaudeAgentRunner` adapter implements Anthropic tool-use loops against the same mock industrial tools. The deterministic runners remain the default for reproducibility.

## LangSmith And Hugging Face

The repo is structured for LangSmith tracing/evaluation and Hugging Face Datasets packaging:

- `LANGSMITH_PROJECT=industrial-agent-reliability-benchmark` can be used for traced runs when credentials are present.
- Scenario records are JSONL and can be converted into a Hugging Face `Dataset` from `agenteval.datasets`.
- CI avoids secret-backed external services by design.

## Scenario Coverage

The synthetic benchmark includes:

- 6 supply-chain scenarios: inventory shortage, approved alternates, expedite paths, traceability, dual release, export review.
- 6 regulatory scenarios: controlled technical data, PMA repair evidence, supplier data handling, dual release, safety-critical approval, classification uncertainty.
- 6 bid/no-bid scenarios: adjusted margin, high compliance risk, supply risk, thin-margin review, autonomous approval prevention.

## Reliability Gate

The reference agent must clear:

- Composite reliability score >= 92%
- Tool-call accuracy = 100%
- Loop termination = 100%
- Grounding >= 80%

The flawed negative-control agent is intentionally expected to fail. This proves the benchmark can detect missing evidence, unsupported claims, repeated tool calls, and absent escalation.
