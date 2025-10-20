"""Module for Gemini LLM provider."""

import os
from pathlib import Path

from t2c.core.llm_provider.providers.remote_provider import RemoteProvider


class Gemini(RemoteProvider):
    """Gemini LLM provider implementation."""

    def __init__(self) -> None:
        self._set_os_env_var("GOOGLE_APPLICATION_CREDENTIALS")
        self._set_os_env_var("VERTEXAI_PROJECT")

    def _set_os_env_var(self, key: str) -> None:
        if os.environ.get(key):
            return

        project_root = self._find_project_root()
        if project_root is None:
            return

        env_file = project_root / ".env"
        if not env_file.exists():
            return

        k = self._read_key_from_env(env_file, key)
        if k:
            os.environ[key] = k

    def _find_project_root(self) -> Path | None:
        """Find repository/project root by looking for pyproject.toml or .git."""
        current = Path(__file__).resolve().parent
        for parent in [current] + list(current.parents):
            if (parent / "pyproject.toml").exists() or (parent / ".git").exists():
                return parent
        return None

    def _read_key_from_env(self, env_path: Path, key_name: str) -> str | None:
        """Parse a simple .env file and return the value for key_name if present.

        Supported formats are KEY=VALUE with optional surrounding quotes and
        comment lines starting with #. This is intentionally minimal to avoid
        adding a new dependency.
        """
        try:
            with env_path.open("r", encoding="utf-8") as fh:
                for raw in fh:
                    line = raw.strip()
                    if not line or line.startswith("#"):
                        continue
                    if "=" not in line:
                        continue
                    k, v = line.split("=", 1)
                    k = k.strip()
                    if k != key_name:
                        continue
                    v = v.strip()
                    if (v.startswith('"') and v.endswith('"')) or (
                        v.startswith("'") and v.endswith("'")
                    ):
                        v = v[1:-1]
                    return v
        except Exception:
            return None
        return None

    def _get_server_model_name(self) -> str:
        return "vertex_ai/gemini-2.0-flash"

    def _get_api_base(self) -> str:
        return ""
