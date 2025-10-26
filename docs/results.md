# Results

Simple python scripts have been created in order to do analysis over data scraped during experiments.

The scripts can be found in the `data-analysis` directory.

## Objective

The main objectives in the analysis were to obtain the best llm able to generate the best code that fits the tests.

Moreover, it was searched the best test type that let most llm succeed in the code generation.

## Results Analysis Criteria

From the objectives it was then derived the results analysis strategy.

### The best LLM

To create a ranking it was exploited a weighted formula based on performance metrics:

| Metric                    | Description                                            | Weight |
| :------------------------ | :----------------------------------------------------- | :----: |
| **Success Rate**          | Whether the model successfully generated runnable code |  0.4   |
| **Pass Rate**             | Percentage of passed test cases                        |  0.4   |
| **Average Coverage**      | Code coverage percentage achieved by generated code    |  0.2   |
| **Normalized Time Taken** | Penalization for longer generation times               |  -0.1  |

The final ranking formula was indeed:

```math
score = 0.4 * success + 0.4 * pass + 0.2 * coverage - 0.1 * normalizedTime
```

Normalized time is refered as the time taken for that code gneration devided by the longest code generation of that kind.

Weight can be adjusted in the script `data-analysis/rank.py` depending on the analysis needs. For this analysis the weights have been kept as above in order to give more importance to correctness of the generated code rather than performance.

## Score Table

