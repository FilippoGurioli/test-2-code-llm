# Experiments

After the creation of the codebase many experiments were conducted to test the performance of the models and to find the best sweet spot of provided tests, prompt and model configuration.

## Strategy

For each case study it has been created 3 different sets of tests:

- unit
- integration
- acceptance

Each model has been tested with all combinations of the above tests, for a total of 7 different combinations:

1. Unit tests only
2. Integration tests only
3. Acceptance tests only
4. Unit + Integration tests
5. Unit + Acceptance tests
6. Integration + Acceptance tests
7. Unit + Integration + Acceptance tests

As explained in the [introduction](introduction.md#project-objectives), the models that have been tested are:

- Mistral
- DeepSeek R1
- Smollm2
- Qwen3
- Llama3
- Gemini Flash (until the API free tier limits)

Each model has been tested with the *default configuration* due to the high number of experiments to be done.

The total number of experiments is therefore:

```math
6 models * 7 test combinations * 3 case studies = 126 experiments
```

## Data Collection

To collect the data from the experiments, the `experiment` command of the CLI tool has been used. The configuration files for each case study are stored under the `experiment-configs` directory.

Results have been collected in json format in order to be easily processable with python scripts for analysis and visualization.

### Manual experiments

To better understand the performance of the models, some manual experiments have been conducted with available models online. In particular, the following models have been manually tested:

- ChatGPT-5
- Claude Sonnet 4.5
