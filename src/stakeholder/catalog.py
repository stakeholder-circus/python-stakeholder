from __future__ import annotations

from dataclasses import dataclass
from typing import Final


@dataclass(frozen=True)
class FamilySpec:
    cli_value: str
    title: str
    protocol: str | None
    group: str


FAMILY_SPECS: Final[tuple[FamilySpec, ...]] = (
    FamilySpec("code-analyzer", "Code analyzer", None, "classic-six"),
    FamilySpec("data-processing", "Data processing", None, "classic-six"),
    FamilySpec("jargon", "Jargon refresh", None, "classic-six"),
    FamilySpec("metrics", "Metrics", None, "classic-six"),
    FamilySpec("network-activity", "Network activity", "grpc", "classic-six"),
    FamilySpec("system-monitoring", "System monitoring", None, "classic-six"),
    FamilySpec("agent-workflows", "Agent workflows", "mcp", "modern-core"),
    FamilySpec("ai-inference-ops", "AI inference ops", "responses-api", "ai-governance"),
    FamilySpec("platform-engineering", "Platform engineering", None, "modern-core"),
    FamilySpec("supply-chain-security", "Supply-chain security", None, "modern-core"),
    FamilySpec("observability-ai-runtime", "Observability AI runtime", None, "modern-core"),
    FamilySpec("delivery-preview-ops", "Delivery preview ops", None, "modern-core"),
    FamilySpec("evaluation-and-guardrails", "Evaluation and guardrails", "responses-api", "ai-governance"),
    FamilySpec("knowledge-retrieval", "Knowledge retrieval", "responses-api", "ai-governance"),
    FamilySpec("edge-client-runtime", "Edge client runtime", "webtransport", "health-protocol"),
    FamilySpec("identity-and-trust", "Identity and trust", None, "security-blockchain"),
    FamilySpec("aibom-provenance", "AIBOM provenance", None, "ai-governance"),
    FamilySpec("agent-boundary-security", "Agent boundary security", "mcp", "security-blockchain"),
    FamilySpec("embedded-agentic-pipeline", "Embedded agentic pipeline", None, "health-protocol"),
    FamilySpec("data-governance-compliance", "Data governance compliance", None, "ai-governance"),
    FamilySpec("finops-capacity", "FinOps capacity", None, "ai-governance"),
    FamilySpec("blockchain-protocol-ops", "Blockchain protocol ops", None, "security-blockchain"),
    FamilySpec("cross-chain-interop", "Cross-chain interop", None, "security-blockchain"),
    FamilySpec("proof-and-sequencer-ops", "Proof and sequencer ops", None, "security-blockchain"),
    FamilySpec("hybrid-runtime-ops", "Hybrid runtime ops", None, "overlay-quantum"),
    FamilySpec("capacity-cost-controller", "Capacity and cost controller", None, "overlay-quantum"),
    FamilySpec("batch-execution-tuner", "Batch execution tuner", None, "overlay-quantum"),
    FamilySpec("compiler-maintainer", "Compiler maintainer", "openqasm3", "overlay-quantum"),
    FamilySpec("interop-adapter-engineer", "Interop adapter engineer", "qir", "overlay-quantum"),
    FamilySpec("preflight-capacity-planner", "Preflight capacity planner", None, "overlay-quantum"),
    FamilySpec("simulator-performance-engineer", "Simulator performance engineer", "openqasm3", "overlay-quantum"),
    FamilySpec("fhir-profile-generator", "FHIR profile generator", "fhir-r4", "health-protocol"),
    FamilySpec("smart-launch-oauth", "SMART launch OAuth", "smart-launch", "health-protocol"),
    FamilySpec("bulk-fhir-population-ops", "Bulk FHIR population ops", "bulk-fhir", "health-protocol"),
    FamilySpec("hl7v2-feed-ops", "HL7 v2 feed ops", "hl7v2", "health-protocol"),
    FamilySpec("clinical-workflow-events", "Clinical workflow events", "fhir-r4", "health-protocol"),
    FamilySpec("dicomweb-imaging-ops", "DICOMweb imaging ops", "dicomweb", "health-protocol"),
    FamilySpec("openehr-semantic-record-ops", "openEHR semantic record ops", "openehr", "health-protocol"),
    FamilySpec("device-telemetry-clinical", "Device telemetry clinical", "ihe-device", "health-protocol"),
    FamilySpec("emr-vendor-adapter", "EMR vendor adapter", "epic-fhir", "health-protocol"),
    FamilySpec("ocpp-chargepoint-ops", "OCPP chargepoint ops", "ocpp-2.x", "health-protocol"),
    FamilySpec("ocpi-roaming-ops", "OCPI roaming ops", "ocpi-2.x", "health-protocol"),
    FamilySpec("mcp-a2a-ops", "MCP and A2A ops", "mcp", "health-protocol"),
    FamilySpec("streaming-bus-ops", "Streaming bus ops", "kafka", "health-protocol"),
    FamilySpec("service-mesh-rpc-ops", "Service mesh RPC ops", "grpc", "health-protocol"),
    FamilySpec("multilingual-security-packs", "Multilingual security packs", None, "overlay-quantum"),
    FamilySpec("security-persona-packs", "Security persona packs", None, "overlay-quantum"),
)

