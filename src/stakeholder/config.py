from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class DevelopmentType(StrEnum):
    BACKEND = "backend"
    FRONTEND = "frontend"
    FULLSTACK = "fullstack"
    DATA_SCIENCE = "data-science"
    DEV_OPS = "dev-ops"
    BLOCKCHAIN = "blockchain"
    MACHINE_LEARNING = "machine-learning"
    SYSTEMS_PROGRAMMING = "systems-programming"
    GAME_DEVELOPMENT = "game-development"
    SECURITY = "security"


class JargonLevel(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    EXTREME = "extreme"


class Complexity(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    EXTREME = "extreme"


class OutputFormat(StrEnum):
    TEXT = "text"
    JSON = "json"


@dataclass(frozen=True)
class SessionConfig:
    dev_type: DevelopmentType = DevelopmentType.BACKEND
    jargon_level: JargonLevel = JargonLevel.MEDIUM
    complexity: Complexity = Complexity.MEDIUM
    duration_seconds: int = 0
    alerts_enabled: bool = False
    project_name: str = "distributed-cluster"
    minimal_output: bool = False
    team_activity: bool = False
    framework: str = ""
    seed: str | None = None
    output_format: OutputFormat = OutputFormat.TEXT
    no_color: bool = False
    trace: bool = False
    experimental_provider: str | None = None
    experimental_model: str | None = None
    experimental_profile: str | None = None
    experimental_prompt: str | None = None
    experimental_adapter_mode: str | None = None
