from __future__ import annotations

from io import StringIO
import json

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


def test_classic_six_and_agent_workflows_have_dedicated_renderer_output() -> None:
    config = SessionConfig(project_name="depth-tranche", jargon_level=JargonLevel.HIGH)
    cases = [
        (
            "code-analyzer",
            "classic-six",
            "analysisFocus",
            "typed interfaces, agent-authored patches, and MCP assumptions",
            "triaging monorepo dependency edges",
        ),
        (
            "data-processing",
            "classic-six",
            "dataWindow",
            "embeddings, semantic chunks, and batch transforms with deterministic ordering",
            "reconciling retrieval indexes",
        ),
        (
            "jargon",
            "classic-six",
            "languagePolicy",
            "credible 2026 terminology instead of fake-deep phrasing",
            "switching phrasing toward credible 2026 agent",
        ),
        (
            "metrics",
            "classic-six",
            "signalBlend",
            "queue depth, token spend, and GPU occupancy in a single operations lane",
            "correlating token spend",
        ),
        (
            "network-activity",
            "classic-six",
            "transportMix",
            "RPC, event-stream, and adapter traffic under deterministic retry rules",
            "mapping MCP calls",
        ),
        (
            "system-monitoring",
            "classic-six",
            "telemetryScope",
            "collector pressure, runner health, and policy-denial signals across the stack",
            "capturing GPU memory pressure",
        ),
        (
            "agent-workflows",
            "modern-core",
            "coordinationMode",
            "delegated agent work, approval gates, and cross-repo handoff envelopes",
            "coordinating delegated patch runs",
        ),
    ]
    for family, renderer_group, focus_key, focus_value, detail_fragment in cases:
        rendered = render_selection(
            ActivitySelection(family=family, flavors=(), kind="generator"), config
        )
        assert rendered.metadata["rendererGroup"] == renderer_group
        assert rendered.metadata["familyMode"] == "dedicated"
        assert rendered.metadata["familyFocusKey"] == focus_key
        assert rendered.metadata[focus_key] == focus_value
        assert rendered.metadata["traceabilitySourceRepo"] == "rust-stakeholder"
        assert rendered.metadata["traceabilitySourcePath"] == "src/stakeholder/runtime.py"
        assert rendered.metadata["traceabilityContractRepo"] == "stakeholder-core"
        assert rendered.metadata["traceabilityContractPath"] == "docs/generator-families.md"
        assert rendered.metadata["traceabilityParityClass"] == "depth"
        assert rendered.metadata["smokeEvidence"] is True
        assert detail_fragment in rendered.message
        assert "Traceability is anchored to Rust and stakeholder-core." in rendered.message


def test_experimental_flags_fail_fast() -> None:
    stdout = StringIO()
    stderr = StringIO()
    assert run(["--experimental-provider", "openai-compatible"], stdout=stdout, stderr=stderr) == 2
    assert "not implemented" in stderr.getvalue()