FAMILIES_BY_CLI: Final[dict[str, FamilySpec]] = {spec.cli_value: spec for spec in FAMILY_SPECS}

DEV_TYPES: Final[tuple[str, ...]] = (
    "backend",
    "frontend",
    "fullstack",
    "data-science",
    "dev-ops",
    "blockchain",
    "machine-learning",
    "systems-programming",
    "game-development",
    "security",
)
JARGON_LEVELS: Final[tuple[str, ...]] = ("low", "medium", "high", "extreme")
COMPLEXITIES: Final[tuple[str, ...]] = ("low", "medium", "high", "extreme")
OUTPUT_FORMATS: Final[tuple[str, ...]] = ("text", "json")
EXPERIMENTAL_PROVIDERS: Final[tuple[str, ...]] = (
    "openai-compatible",
    "anthropic",
    "openai-consumer",
    "claude-consumer",
)
EXPERIMENTAL_ADAPTER_MODES: Final[tuple[str, ...]] = ("api", "consumer")
FLAGS: Final[tuple[str, ...]] = (
    "alerts",
    "minimal",
    "team",
    "seed",
    "output-format",
    "no-color",
    "trace",
    "list-values",
    "experimental-provider",
    "experimental-model",
    "experimental-profile",
    "experimental-prompt",
    "experimental-adapter-mode",
)

CLASSIC_FAMILIES: Final[tuple[str, ...]] = (
    "code-analyzer",
    "data-processing",
    "jargon",
    "metrics",
    "network-activity",
    "system-monitoring",
)
POLICY_FAMILIES: Final[tuple[str, ...]] = (
    "supply-chain-security",
    "observability-ai-runtime",
    "evaluation-and-guardrails",
    "identity-and-trust",
    "aibom-provenance",
    "agent-boundary-security",
    "data-governance-compliance",
    "finops-capacity",
)
ALERT_FAMILIES: Final[tuple[str, ...]] = (
    "supply-chain-security",
    "observability-ai-runtime",
    "agent-boundary-security",
    "device-telemetry-clinical",
    "ocpp-chargepoint-ops",
    "streaming-bus-ops",
    "service-mesh-rpc-ops",
    "mcp-a2a-ops",
)
TEAM_FAMILIES: Final[tuple[str, ...]] = (
    "agent-workflows",
    "platform-engineering",
    "delivery-preview-ops",
    "service-mesh-rpc-ops",
)
SECURITY_FAMILIES: Final[tuple[str, ...]] = (
    "supply-chain-security",
    "agent-boundary-security",
    "identity-and-trust",
    "aibom-provenance",
    "data-governance-compliance",
    "mcp-a2a-ops",
    "blockchain-protocol-ops",
    "cross-chain-interop",
    "proof-and-sequencer-ops",
    "multilingual-security-packs",
    "security-persona-packs",
)


def list_values() -> dict[str, object]:
    values = [spec.cli_value for spec in FAMILY_SPECS]
    return {
        "devType": list(DEV_TYPES),
        "devTypes": list(DEV_TYPES),
        "jargon": list(JARGON_LEVELS),
        "jargonLevels": list(JARGON_LEVELS),
        "complexity": list(COMPLEXITIES),
        "complexities": list(COMPLEXITIES),
        "outputFormat": list(OUTPUT_FORMATS),
        "outputFormats": list(OUTPUT_FORMATS),
        "generatorFamilies": values,
        "experimentalProviders": list(EXPERIMENTAL_PROVIDERS),
        "experimentalAdapterModes": list(EXPERIMENTAL_ADAPTER_MODES),
        "flags": list(FLAGS),
    }
