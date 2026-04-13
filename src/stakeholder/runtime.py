from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import UTC, datetime, timedelta
import random
from typing import Final

from .catalog import (
    ALERT_FAMILIES,
    CLASSIC_FAMILIES,
    FAMILY_SPECS,
    FAMILIES_BY_CLI,
    POLICY_FAMILIES,
    SECURITY_FAMILIES,
    TEAM_FAMILIES,
    FamilySpec,
)
from .config import Complexity, DevelopmentType, JargonLevel, SessionConfig


MULTILINGUAL_SECURITY: Final[tuple[str, ...]] = (
    "english",
    "chinese",
    "russian",
    "spanish",
    "arabic",
)
SECURITY_PERSONAS: Final[tuple[str, ...]] = (
    "bug-bounty-operator",
    "incident-commander",
    "reverse-engineer",
    "threat-hunter",
    "soc-analyst",
    "dark-market-watcher",
    "cti-brief-writer",
)
DEDICATED_FAMILIES: Final[set[str]] = {
    "code-analyzer",
    "data-processing",
    "jargon",
    "metrics",
    "network-activity",
    "system-monitoring",
    "agent-workflows",
    "platform-engineering",
    "observability-ai-runtime",
    "delivery-preview-ops",
    "supply-chain-security",
}
DEDICATED_RENDERERS: Final[dict[str, tuple[str, str, str, str]]] = {
    "code-analyzer": (
        "classic-six",
        "analysisFocus",
        "typed interfaces, agent-authored patches, and MCP assumptions",
        "src/stakeholder/runtime.py",
    ),
    "data-processing": (
        "classic-six",
        "dataWindow",
        "embeddings, semantic chunks, and batch transforms with deterministic ordering",
        "src/stakeholder/runtime.py",
    ),
    "jargon": (
        "classic-six",
        "languagePolicy",
        "credible 2026 terminology instead of fake-deep phrasing",
        "src/stakeholder/runtime.py",
    ),
    "metrics": (
        "classic-six",
        "signalBlend",
        "queue depth, token spend, and GPU occupancy in a single operations lane",
        "src/stakeholder/runtime.py",
    ),
    "network-activity": (
        "classic-six",
        "transportMix",
        "RPC, event-stream, and adapter traffic under deterministic retry rules",
        "src/stakeholder/runtime.py",
    ),
    "system-monitoring": (
        "classic-six",
        "telemetryScope",
        "collector pressure, runner health, and policy-denial signals across the stack",
        "src/stakeholder/runtime.py",
    ),
    "agent-workflows": (
        "modern-core",
        "coordinationMode",
        "delegated agent work, approval gates, and cross-repo handoff envelopes",
        "src/stakeholder/runtime.py",
    ),
    "platform-engineering": (
        "modern-core",
        "platformSurface",
        "golden paths, identity boundaries, and queue ownership in the shared platform lane",
        "src/stakeholder/runtime.py",
    ),
    "observability-ai-runtime": (
        "modern-core",
        "runtimeSignals",
        "trace spans, token burn, GPU pressure, and policy denials in one runtime lane",
        "src/stakeholder/runtime.py",
    ),
    "delivery-preview-ops": (
        "modern-core",
        "deliveryGuardrail",
        "preview deploys, canaries, release flags, and rollback checkpoints under seed control",
        "src/stakeholder/runtime.py",
    ),
    "supply-chain-security": (
        "modern-core",
        "supplyChainPosture",
        "provenance, attestations, dependency drift, and secret exposure in one security lane",
        "src/stakeholder/runtime.py",
    ),
}
DEDICATED_JAVA_PATHS: Final[dict[str, str]] = {
    "code-analyzer": "src/main/java/com/stakeholder/generators/CodeAnalyzerRenderer.java",
    "data-processing": "src/main/java/com/stakeholder/generators/DataProcessingRenderer.java",
    "jargon": "src/main/java/com/stakeholder/generators/JargonRenderer.java",
    "metrics": "src/main/java/com/stakeholder/generators/MetricsRenderer.java",
    "network-activity": "src/main/java/com/stakeholder/generators/NetworkActivityRenderer.java",
    "system-monitoring": "src/main/java/com/stakeholder/generators/SystemMonitoringRenderer.java",
    "agent-workflows": "src/main/java/com/stakeholder/generators/AgentWorkflowsRenderer.java",
    "platform-engineering": "src/main/java/com/stakeholder/generators/PlatformEngineeringRenderer.java",
    "observability-ai-runtime": "src/main/java/com/stakeholder/generators/ObservabilityAIRuntimeRenderer.java",
    "delivery-preview-ops": "src/main/java/com/stakeholder/generators/DeliveryPreviewOpsRenderer.java",
    "supply-chain-security": "src/main/java/com/stakeholder/generators/SupplyChainSecurityRenderer.java",
}


