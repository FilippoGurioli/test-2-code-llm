# Design

This section provides detailed design specifications for each component of the **Test 2 Code with LLMs (T2C)** system, focusing on internal structure, data flows, algorithms, and interfaces.

## CLI Handler

The CLI Handler implements a **Chain of Responsibility** for validation. It provides a clean separation between command parsing, validation, and execution delegation.

Since the execution logic is demanded to internal components, the CLI Handler focuses on argument parsing and validation. To achieve these functionalities, it employs two macro components:

- Parsing Pipeline;
- Validation Chain.

```mermaid
---
title: CLI Handler Overview
---
sequenceDiagram
    participant User
    participant CLIHandler
    participant ParsingPipeline
    participant ValidationChain
    participant Dispatcher

    User->>CLIHandler: t2c generate --tests ./my-tests
    CLIHandler->>ParsingPipeline: parse(arguments)
    ParsingPipeline-->>CLIHandler: Configuration
    CLIHandler->>ValidationChain: validate(Configuration)
    ValidationChain-->>CLIHandler: ValidationResult
    CLIHandler->>Dispatcher: execute(Configuration)
    Dispatcher-->>CLIHandler: ExecutionResult
    CLIHandler-->>User: display(ExecutionResult)
```

### Parsing Pipeline

To parse the command line arguments, 2 main steps are performed:

- Argument Parsing: to convert raw CLI input into structured data;
- Configuration Merging: to combine parsed arguments with defaults, config files, and environment variables.

### Validation Chain

The validation chain implements a series of validators that check different aspects of the configuration. Each validator can either pass the configuration to the next validator or return an error if validation fails.

The following validators are included:

- Command Validator: ensures the command is valid;
- Path Validator: checks if specified paths exist and are accessible;
- Model Validator: verifies if the specified LLM model is supported;
- Dependency Validator: ensures all required dependencies are installed;

### Final Class Diagram

```mermaid
---
  config:
    class:
      hideEmptyMembersBox: true
---
classDiagram
    class CLIHandler {
        -ArgumentParser parser
        -ConfigurationMerger config_merger
        -ChainValidator validator
        -Dispatcher dispatcher
        +parse_arguments(args[]) Configuration
        +validate_configuration(config) ValidationResult
        +execute_command(config) ExecutionResult
    }

    namespace ParsingPipeline {
        class ArgumentParser {
            +parse(args[]) Configuration
        }

        class ConfigurationMerger {
            +merge(parsed_args, defaults, file, env) Configuration
        }
    }

    namespace ValidationChain {
        class ChainValidator {
            -List~Validator~ validators
            +add_validator(validator)
            +validate(config) ValidationResult
        }

        class Validator {
            <<interface>>
            +validate(config) ValidationResult
        }

        class PathValidator {}
        class ModelValidator {}
        class DependencyValidator {}
        class CommandValidator {}
    }

    CLIHandler --> ChainValidator
    ChainValidator --> Validator
    Validator <|-- PathValidator
    Validator <|-- ModelValidator
    Validator <|-- DependencyValidator
    Validator <|-- CommandValidator
    CLIHandler --> Dispatcher
    CLIHandler --> ArgumentParser
    CLIHandler --> ConfigurationMerger
```

### Detailed Processing Steps

```mermaid
sequenceDiagram
    participant User
    participant CLIHandler
    participant ArgumentParser
    participant ConfigurationMerger
    participant ChainValidator
    participant Dispatcher

    User->>CLIHandler: t2c generate --tests ./my-tests
    CLIHandler->>ArgumentParser: parse(["generate", "--tests", "./my-tests"])
    ArgumentParser-->>CLIHandler: ParsedArguments(command="generate", args={...})

    CLIHandler->>ConfigurationMerger: merge(parsed_args, defaults, file, env)
    ConfigurationMerger-->>CLIHandler: Configuration(tests="./my-tests", ...)

    CLIHandler->>ChainValidator: validate(configuration)
    ChainValidator-->>CLIHandler: ValidationResult(valid=true)

    CLIHandler->>Dispatcher: launch_command(configuration)
    Dispatcher-->>CLIHandler: Result(success=true, details={...})
```

## Dispatcher

The goal of the dispatcher is to delegate the execution of commands to the appropriate command handler based on user input. To do that, the dispatcher exploits the **Command Pattern** to encapsulate requests as objects and a **Service Locator** to retrieve later components' instances.

