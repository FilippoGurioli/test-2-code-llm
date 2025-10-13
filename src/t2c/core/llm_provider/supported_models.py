from enum import Enum


class SupportedModels(str, Enum):
    """Enumeration of supported LLM models."""

    Mistral = "mistral"
    DeepSeek = "deepseek-r1"
    Smollm2 = "smollm2"
    Qwen3 = "qwen3"
    Copilot = "copilot"
    Gemini = "gemini"