@dataclass(frozen=True)
class ActivitySelection:
    family: str
    flavors: tuple[str, ...]
    kind: str


@dataclass(frozen=True)
class NormalizedEvent:
    eventType: str
    sequence: int
    message: str
    timestamp: str
    context: dict[str, object]


@dataclass(frozen=True)
class RenderedActivity:
    message: str
    metadata: dict[str, object]


def run_session(config: SessionConfig) -> list[NormalizedEvent]:
    rng = new_random(config.seed)
    plan = build_activity_plan(config, rng)
    events: list[NormalizedEvent] = []
    sequence = 0
    events.append(
        build_event(
            config,
            sequence,
            "session.start",
            "Session configuration accepted",
            {
                "project": config.project_name,
                "devType": config.dev_type.value,
                "jargon": config.jargon_level.value,
                "complexity": config.complexity.value,
                "framework": config.framework,
                "durationSeconds": config.duration_seconds,
            },
        )
    )
    sequence += 1
    events.append(
        build_event(
            config,
            sequence,
            "boot.sequence",
            "Scheduler baseline initialized",
            {
                "plannedActivities": planned_activities(config.complexity),
                "alertsEnabled": config.alerts_enabled,
                "teamActivity": config.team_activity,
                "seeded": config.seed is not None,
                "outputFormat": config.output_format.value,
            },
        )
    )
    sequence += 1

    for selection in plan:
        rendered = render_selection(selection, config)
        context = {
            "family": selection.family,
            "kind": selection.kind,
            "protocol": FAMILIES_BY_CLI[selection.family].protocol,
            "flavors": list(selection.flavors),
            "project": config.project_name,
            **rendered.metadata,
        }
        if config.framework:
            context["framework"] = config.framework
        events.append(build_event(config, sequence, "activity", rendered.message, context))
        sequence += 1
        if config.trace:
            events.append(
                build_event(
                    config,
                    sequence,
                    "trace",
                    trace_line(selection),
                    {
                        "family": selection.family,
                        "protocol": FAMILIES_BY_CLI[selection.family].protocol,
                        "flavorCount": len(selection.flavors),
                    },
                )
            )
            sequence += 1

    events.append(
        build_event(
            config,
            sequence,
            "session.end",
            "Session completed",
            {"exitCode": 0, "result": "ok", "plannedActivities": len(plan)},
        )
    )
    return events


def text_lines(config: SessionConfig) -> list[str]:
    lines: list[str] = []
    for event in run_session(config):
        if event.eventType == "activity":
            lines.append(f"[{FAMILIES_BY_CLI[event.context['family']].title}] {event.message}")
        elif event.eventType == "trace":
            lines.append(f"trace: {event.message}")
    lines.append("session terminated (deterministic-pass)")
    return lines


def build_activity_plan(config: SessionConfig, rng: random.Random) -> list[ActivitySelection]:
    target_count = planned_activities(config.complexity)
    eligible = eligible_families(config)
    selected: list[str] = []
    push_unique(selected, eligible, CLASSIC_FAMILIES, rng)
    if target_count >= 2:
        modern = [
            family for family in eligible if family not in CLASSIC_FAMILIES and family != "jargon"
        ]
        push_unique(selected, modern, modern, rng)
    if target_count >= 3:
        push_unique(selected, eligible, POLICY_FAMILIES, rng)
    while len(selected) < target_count:
        choice = rng.choice(eligible)
        if choice not in selected:
            selected.append(choice)
    if config.alerts_enabled:
        push_unique(selected, eligible, ALERT_FAMILIES, rng)
    if config.team_activity:
        push_unique(selected, eligible, TEAM_FAMILIES, rng)
    return [
        ActivitySelection(
            family=family,
            flavors=resolve_flavors(config, family, rng),
            kind=(
                "alert-injection"
                if config.alerts_enabled and family in ALERT_FAMILIES
                else "team-injection"
                if config.team_activity and family in TEAM_FAMILIES
                else "generator"
            ),
        )
        for family in selected
    ]


