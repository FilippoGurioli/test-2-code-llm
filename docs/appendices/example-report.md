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
                    "success": true
                },
                "test-validation": {
                    "time-taken": 4.2,
                    "passed-tests": 0,
                    "number-of-tests": 20,
                    "coverage": 85.0
                }
            }
        ]
    }
}
```
