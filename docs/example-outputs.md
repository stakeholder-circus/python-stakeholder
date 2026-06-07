# Example Outputs

## Deterministic JSON smoke
- Command: `stakeholder --seed 2 --output-format json`
- Dedicated family evidence: `code-analyzer`, `data-processing`, `jargon`, `metrics`, `network-activity`, `system-monitoring`

## Deterministic JSON team smoke
- Command: `stakeholder --seed 1 --output-format json --dev-type security --team`
- Dedicated family evidence: `agent-workflows`, `platform-engineering`, `observability-ai-runtime`, `delivery-preview-ops`, `supply-chain-security`

## Experimental fail-fast
- Command: `stakeholder --experimental-provider openai-compatible`
- Result: explicit non-zero fail-fast because provider runtime is intentionally not implemented in this repo.