def eligible_families(config: SessionConfig) -> list[str]:
    selected = set(CLASSIC_FAMILIES)
    if config.dev_type is DevelopmentType.BACKEND:
        selected.update(
            {
                "agent-workflows",
                "ai-inference-ops",
                "platform-engineering",
                "supply-chain-security",
                "observability-ai-runtime",
                "delivery-preview-ops",
                "evaluation-and-guardrails",
                "knowledge-retrieval",
                "identity-and-trust",
                "aibom-provenance",
                "data-governance-compliance",
                "finops-capacity",
                "mcp-a2a-ops",
                "streaming-bus-ops",
                "service-mesh-rpc-ops",
            }
        )
    elif config.dev_type is DevelopmentType.FRONTEND:
        selected.update(
            {
                "agent-workflows",
                "delivery-preview-ops",
                "edge-client-runtime",
                "observability-ai-runtime",
                "knowledge-retrieval",
                "service-mesh-rpc-ops",
            }
        )
    elif config.dev_type is DevelopmentType.FULLSTACK:
        selected.update(
            {
                "agent-workflows",
                "ai-inference-ops",
                "platform-engineering",
                "observability-ai-runtime",
                "delivery-preview-ops",
                "knowledge-retrieval",
                "mcp-a2a-ops",
                "streaming-bus-ops",
                "service-mesh-rpc-ops",
                "supply-chain-security",
            }
        )
    elif config.dev_type is DevelopmentType.DATA_SCIENCE:
        selected.update(
            {
                "ai-inference-ops",
                "knowledge-retrieval",
                "evaluation-and-guardrails",
                "aibom-provenance",
                "data-governance-compliance",
                "observability-ai-runtime",
            }
        )
    elif config.dev_type is DevelopmentType.DEV_OPS:
        selected.update(
            {
                "agent-workflows",
                "platform-engineering",
                "supply-chain-security",
                "observability-ai-runtime",
                "delivery-preview-ops",
                "identity-and-trust",
                "finops-capacity",
                "mcp-a2a-ops",
                "streaming-bus-ops",
                "service-mesh-rpc-ops",
            }
        )
    elif config.dev_type is DevelopmentType.BLOCKCHAIN:
        selected.update(
            {
                "blockchain-protocol-ops",
                "cross-chain-interop",
                "proof-and-sequencer-ops",
                "supply-chain-security",
                "identity-and-trust",
                "mcp-a2a-ops",
            }
        )
    elif config.dev_type is DevelopmentType.MACHINE_LEARNING:
        selected.update(
            {
                "ai-inference-ops",
                "knowledge-retrieval",
                "evaluation-and-guardrails",
                "observability-ai-runtime",
                "aibom-provenance",
                "finops-capacity",
            }
        )
    elif config.dev_type is DevelopmentType.SYSTEMS_PROGRAMMING:
        selected.update(
            {
                "observability-ai-runtime",
                "embedded-agentic-pipeline",
                "identity-and-trust",
                "supply-chain-security",
                "streaming-bus-ops",
            }
        )
    elif config.dev_type is DevelopmentType.GAME_DEVELOPMENT:
        selected.update(
            {
                "edge-client-runtime",
                "delivery-preview-ops",
                "observability-ai-runtime",
                "streaming-bus-ops",
                "service-mesh-rpc-ops",
            }
        )
    elif config.dev_type is DevelopmentType.SECURITY:
        selected.update(
            {
                "agent-workflows",
                "supply-chain-security",
                "observability-ai-runtime",
                "evaluation-and-guardrails",
                "identity-and-trust",
                "aibom-provenance",
                "agent-boundary-security",
                "data-governance-compliance",
                "mcp-a2a-ops",
                "streaming-bus-ops",
                "service-mesh-rpc-ops",
            }
        )
    context = f"{config.project_name} {config.framework}".lower()
    if contains_keyword(
        context, "ehr", "emr", "fhir", "hl7", "openehr", "dicom", "clinical", "patient", "hospital"
    ):
        selected.update(
            {
                "fhir-profile-generator",
                "smart-launch-oauth",
                "bulk-fhir-population-ops",
                "hl7v2-feed-ops",
                "clinical-workflow-events",
                "dicomweb-imaging-ops",
                "openehr-semantic-record-ops",
                "device-telemetry-clinical",
                "emr-vendor-adapter",
            }
        )
    if contains_keyword(context, "charge", "charger", "charging", "ev", "ocpp", "ocpi", "roaming"):
        selected.update(
            {
                "ocpp-chargepoint-ops",
                "ocpi-roaming-ops",
                "streaming-bus-ops",
                "service-mesh-rpc-ops",
            }
        )
    if contains_keyword(context, "quantum", "qir", "qasm", "braket", "qiskit", "cudaq", "ionq"):
        selected.update(
            {
                "hybrid-runtime-ops",
                "capacity-cost-controller",
                "batch-execution-tuner",
                "compiler-maintainer",
                "interop-adapter-engineer",
                "preflight-capacity-planner",
                "simulator-performance-engineer",
            }
        )
    if contains_keyword(
        context, "mcp", "a2a", "mqtt", "nats", "kafka", "grpc", "graphql", "webtransport"
    ):
        selected.update({"mcp-a2a-ops", "streaming-bus-ops", "service-mesh-rpc-ops"})
    return [spec.cli_value for spec in FAMILY_SPECS if spec.cli_value in selected]


