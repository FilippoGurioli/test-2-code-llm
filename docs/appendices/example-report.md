# Example report

This is how the json report looks like:

```json
{
    "ATxUTxIT-gemini-20251015_160555": {
        "model": "gemini",
        "language": "python",
        "attempts": 3,
        "runs": [
            {
                "code-generation": {
                    "time-taken": 14.5,
                    "success": true,
                    "error": null
                },
                "test-validation": {
                    "time-taken": 4.2,
                    "passed-tests": 0,
                    "number-of-tests": 20,
                    "error": null,
                    "coverage": 85.0
                }
            }
        ]
    }
}
```

```yaml
experiment:
  name: "low-complexity-generation"
  output_dir: "./experiments/results"
  language: "python"
  upper_bound: 3

models:
  - "mistral"
  - "smollm2"
  - "llama3"

test_kinds:
  - name: "unit_tests"
    path: "./tests/unit"
  - name: "integration_tests"
    path: "./tests/integration"
  - name: "acceptance_tests"
    path: "./tests/acceptance"
```
