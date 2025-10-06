# Architecture

The system architecture consists of several key components that work together to achieve the goal of generating code from test specifications using Large Language Models (LLMs).

## Overall Diagram

```mermaid
flowchart TD
    User([User]) -->|commands| CLI[CLI Handler]
    CLI -->|triggers| Dispatcher[Dispatcher]
    CLI -->|loads| CM[Configuration Manager]
    subgraph CoreComponents[Core Components]
      EM
      EV
      CGE
      ARE
    end
    Dispatcher -->|orchestrates| EM[Experiment Manager]
    Dispatcher -->|dispatches| CGE[Code Generation Engine]
    Dispatcher -->|validates| EV[Execution Validator]
    EV -->|output results| ARE
    EV -->|executes| Sandbox[Sandboxed Environment]
    CGE -->|perf results| ARE[Reporting Engine]
    EM -->|uses many| CGE
    Sandbox --> TestRunner[Test Runners]
    CGE -->|generated code| EV
    CGE -->|API calls| LLM@{ shape: procs, label: "LLM Providers"}
    LLM -->|responses| CGE
    
    ARE -.-> Reports[(Report Files)]
    ARE -.-> Console[/Console Output/]
```

## Command Line Interface Helper

The front-end of the application faces directly to command line. This component is responsible of parsing the user input in order to launch the corresponding features in the later components.

It features 2 main commands: `generate` and `experiment`.

### Generate Command

The `generate` command that performs a one-shot code generation with the specified configuration.

The command has been planned to be functional even with no configuration. The following is sufficient to let T2C do its job.

```bash
t2c generate
```

However it supports these options:

- `--tests`, `-t`: a path to the directory containing the test files;
- `--output`, `-o`: a path to the directory that will contain the result;
- `--model`, `-m`: a string that describes what model to use;
- `--upperBound`, `-u`: the max number of tries the tool should do before returning a failure.

As said before, even no arguments could be passed. In that case the following values will be used:

- `--tests`: `.`;
- `--output`: `../result`;
- `--model`: `smollm2`;
- `--upperBound`: `3`.

### Experiment Command

The experiment command is the one that performs experiments over many different LLMs. It performs multiple runs with different configurations and collects detailed metrics on the performance of each model and tests adopted.

It takes as input a `yml` file in which all the configurations are set.

```bash
t2c experiment config.yml
```

This is a comprehensive example of the file:

```yaml
experiment:
  name: "T2C Comparative Study"
  output_dir: "./experiments/results"
  
models:
  - "mistral"
  - "smollm2"
  - "github-copilot"

test_suites:
  - name: "unit_tests"
    path: "./tests/unit"
    language: "python"
  - name: "integration_tests"
    path: "./tests/integration"
    language: "python"

strategies:
  max_retries: [1, 3, 5]
  matrix_testing: true # to combine multiple test suites in a single run
```

## Configuration Manager

This component is responsible of loading and validating the configuration file passed to the experiment command. It also provides default values for missing configurations.

## Dispatcher

The dispatcher orchestrates the workflow by coordinating interactions between the other core components. It receives input from the CLI and ensures that each component performs its designated tasks in the correct sequence.

## Experiment Manager

This component is responsible of managing the experiments. It takes care of combining the different configurations in order to create a list of experiments to be run. It also handles the output directory structure for the results.

## Reporting Engine

It is responsible of handling the information gained from the code generation engine's runs. It features both dumping to console standard output and/or error and to a file.

It provides insights on the following metrics:

- generation success rates by model/tests;
- time taken for generation;
- coverage;
- test pass rates.

## Code Generation Engine

It's the core of the application. It exploits an LLM to perform the code generation while dumping useful statistics during and at the end of the process.

## LLM Provider Interface

This component abstracts the interactions with various LLM providers, allowing the system to switch between different models seamlessly. It handles API calls, manages authentication, and processes responses from the LLMs.

## Execution Validator

It exploits a sandboxed environment to execute the generated code against the provided test suite.

## Feedback Loop Sequence

```mermaid
sequenceDiagram
    actor User
    participant CLI as CLI Handler
    participant Dispatcher
    participant CGE as Code Generation Engine
    participant LLM as LLM Provider
    participant EV as Execution Validator
    participant ARE as Reporting Engine
    
    User ->> CLI: run "t2c generate"
    CLI ->> Dispatcher: trigger generation
    loop retries until success or upperBound
        Dispatcher ->> CGE: request code
        CGE ->> LLM: generate code
        LLM -->> CGE: return code
        CGE -->> Dispatcher: generated code
        Dispatcher ->> EV: send code for validation
        EV -->> Dispatcher: pass/fail result
        CGE ->> ARE: send results & metrics
        EV ->> ARE: send results & metrics
    end
    ARE -->> User: report outcome
```