def resolve_flavors(config: SessionConfig, family: str, rng: random.Random) -> tuple[str, ...]:
    flavors: list[str] = []
    if config.dev_type is DevelopmentType.SECURITY or family in SECURITY_FAMILIES:
        if config.jargon_level in {JargonLevel.HIGH, JargonLevel.EXTREME} or config.alerts_enabled:
            flavors.append(f"multilingual-security:{rng.choice(MULTILINGUAL_SECURITY)}")
        if config.jargon_level in {JargonLevel.HIGH, JargonLevel.EXTREME}:
            flavors.append(f"security-persona:{rng.choice(SECURITY_PERSONAS)}")
    context = f"{config.project_name} {config.framework}".lower()
    if contains_keyword(
        context, "experimental", "openai", "anthropic", "claude", "responses", "llm"
    ) and family in {
        "ai-inference-ops",
        "evaluation-and-guardrails",
        "aibom-provenance",
    }:
        flavors.append("experimental-live-provider")
    return tuple(flavors)


def render_selection(selection: ActivitySelection, config: SessionConfig) -> RenderedActivity:
    spec = FAMILIES_BY_CLI[selection.family]
    if selection.family in DEDICATED_FAMILIES:
        renderer_group, focus_key, focus_value, _ = DEDICATED_RENDERERS[selection.family]
        detail = dedicated_detail(selection.family, config.jargon_level)
        metadata: dict[str, object] = {
            "rendererGroup": renderer_group,
            "familyMode": "dedicated",
            "familyFocusKey": focus_key,
            focus_key: focus_value,
            "smokeEvidence": True,
        }
        if selection.family == "agent-workflows":
            metadata["controlPlane"] = spec.cli_value
        else:
            metadata["discipline"] = spec.cli_value
        metadata["traceabilitySourceRepo"] = "rust-stakeholder"
        metadata["traceabilitySourcePath"] = DEDICATED_RENDERERS[selection.family][3]
        metadata["traceabilityJavaRepo"] = "java-stakeholder"
        metadata["traceabilityJavaPath"] = DEDICATED_JAVA_PATHS[selection.family]
        metadata["traceabilityContractRepo"] = "stakeholder-core"
        metadata["traceabilityContractPath"] = "docs/generator-families.md"
        metadata["traceabilityParityClass"] = "depth"
        return RenderedActivity(
            message=f"{spec.title.lower()} depth pass for {config.project_name}: {detail} Traceability is anchored to Java, Rust, and stakeholder-core.",
            metadata=metadata,
        )
    return RenderedActivity(
        message=f"{spec.title.lower()} lane for {config.project_name}: {fallback_detail(spec, config.jargon_level)}",
        metadata={
            "rendererGroup": spec.group,
            "familyMode": "grouped-fallback",
            "protocolAware": spec.protocol is not None,
        },
    )