| Complexity | Test kind | LLM         | Score  |
| ---------- | --------- | ----------- | ------ |
| LOW        | IT        | gemini      | 19.998 |
| LOW        | AT        | gemini      | 18.8   |
| HIGH       | IT        | gemini      | 18.4   |
| HIGH       | ATxIT     | gemini      | 18.2   |
| MEDIUM     | AT        | gemini      | 18     |
| HIGH       | AT        | gemini      | 17.4   |
| MEDIUM     | ATxIT     | gemini      | 10.433 |
| LOW        | AT        | qwen3       | 9.514  |
| MEDIUM     | ITxUT     | gemini      | 7.26   |
| LOW        | IT        | smollm2     | 0.797  |
| LOW        | ATxITxUT  | smollm2     | 0.795  |
| HIGH       | ATxITxUT  | smollm2     | 0.783  |
| HIGH       | ATxUT     | mistral     | 0.782  |
| MEDIUM     | ATxITxUT  | mistral     | 0.781  |
| MEDIUM     | ATxITxUT  | smollm2     | 0.78   |
| HIGH       | ATxITxUT  | mistral     | 0.779  |
| LOW        | ATxUT     | smollm2     | 0.778  |
| LOW        | ITxUT     | smollm2     | 0.778  |
| HIGH       | ATxUT     | smollm2     | 0.777  |
| MEDIUM     | UT        | smollm2     | 0.776  |
| MEDIUM     | ATxUT     | llama3      | 0.776  |
| MEDIUM     | ATxITxUT  | llama3      | 0.776  |
| LOW        | ATxITxUT  | llama3      | 0.776  |
| MEDIUM     | ATxUT     | smollm2     | 0.775  |
| MEDIUM     | ITxUT     | llama3      | 0.775  |
| HIGH       | ATxUT     | llama3      | 0.775  |
| HIGH       | ATxIT     | smollm2     | 0.775  |
| HIGH       | UT        | smollm2     | 0.774  |
| HIGH       | ITxUT     | mistral     | 0.774  |
| LOW        | ITxUT     | mistral     | 0.773  |
| LOW        | ATxITxUT  | mistral     | 0.773  |
| HIGH       | ITxUT     | llama3      | 0.773  |
| HIGH       | ATxITxUT  | llama3      | 0.773  |
| LOW        | ATxUT     | llama3      | 0.772  |
| LOW        | ATxITxUT  | deepseek-r1 | 0.771  |
| LOW        | ITxUT     | llama3      | 0.77   |
| MEDIUM     | ITxUT     | mistral     | 0.769  |
| LOW        | UT        | smollm2     | 0.769  |
| MEDIUM     | ATxUT     | mistral     | 0.768  |
| MEDIUM     | UT        | llama3      | 0.767  |
| HIGH       | ITxUT     | deepseek-r1 | 0.767  |
| HIGH       | ATxITxUT  | deepseek-r1 | 0.767  |
| HIGH       | ATxIT     | llama3      | 0.766  |
| HIGH       | UT        | mistral     | 0.765  |
| MEDIUM     | ATxITxUT  | qwen3       | 0.764  |
| LOW        | ITxUT     | deepseek-r1 | 0.764  |
| HIGH       | ATxITxUT  | qwen3       | 0.764  |
| LOW        | ATxIT     | smollm2     | 0.763  |
| MEDIUM     | UT        | mistral     | 0.762  |
| MEDIUM     | ATxITxUT  | deepseek-r1 | 0.762  |
| LOW        | UT        | llama3      | 0.762  |
| LOW        | ATxUT     | mistral     | 0.762  |
| LOW        | ATxIT     | llama3      | 0.761  |
| HIGH       | ITxUT     | qwen3       | 0.761  |
| MEDIUM     | IT        | gemini      | 0.76   |
| LOW        | ATxIT     | mistral     | 0.758  |
| HIGH       | ATxIT     | mistral     | 0.758  |
| LOW        | ATxUT     | qwen3       | 0.757  |
| HIGH       | ATxUT     | qwen3       | 0.757  |
| MEDIUM     | ITxUT     | deepseek-r1 | 0.756  |
| MEDIUM     | ATxUT     | qwen3       | 0.755  |
| HIGH       | ATxUT     | deepseek-r1 | 0.755  |
| MEDIUM     | ATxIT     | smollm2     | 0.753  |
| LOW        | ITxUT     | qwen3       | 0.753  |
| MEDIUM     | ITxUT     | qwen3       | 0.752  |
| HIGH       | IT        | llama3      | 0.752  |
| HIGH       | IT        | smollm2     | 0.752  |
| MEDIUM     | ATxIT     | llama3      | 0.751  |
| LOW        | IT        | llama3      | 0.75   |
| HIGH       | ATxUT     | gemini      | 0.75   |
| LOW        | IT        | mistral     | 0.748  |
| HIGH       | IT        | mistral     | 0.748  |
| HIGH       | ATxIT     | deepseek-r1 | 0.748  |
| LOW        | ATxIT     | deepseek-r1 | 0.747  |
| MEDIUM     | ATxIT     | mistral     | 0.746  |
| MEDIUM     | ITxUT     | smollm2     | 0.746  |
| MEDIUM     | ATxIT     | deepseek-r1 | 0.742  |
| HIGH       | ATxIT     | qwen3       | 0.741  |
| MEDIUM     | ATxUT     | deepseek-r1 | 0.74   |
| LOW        | ATxITxUT  | gemini      | 0.738  |
| HIGH       | ITxUT     | smollm2     | 0.737  |
| LOW        | ATxIT     | qwen3       | 0.735  |
| LOW        | ATxIT     | gemini      | 0.733  |
| LOW        | IT        | qwen3       | 0.728  |
| HIGH       | IT        | qwen3       | 0.728  |
| LOW        | ATxUT     | deepseek-r1 | 0.726  |
| MEDIUM     | ATxIT     | qwen3       | 0.723  |
| MEDIUM     | IT        | smollm2     | 0.718  |
| MEDIUM     | IT        | llama3      | 0.717  |
| HIGH       | AT        | llama3      | 0.717  |
| HIGH       | AT        | smollm2     | 0.715  |
| MEDIUM     | IT        | mistral     | 0.713  |
| HIGH       | AT        | mistral     | 0.707  |
| MEDIUM     | AT        | llama3      | 0.698  |
| MEDIUM     | AT        | smollm2     | 0.698  |
| MEDIUM     | IT        | qwen3       | 0.697  |
| LOW        | ITxUT     | gemini      | 0.695  |
| MEDIUM     | AT        | mistral     | 0.69   |
| HIGH       | AT        | qwen3       | 0.69   |
| MEDIUM     | AT        | qwen3       | 0.675  |
| LOW        | AT        | smollm2     | 0.665  |
| LOW        | AT        | llama3      | 0.663  |
| LOW        | AT        | mistral     | 0.663  |
| HIGH       | UT        | llama3      | 0.66   |
| LOW        | ATxUT     | gemini      | 0.659  |
| HIGH       | UT        | gemini      | 0.638  |
| LOW        | UT        | gemini      | 0.628  |
| MEDIUM     | UT        | gemini      | 0.622  |
| MEDIUM     | ATxITxUT  | gemini      | 0.616  |
| LOW        | ATxITxUT  | qwen3       | 0.615  |
| MEDIUM     | UT        | qwen3       | 0.575  |
| MEDIUM     | ATxUT     | gemini      | 0.568  |
| LOW        | UT        | mistral     | 0.539  |
| HIGH       | ITxUT     | gemini      | 0.428  |
| LOW        | UT        | qwen3       | 0.414  |
| HIGH       | UT        | qwen3       | 0.414  |
| HIGH       | ATxITxUT  | gemini      | 0.412  |
| LOW        | IT        | deepseek-r1 | 0.409  |
| MEDIUM     | UT        | deepseek-r1 | -0.1   |
| MEDIUM     | IT        | deepseek-r1 | -0.1   |
| MEDIUM     | AT        | deepseek-r1 | -0.1   |
| LOW        | UT        | deepseek-r1 | -0.1   |
| LOW        | AT        | deepseek-r1 | -0.1   |
| HIGH       | UT        | deepseek-r1 | -0.1   |
| HIGH       | IT        | deepseek-r1 | -0.1   |
| HIGH       | AT        | deepseek-r1 | -0.1   |

