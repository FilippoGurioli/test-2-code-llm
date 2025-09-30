# Architecture

The system architecture consists of several key components that work together to achieve the goal of generating code from test specifications using Large Language Models (LLMs).

## Command Line Interface

The front-end of the application faces directly to command line. This component is responsible of parsing the user input in order to launch the corresponding features in the later components. Here options are parsed and validated.

It also handles output messages such as informations, warnings and errors.

### Commands Design

#### Generate Command

The `generate` command is a one-shot command that performs a code generation with the specified configuration.

The command has been planned to be functional even with no configuration. The following is sufficient to let T2C do its job.

```bash
t2c generate
```

However it supports these configurations:

- `--tests`, `-t`: a path to the directory containing the test files;
- `--outout`, `-o`: a path to the directory that will contain the result;
- `--model`, `-m`: a string that describes what model to use;
- `--upperBound`, `-u`: the max number of tries the tool should do before returning a failure.

As said before, even no arguments could be passed. In that case the following values will be used:

- `--tests`: `.`;
- `--output`: `../result`;
- `--model`: `smollm2`;
- `--upperBound`: `3`.

#### Experiment Command

The experiment command is the one that performs experiments over many different llms. Its main capability is to report into a file the results gained during the experiments.

It takes as input a `yml` file in which all the configurations are set.

This is an comprehensive example of the file:

```yml
models:
    - ministral
    - DeepSeek R1
    - Smollm2
    - GitHub Copilot
    # other modles can be added here

testDirs:
    - ./unitTests
    - ./integrationTests
    - ./acceptanceTests
    # other directories can be added here

upperBound: 3

promptEng:
    - none
    - zeroShot
    - oneShot
    - fewShot
```

## Dispatcher

The dispatcher orchestrates the workflow by coordinating interactions between the other components. It receives input from the CLI, manages the flow of data, and ensures that each component performs its designated tasks in the correct sequence.

This component is also responsible for the automatic retry until a certain upper bound is reached.

## Model

This is the LLMs wrapper. It should exploit polimorphism to hide which model is actually working under the hood.

## Engine

This is the core of the application. It exploits LLMs to perform the code generation.