def fallback_detail(spec: FamilySpec, jargon: JargonLevel) -> str:
    by_group = {
        "classic-six": "keeping the baseline scheduler deterministic while the shared registry handles the legacy engineering lanes",
        "modern-core": "coordinating 2026-first control-plane work under the shared registry and deterministic activity planner",
        "ai-governance": "tracking retrieval, evaluation, provenance, and governance checkpoints without widening the parity contract",
        "security-blockchain": "holding trust, sequencing, and boundary controls steady under deterministic replay",
        "health-protocol": "covering protocol-aware operations through grouped fallback until dedicated family ports land",
        "overlay-quantum": "holding overlay and quantum operations on grouped fallback while preserving the expanded registry surface",
    }
    detail = by_group.get(spec.group, "running through the shared deterministic fallback renderer")
    if jargon in {JargonLevel.HIGH, JargonLevel.EXTREME} and spec.protocol:
        return f"{detail} with protocol focus on {spec.protocol}"
    return detail


def dedicated_detail(family: str, jargon: JargonLevel) -> str:
    details = {
        "code-analyzer": {
            JargonLevel.LOW: "reviewing typed interfaces and generated-client drift across the active service graph",
            JargonLevel.MEDIUM: "reviewing typed interfaces and generated-client drift across the active service graph",
            JargonLevel.HIGH: "triaging monorepo dependency edges, schema mismatches, and SDK drift before merge",
            JargonLevel.EXTREME: "replaying agent-authored patchsets against contract drift, ownership boundaries, and tool assumptions",
        },
        "data-processing": {
            JargonLevel.LOW: "rebuilding embeddings, semantic chunks, and batch transforms with deterministic ordering",
            JargonLevel.MEDIUM: "rebuilding embeddings, semantic chunks, and batch transforms with deterministic ordering",
            JargonLevel.HIGH: "reconciling retrieval indexes, backfills, and multimodal data cuts for downstream consumers",
            JargonLevel.EXTREME: "stitching lakehouse slices, evaluation-ready datasets, and replay-safe transforms into one data lane",
        },
        "jargon": {
            JargonLevel.LOW: "keeping technical language current without drifting into fake-deep jargon",
            JargonLevel.MEDIUM: "keeping technical language current without drifting into fake-deep jargon",
            JargonLevel.HIGH: "switching phrasing toward credible 2026 agent, platform, protocol, and security terminology",
            JargonLevel.EXTREME: "enforcing modern domain vocabulary so advanced output stays precise instead of sounding synthetic",
        },
        "metrics": {
            JargonLevel.LOW: "tracking queue depth, latency bands, and cost signals across the active workload",
            JargonLevel.MEDIUM: "tracking queue depth, latency bands, and cost signals across the active workload",
            JargonLevel.HIGH: "correlating token spend, SLO burn, GPU occupancy, and attestation coverage in one metrics lane",
            JargonLevel.EXTREME: "folding evaluation score movement, blob economics, and runner pressure into a single operations dashboard",
        },
        "network-activity": {
            JargonLevel.LOW: "observing RPC, event-stream, and adapter traffic across the current service boundary",
            JargonLevel.MEDIUM: "observing RPC, event-stream, and adapter traffic across the current service boundary",
            JargonLevel.HIGH: "mapping MCP calls, inference APIs, registry fetches, and cross-domain message flow under backpressure",
            JargonLevel.EXTREME: "profiling mixed gRPC, Kafka, MQTT, and bridge traffic while preserving replay semantics and retry windows",
        },
        "system-monitoring": {
            JargonLevel.LOW: "watching collector pressure, runner health, and process saturation on the active stack",
            JargonLevel.MEDIUM: "watching collector pressure, runner health, and process saturation on the active stack",
            JargonLevel.HIGH: "capturing GPU memory pressure, secret-scan spikes, sandbox failures, and scheduler queue churn",
            JargonLevel.EXTREME: "stitching host telemetry, proof queues, provisioning lag, and policy denials into one operational heartbeat",
        },
        "agent-workflows": {
            JargonLevel.LOW: "routing coding-agent work through review queues and approval gates",
            JargonLevel.MEDIUM: "routing coding-agent work through review queues and approval gates",
            JargonLevel.HIGH: "coordinating delegated patch runs, blocked tool calls, and human checkpoints across multiple repos",
            JargonLevel.EXTREME: "orchestrating branch handoff envelopes, MCP leases, and merge-safe approval chains for background agents",
        },
        "platform-engineering": {
            JargonLevel.LOW: "keeping golden paths, identity handoffs, and queue ownership explicit across the platform lane",
            JargonLevel.MEDIUM: "keeping golden paths, identity handoffs, and queue ownership explicit across the platform lane",
            JargonLevel.HIGH: "lining up golden paths, identity federation, queue ownership, and paved-road rollouts across the platform control plane",
            JargonLevel.EXTREME: "reconciling platform contracts, tenancy edges, build queues, and paved-road drift across the shared engineering surface",
        },
        "observability-ai-runtime": {
            JargonLevel.LOW: "tracking trace spans, token burn, GPU pressure, and policy denials in one runtime lane",
            JargonLevel.MEDIUM: "tracking trace spans, token burn, GPU pressure, and policy denials in one runtime lane",
            JargonLevel.HIGH: "correlating inference spans, token burn, GPU saturation, and sandbox denials across the AI runtime",
            JargonLevel.EXTREME: "stitching evaluation regressions, trace waterfalls, GPU fragmentation, and policy failures into one runtime investigation lane",
        },
        "delivery-preview-ops": {
            JargonLevel.LOW: "keeping preview deploys, canaries, and release flags legible before promotion",
            JargonLevel.MEDIUM: "keeping preview deploys, canaries, and release flags legible before promotion",
            JargonLevel.HIGH: "coordinating preview deploys, canary health, release flags, and rollback checkpoints under seed control",
            JargonLevel.EXTREME: "threading preview environments, phased rollouts, rollback gates, and reviewer sign-off through one delivery lane",
        },
        "supply-chain-security": {
            JargonLevel.LOW: "tracking provenance, attestations, dependency drift, and secret exposure in one security lane",
            JargonLevel.MEDIUM: "tracking provenance, attestations, dependency drift, and secret exposure in one security lane",
            JargonLevel.HIGH: "linking attestations, dependency drift, key rotation, and registry trust signals across the supply chain",
            JargonLevel.EXTREME: "triaging attestation gaps, compromised dependencies, secret sprawl, and signing-boundary drift before release",
        },
    }
    return details[family][jargon]


