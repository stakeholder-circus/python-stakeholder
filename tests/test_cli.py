from __future__ import annotations

import json
from io import StringIO

from stakeholder.cli import run
from stakeholder.config import JargonLevel, SessionConfig
from stakeholder.runtime import ActivitySelection, render_selection


def test_list_values_returns_registry_and_experimental_flags() -> None:
    stdout = StringIO()
    stderr = StringIO()
    assert run(["--list-values"], stdout=stdout, stderr=stderr) == 0
    payload = json.loads(stdout.getvalue())
    assert "code-analyzer" in payload["generatorFamilies"]
    assert "agent-workflows" in payload["generatorFamilies"]
    assert "experimental-provider" in payload["flags"]


def test_json_output_is_deterministic_for_same_seed() -> None:
    first = StringIO()
    second = StringIO()
    assert run(["--seed", "42", "--output-format", "json"], stdout=first, stderr=StringIO()) == 0
    assert run(["--seed", "42", "--output-format", "json"], stdout=second, stderr=StringIO()) == 0
    assert json.loads(first.getvalue()) == json.loads(second.getvalue())


def test_classic_six_and_modern_core_have_dedicated_renderer_output() -> None:
    config = SessionConfig(project_name="depth-tranche", jargon_level=JargonLevel.HIGH)
    cases = [
        (
            "code-analyzer",
            "classic-six",
            "analysisFocus",
            "typed interfaces, agent-authored patches, and MCP assumptions",
            "triaging monorepo dependency edges",
            "src/main/java/com/stakeholder/generators/CodeAnalyzerRenderer.java",
        ),
        (
            "data-processing",
            "classic-six",
            "dataWindow",
            "embeddings, semantic chunks, and batch transforms with deterministic ordering",
            "reconciling retrieval indexes",
            "src/main/java/com/stakeholder/generators/DataProcessingRenderer.java",
        ),
        (
            "jargon",
            "classic-six",
            "languagePolicy",
            "credible 2026 terminology instead of fake-deep phrasing",
            "switching phrasing toward credible 2026 agent",
            "src/main/java/com/stakeholder/generators/JargonRenderer.java",
        ),
        (
            "metrics",
            "classic-six",
            "signalBlend",
            "queue depth, token spend, and GPU occupancy in a single operations lane",
            "correlating token spend",
            "src/main/java/com/stakeholder/generators/MetricsRenderer.java",
        ),
        (
            "network-activity",
            "classic-six",
            "transportMix",
            "RPC, event-stream, and adapter traffic under deterministic retry rules",
            "mapping MCP calls",
            "src/main/java/com/stakeholder/generators/NetworkActivityRenderer.java",
        ),
        (
            "system-monitoring",
            "classic-six",
            "telemetryScope",
            "collector pressure, runner health, and policy-denial signals across the stack",
            "capturing GPU memory pressure",
            "src/main/java/com/stakeholder/generators/SystemMonitoringRenderer.java",
        ),
        (
            "agent-workflows",
            "modern-core",
            "coordinationMode",
            "delegated agent work, approval gates, and cross-repo handoff envelopes",
            "coordinating delegated patch runs",
            "src/main/java/com/stakeholder/generators/AgentWorkflowsRenderer.java",
        ),
        (
            "platform-engineering",
            "modern-core",
            "platformSurface",
            "golden paths, identity boundaries, and queue ownership in the shared platform lane",
            "lining up golden paths, identity federation, queue ownership, and paved-road rollouts",
            "src/main/java/com/stakeholder/generators/PlatformEngineeringRenderer.java",
        ),
        (
            "observability-ai-runtime",
            "modern-core",
            "runtimeSignals",
            "trace spans, token burn, GPU pressure, and policy denials in one runtime lane",
            "correlating inference spans, token burn, GPU saturation, and sandbox denials",
            "src/main/java/com/stakeholder/generators/ObservabilityAIRuntimeRenderer.java",
        ),
        (
            "delivery-preview-ops",
            "modern-core",
            "deliveryGuardrail",
            "preview deploys, canaries, release flags, and rollback checkpoints under seed control",
            "coordinating preview deploys, canary health, release flags, and rollback checkpoints",
            "src/main/java/com/stakeholder/generators/DeliveryPreviewOpsRenderer.java",
        ),
        (
            "supply-chain-security",
            "modern-core",
            "supplyChainPosture",
            "provenance, attestations, dependency drift, and secret exposure in one security lane",
            "linking attestations, dependency drift, key rotation, and registry trust signals",
            "src/main/java/com/stakeholder/generators/SupplyChainSecurityRenderer.java",
        ),
    ]
    for family, renderer_group, focus_key, focus_value, detail_fragment, java_path in cases:
        rendered = render_selection(
            ActivitySelection(family=family, flavors=(), kind="generator"), config
        )
        assert rendered.metadata["rendererGroup"] == renderer_group
        assert rendered.metadata["familyMode"] == "dedicated"
        assert rendered.metadata["familyFocusKey"] == focus_key
        assert rendered.metadata[focus_key] == focus_value
        assert rendered.metadata["traceabilitySourceRepo"] == "rust-stakeholder"
        assert rendered.metadata["traceabilitySourcePath"] == "src/stakeholder/runtime.py"
        assert rendered.metadata["traceabilityJavaRepo"] == "java-stakeholder"
        assert rendered.metadata["traceabilityJavaPath"] == java_path
        assert rendered.metadata["traceabilityContractRepo"] == "stakeholder-core"
        assert rendered.metadata["traceabilityContractPath"] == "docs/generator-families.md"
        assert rendered.metadata["traceabilityParityClass"] == "depth"
        assert rendered.metadata["smokeEvidence"] is True
        assert detail_fragment in rendered.message
        assert "Traceability is anchored to Java, Rust, and stakeholder-core." in rendered.message


def test_experimental_flags_fail_fast() -> None:
    stdout = StringIO()
    stderr = StringIO()
    assert run(["--experimental-provider", "openai-compatible"], stdout=stdout, stderr=stderr) == 2
    assert "not implemented" in stderr.getvalue()
