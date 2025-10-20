"""Module implementing the code generation engine."""

import os
import re

from t2c.core.llm_provider.interface import LLMProviderInterface
from t2c.core.reporting.observers.code_generation_observer import CodeGenerationObserver


class CodeGenerationEngine:
    """The code generation engine responsible for generating code using an LLM provider."""

    def __init__(self, llm_provider: LLMProviderInterface) -> None:
        self._llm_provider: LLMProviderInterface = llm_provider
        self._observers: list[CodeGenerationObserver] = []
        self._chat_history: list[dict[str, str]] = [
            {
                "role": "system",
                "content": "You are a helpful assistant that generates code based on provided tests.",
            }
        ]

    def subscribe(self, observer: CodeGenerationObserver) -> None:
        self._observers.append(observer)

    def unsubscribe(self, observer: CodeGenerationObserver) -> None:
        self._observers.remove(observer)

    def generate_code(
        self, lang: str, tests_path: str, output_path: str, validation_error: str | None
    ) -> bool:
        """It launches a code generation based on the provided tests and previous errors. It dumps all the generated code into the output directory.

        Args:
            lang (str): the programming language to generate code in
            tests_path (str): the path to the tests
            output_path (str): the path where to dump the generated code
            validation_error (str | None): the validation error from the previous attempt

        Returns:
            bool: if the code generation was successful
        """
        self._notify_start()
        if validation_error is not None:
            self._chat_history.append(
                {"role": "user", "content": self._get_retry_query(validation_error)}
            )
        else:
            query: str = self._get_query(lang, self._serialize_tests(tests_path))
            self._chat_history.append({"role": "user", "content": query})
        try:
            answer: str = self._llm_provider.query(self._chat_history)
            self._chat_history.append({"role": "assistant", "content": answer})
        except Exception as e:
            self._notify_end(str(e))
            return False
        self._dump_to_file(answer, output_path)
        self._notify_end()
        return True

    def _notify_start(self) -> None:
        for obs in self._observers:
            obs.on_code_generation_start()

    def _notify_end(self, error: str = "") -> None:
        for obs in self._observers:
            obs.on_code_generation_end(
                self._chat_history, error if error != "" else None
            )

    def _serialize_tests(self, tests_path: str) -> str:
        """Read and concatenate test files under `tests_path`.

        Walk the directory recursively, skipping hidden files and `__pycache__`.
        For each file emit a header with the relative path and the file contents
        decoded as UTF-8 (binary fallback uses repr).
        """

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

    def _dump_to_file(self, answer: str, output_path: str) -> None:
        """Parse the LLM answer and write files to output_path.

        The answer is expected to contain multiple code snippets, each starting
        with a comment line indicating the file path, e.g.:

        ```
        # path/to/file.py
        <code>
        ```
        """

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
            rel_path = path_match.group(2).strip()
            code = "\n".join(lines[1:]).strip()
            if not code:
                continue
            full_path = os.path.join(output_path, rel_path)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, "w", encoding="utf-8") as fh:
                fh.write(code + "\n")

    def _get_query(self, lang: str, tests: str) -> str:
        query: str = (
            f"Generate {lang} source code that satisfies the following tests.\n"
        )
        query += "Do not include any explanation or extra text — only the code.\n"
        query += "Do not merge multiple files into a single code block.\n"
        query += "Do not generate tests, only the source code.\n\n"
        query += "Include the main entry point if needed.\n\n"
        query += f"The tests are:\n{tests}\n\n"
        query += "For each file:\n"
        query += "- Start with a comment on top with the file path like this: # path/to/file.py\n"
        query += "- Put each file in its own triple-backtick code block with the language specified:\n"
        query += "  ```python\n"
        query += "  # path/to/file.py\n"
        query += "  <code>\n"
        query += "  ```\n\n"
        return query

    def _get_retry_query(self, validation_error: str) -> str:
        retry_query: str = (
            "The previously generated code did not pass the tests due to the following error:\n\n"
        )
        retry_query += f"{validation_error}\n\n"
        retry_query += "Fix the code accordingly. Remember to:\n"
        retry_query += "- Not include any explanation or extra text — only the code.\n"
        retry_query += "- Not merge multiple files into a single code block.\n"
        retry_query += "- Not generate tests, only the source code.\n\n"
        retry_query += "For each file:\n"
        retry_query += "- Start with a comment on top with the file path like this: # path/to/file.py\n"
        retry_query += "- Put each file in its own triple-backtick code block with the language specified:\n"
        retry_query += "  ```python\n"
        retry_query += "  # path/to/file.py\n"
        retry_query += "  <code>\n"
        retry_query += "  ```\n\n"
        return retry_query
