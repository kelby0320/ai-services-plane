from dataclasses import dataclass

from ai_core.orchestration.services.llm_service import LLMService


@dataclass
class Services:
    """Container for orchestration services."""

    llm_main: LLMService
