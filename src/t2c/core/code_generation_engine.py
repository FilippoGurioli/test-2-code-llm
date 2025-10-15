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

    def generate_code(self, tests_path: str, output_path: str) -> bool:
        self._notify_start()
        tests: str = self._serialize_tests(tests_path)
        query: str = self._get_query("python", tests)  # TODO
        try:
            answer: str = self._llm_provider.query(query)
        except Exception as e:
            self._notify_end(str(e))
            return False
        print(answer)
        self._parse_answer(answer, output_path)
        self._notify_end()
        return True

    def _notify_start(self) -> None:
        for obs in self._observers:
            obs.on_code_generation_start()

    def _notify_end(self, error: str = "") -> None:
        for obs in self._observers:
            obs.on_code_generation_end(error if error != "" else None)

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

        code_block_re = re.compile(r"```(?:\w+)?\n(.*?)\n```", re.DOTALL)
        path_re = re.compile(r"#\s*(File:)?(.+)")

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

    def _get_query(self, lang: str, tests: str) -> str:
        query: str = f"Generate {lang} source code that satisfies the following tests. "
        query += "Don't include any explanation, just the code. "
        query += "Don't generate tests, only the source code. "
        query += f"Remember to generate the main method and file too.\n\n{tests}"
        query += "\n\nFor each file, make sure to:\n"
        query += "- include a comment on top with the file path like this: # path/to/file.py\n"
        query += "- insert them in different code snippets (use triple backticks)"


# """
# Generate Python source code that satisfies the following tests.
# Do not include any explanation or extra text — only the code.
# Do not generate tests, only the source code.

# Include the main entry point if needed.

# The tests are:
# {tests}

# For each file:
# - Start with a comment line showing the file path, e.g.: # path/to/file.py
# - Put each file in its own triple-backtick code block with the language specified:
#   ```python
#   # path/to/file.py
#   <code>
#   ```

#     Do not merge multiple files into a single code block.
#         return query
# """