def build_event(
    config: SessionConfig, sequence: int, event_type: str, message: str, context: dict[str, object]
) -> NormalizedEvent:
    base = datetime(1970, 1, 1, tzinfo=UTC) if config.seed is not None else datetime.now(tz=UTC)
    return NormalizedEvent(
        eventType=event_type,
        sequence=sequence,
        message=message,
        timestamp=(base + timedelta(seconds=sequence)).isoformat().replace("+00:00", "Z"),
        context=context,
    )


def serialize_events(events: list[NormalizedEvent]) -> list[dict[str, object]]:
    return [asdict(event) for event in events]


def trace_line(selection: ActivitySelection) -> str:
    protocol = FAMILIES_BY_CLI[selection.family].protocol
    suffix = f" protocol={protocol}" if protocol else ""
    return f"scheduled {selection.family} kind={selection.kind} flavorCount={len(selection.flavors)}{suffix}"


def planned_activities(complexity: Complexity) -> int:
    return {
        Complexity.LOW: 1,
        Complexity.MEDIUM: 2,
        Complexity.HIGH: 3,
        Complexity.EXTREME: 4,
    }[complexity]


def new_random(seed: str | None) -> random.Random:
    if seed is None:
        return random.Random()
    return random.Random(stable_seed(seed))


def stable_seed(value: str) -> int:
    try:
        return int(value, 10)
    except ValueError:
        hash_value = 1469598103934665603
        for byte in value.encode("utf-8"):
            hash_value ^= byte
            hash_value *= 1099511628211
            hash_value &= 0xFFFFFFFFFFFFFFFF
        return hash_value


def push_unique(
    selected: list[str], eligible: list[str], pool: tuple[str, ...] | list[str], rng: random.Random
) -> None:
    candidates = [family for family in pool if family in eligible and family not in selected]
    if candidates:
        selected.append(rng.choice(candidates))


def contains_keyword(haystack: str, *needles: str) -> bool:
    return any(needle in haystack for needle in needles)
