from t2c.core.llm_provider.interface import LLMProviderInterface
from t2c.core.reporting.observers.code_generation_observer import CodeGenerationObserver


class CodeGenerationEngine:

    def __init__(self, llm_provider: LLMProviderInterface) -> None:
        self._llm_provider: LLMProviderInterface = llm_provider
        self._observers: list[CodeGenerationObserver] = []

    def subscribe(self, observer: CodeGenerationObserver) -> None:
        self._observers.append(observer)

    def unsubscribe(self, observer: CodeGenerationObserver) -> None:
        self._observers.remove(observer)

    def generate_code(self, run_id: str, tests_path: str, output_path: str) -> bool:
        self._notify_start(run_id, "pytest")  # TODO
        tests: str = self._serialize_tests(tests_path)
        query: str = (
            f"Generate the source code that satisfies the following tests. Don't include any explanation, just the code.\n\n{tests}"
        )
        query = query + "\n\nFor each file, make sure to:\n"
        query = (
            query
            + "- include a comment on top with the file path like this: # path/to/file.py\n"
        )
        query = (
            query + "- insert them in different code snippets (use triple backticks)"
        )
        answer: str = self._llm_provider.query(query)
        print(f"LLM answer:\n{answer}")
        self._parse_answer(answer, output_path)
        self._notify_end(answer == "Hello World!")
        return answer == "Hello World!"

    def _notify_start(self, model_name: str, test_suite: str) -> None:
        for obs in self._observers:
            obs.on_code_generation_start(model_name, test_suite)

    def _notify_end(self, is_failed: bool) -> None:
        for obs in self._observers:
            obs.on_code_generation_end(is_failed)

    def _serialize_tests(self, tests_path: str) -> str:
        """Read and concatenate test files under `tests_path`.

        Walk the directory recursively, skipping hidden files and `__pycache__`.
        For each file emit a header with the relative path and the file contents
        decoded as UTF-8 (binary fallback uses repr).
        """
        import os

        parts: list[str] = []
        for root, dirs, files in os.walk(tests_path):
            dirs[:] = [d for d in dirs if not d.startswith(".") and d != "__pycache__"]
            for fname in sorted(files):
                if fname.startswith("."):
                    continue
                fpath = os.path.join(root, fname)
                rel = os.path.relpath(fpath, tests_path)
                parts.append(f"# File: {rel}\n")
                try:
                    with open(fpath, encoding="utf-8") as fh:
                        parts.append(fh.read())
                except Exception:
                    try:
                        with open(fpath, "rb") as fh:
                            data = fh.read()
                            parts.append(repr(data))
                    except Exception as e:
                        parts.append(f"# could not read file {rel}: {e}\n")
        return "\n".join(parts)

    def _parse_answer(self, answer: str, output_path: str) -> None:
        """Parse the LLM answer and write files to output_path.

        The answer is expected to contain multiple code snippets, each starting
        with a comment line indicating the file path, e.g.:

        ```
        # path/to/file.py
        <code>
        ```

        Files are written under `output_path` preserving the relative paths.
        """
        import os
        import re

        code_block_re = re.compile(r"```(?:python)?\n(.*?)\n```", re.DOTALL)
        path_re = re.compile(r"#\s*(.+)")

        matches = code_block_re.findall(answer)
        for match in matches:
            lines = match.strip().splitlines()
            if not lines:
                continue
            path_line = lines[0]
            path_match = path_re.match(path_line)
            if not path_match:
                continue
            rel_path = path_match.group(1).strip()
            code = "\n".join(lines[1:]).strip()
            if not code:
                continue
            full_path = os.path.join(output_path, rel_path)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, "w", encoding="utf-8") as fh:
                fh.write(code + "\n")