## Overall Observations

- Smollm2, llama3 and mistral consistently shows stable performance across all complexity levels and test types (score around 0.75-0.78).
- Gemini exhibits high variability, achieving top scores in IT and AT tests but very low in UT.
- Qwen3 performs moderately well but rarely leads any category.
- Deepseek-r1 generally underperforms compared to other LLMs, often scoring negative (i.e. code generation failed) or very low values.

## Insights

### Low Complexity

- Gemini dominates IT and AT contexts, achieving coverage near 90-96% and exceptional scores (~19).
- Smollm2 and llama3 are top performers in UT and multi-test scenarios (ATxITxUT).
- Deepseek-r1 fails to perform well in isolation but improves when evaluated jointly with other contexts (slight positive scores).

### Medium Complexity

- Gemini still leads in IT and AT, though with slightly reduced scores (~18).
- Smollm2, llama3, and mistral maintain balanced and strong performance across composite contexts (e.g., ATxITxUT, ATxUT).
- Mistral slightly outperforms others in the ATxITxUT configuration, indicating better adaptability as complexity rises.

### High Complexity

- Gemini continues to excel in IT and AT contexts (scores ~17-18, high coverage).
- In UT and multi-context settings, smollm2 and mistral regain dominance, showing best overall stability.
- Deepseek-r1 achieves limited improvements in composite evaluations, suggesting that aggregation mitigates isolated weaknesses.

## Manual testing Results

As said before, it has been done some manual testing on GPT-5 and Claude Sonnet 4.5. As one might expect, both models performed very well, often achieving 100% correctness in code generation across all complexity levels and test types. This confirms the trend observed in automatic experiments, where more advanced models tend to perform better in code generation tasks. They have not been included in the ranking table since the experiments were not automated and thus not comparable with the other results.

Differently from automatic testing, in these cases there was some manual help in case of model failure, by providing localized hints to the model about the errors found in the generated answer.

## Conclusions

It must be noted that the results are biased by the fact that they should reflect an overall performance indicator over heterogeneous values (coverage, correctness, time ...).

In a real world scenario, the importance of each metric may vary depending on the specific use case. In a cooperative coding scenario, where developer provides tests to the LLM, it should be considered a failure everything but 100% pass rate. In this case all weights should be substituted with 0, except for pass rate that should be set to 1. This is exactly the case of inserting t2c into a CI/CD pipeline where only correctness matters. In this case, the ranking sees gemini and smollm2 as the only models able to reach 100% correctness in *some* configuration. In particular:

| Complexity | Test kind | LLM     |
| ---------- | --------- | ------- |
| LOW        | IT        | smollm2 |
| LOW        | ATxITxUT  | smollm2 |
| LOW        | IT        | gemini  |
| LOW        | AT        | gemini  |
| MEDIUM     | AT        | gemini  |
| HIGH       | IT        | gemini  |
| HIGH       | AT        | gemini  |
| HIGH       | ATxIT     | gemini  |

---

It is also interesting to note how test types influence the results. In particular, IT and AT seems to be the best test types able to guide the LLMs towards correct code generation. This is probably due to the fact that these test types provide more context about the expected behavior of the code, rather than just isolated unit tests. Another plausible reason is that LLMs are generally better at understanding higher-level requirements (integration and acceptance) rather than low-level unit tests.

Finally it is worth noticing how complexity affects the results. As expected, as complexity increases, the performance of all LLMs tends to decrease. However, some models like smollm2 and mistral show more resilience to increasing complexity, maintaining relatively stable performance across different complexity levels. This suggests that these models may have better generalization capabilities, allowing them to handle more complex coding tasks effectively.