```mermaid
---
  config:
    class:
      hideEmptyMembersBox: true
---
classDiagram
    class CommandFactory {
        -ComponentLocator component_locator
        -Map~String, Command~ commands
        +get_command(name) Command
        +list_commands() String[]
    }

    class Command {
        <<interface>>
        +execute(config) ExecutionResult
        +get_help_text() String
    }

    class GenerateCommand {}

    class ExperimentCommand {}

    class ComponentLocator {
        -Map~String, T~ components
        +register~T~(name, instance)
        +get(name) T
    }

    CLIHandler --> CommandFactory
    CommandFactory --> Command
    Command <|-- GenerateCommand
    Command <|-- ExperimentCommand
    ExperimentCommand --> ComponentLocator
    GenerateCommand --> ComponentLocator
```

## Code Generation Engine

The Code Generation Engine is responsible for generating code based on provided test specifications using Large Language Models (LLMs). It exploits the **Strategy Pattern** to support multiple LLM providers and the **Factory Pattern** to instantiate the appropriate strategy based on user configuration.

```mermaid
---
  config:
    class:
      hideEmptyMembersBox: true
---
classDiagram
    class CodeGenerationEngine {
        -LLMProviderInterface llm_provider
        -List~CodeGenerationObserver~ observers
        +generate_code(tests, config) CodeResult
        +subscribe(observer) void
        +unsubscribe(observer) void
    }
    class LLMProviderInterface {
        <<interface>>
        +generate_code(prompt, config) CodeResult
    }
    class LLMProviderFactory {
        +create_provider(name) LLMProviderInterface
    }
    class Dispatcher {}
    Dispatcher --> CodeGenerationEngine
    CodeGenerationEngine --> LLMProviderInterface
    LLMProviderFactory --> LLMProviderInterface
    LLMProviderInterface <|-- MistralProvider
    LLMProviderInterface <|-- DeepSeekR1Provider
    LLMProviderInterface <|-- Smollm2Provider
    LLMProviderInterface <|-- Qwen3Provider
    LLMProviderInterface <|-- GitHubCopilotProvider
    LLMProviderInterface <|-- GeminiFlashProvider
```

## Execution Validator

The Execution Validator is responsible for executing the generated code against the provided test suite in a sandboxed environment. It ensures that the generated code meets the functional requirements specified by the tests.

```mermaid
---
  config:
    class:
      hideEmptyMembersBox: true
---
classDiagram
    class ExecutionValidator {
        -SandboxEnvironment sandbox
        -String language
        +execute_code(generated_code, test_suite) void
        +subscribe(observer) void
        +unsubscribe(observer) void
    }

    class SandboxEnvironment {
        +run(code, tests) ExecutionResult
    }

    class ExecutionResult {
        -Boolean success
        -String output
        -String error
        +is_successful() Boolean
        +get_output() String
        +get_error() String
    }

    ExecutionValidator --> SandboxEnvironment
    SandboxEnvironment --> ExecutionResult
```

## Experiment Manager

The logic for the experiment manager will already be included into the [`ExperimentCommand`](#dispatcher). Therefore no design is needed for this component.

## Reporting Engine

The Reporting Engine is responsible for actively collecting, tracking, and analyzing metrics throughout the code generation process. It implements the **Observer Pattern** to monitor events and the **Strategy Pattern** to construct comprehensive reports.

```mermaid
---
  config:
    class:
      hideEmptyMembersBox: true
---
classDiagram
    class ReportingEngine {
        -CollectStrategy collect_strategy
        -List~CodeGenStat~ statistics
        +log_report() void
    }

    class CodeGenerationObserver {
        <<interface>>
        +on_code_generation_start(model_name, test_suite) void
        +on_code_generation(is_failed) void
    }

    class CodeValidationObserver {
        <<interface>>
        +on_code_validation_start(model_name, test_suite) void
        +on_code_validation(is_failed) void
        +on_test_metrics_measured(test_pass_rate, coverage) void
    }

    class CollectStrategy {
        <<interface>>
        +collect(code_gen_stat) void
    }

    class CodeGenStat {
        -String model_name
        -String test_suite
        -Boolean generation_success
        -Boolean validation_success
        -Float test_pass_rate
        -Float coverage
        -Duration time_taken
    }

    CodeGenerationEngine --> CodeGenerationObserver
    ExecutionValidator --> CodeValidationObserver
    CodeGenerationObserver <|-- ReportingEngine
    CodeValidationObserver <|-- ReportingEngine
    ReportingEngine --> CollectStrategy
    ReportingEngine --> CodeGenStat
    CollectStrategy <|-- ConsoleCollector
    CollectStrategy <|-- JsonCollector
    CollectStrategy <|-- CsvCollector
```
