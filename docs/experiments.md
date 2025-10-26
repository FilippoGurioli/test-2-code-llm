# Experiments

After the creation of the codebase many experiments were conducted to test the performance of the models and to find the best sweet spot of provided tests, prompt and model configuration.

## Setup

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

Finally, the upper bound has been set to 3 tries for each experiment in order to give the model multiple chances to generate correct code.

The total number of experiments is therefore:

```math
6 models * 7 test combinations * 3 case studies * 3 tries = 378 experiments
```

Note: this is the *worst case scenario*, since if the model is able to generate correct code in less than 3 tries the experiment ends earlier.

Best case scenario is:

```math
6 models * 7 test combinations * 3 case studies * 1 try = 126 experiments
```

A good estimate of the total number of experiments is the third quarter between the best and worst case scenarios:

```math
(378 - 126) * 0.75 + 126 = 315 experiments
```

## Data Collection

To collect the data from the experiments, the `experiment` command of the CLI tool has been used. The configuration files for each case study are stored under the `experiment-configs` directory.

Results have been collected in json format in order to be easily processable with python scripts for analysis and visualization.

## Improvements

During the experiments an improvement has been made to the core logic of the tool. Initially, the code generation engine was not aware of the previous test validation errors, thus each code generation was independent from the previous one. This caused problems in some cases, since the model could generate code that did not fix the previous errors. To solve this problem, the code generation engine has been modified to take into account the previous test validation errors. This has been done by passing the previous errors to the LLM as part of the prompt. This way, the model is aware of the previous errors and can generate code that fixes them.

## Automatic Experiments

To launch experiments automatically, over all the combination of models, test types and case studies, launch the following commands from the project root directory:

```bash
# source the virtual environment
source .venv/bin/activate

t2c experiment ./experiment-configs/low-complexity.yaml && \
t2c experiment ./experiment-configs/medium-complexity.yaml && \
t2c experiment ./experiment-configs/high-complexity.yaml
```

## Manual experiments

To better understand the performance of the models, some manual experiments have been conducted with available models online. In particular, the following models have been manually tested:

- ChatGPT-5
- Claude Sonnet 4.5
