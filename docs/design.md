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

- Path Validator: checks if specified paths exist and are accessible;
- Model Validator: verifies if the specified LLM model is supported;
- Dependency Validator: ensures all required dependencies are installed;
- Resource Validator: checks if sufficient resources (e.g., memory, CPU) are available.

### Final Class Diagrams

```mermaid
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
    
    CLIHandler --> Dispatcher
    CLIHandler --> ValidationChain
    CLIHandler --> ArgumentParser
    CLIHandler --> ConfigurationMerger
```

```mermaid
classDiagram
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
        class ResourceValidator {}
    }
    
    CLIHandler --> ChainValidator
    ChainValidator --> Validator
    Validator <|-- PathValidator
    Validator <|-- ModelValidator
    Validator <|-- DependencyValidator
    Validator <|-- ResourceValidator
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
    
    CLIHandler->>Dispatcher: get_command("generate")
    Dispatcher-->>CLIHandler: GenerateCommand instance
```

## Dispatcher

The goal of the dispatcher is to delegate the execution of commands to the appropriate command handler based on user input. To do that, the dispatcher exploits the **Command Pattern** to encapsulate requests as objects and a **Service Locator** to retrieve later components' instances.

```mermaid
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
        -Map~String, Component~ components
        +register(name, instance)
        +get(name) Component
    }

    class Component {
        <<interface>>
        +perform_task() Result
    }

    CLIHandler --> CommandFactory
    CommandFactory --> Command
    Command <|-- GenerateCommand
    Command <|-- ExperimentCommand
    ExperimentCommand --> ComponentLocator
    GenerateCommand --> ComponentLocator
    ComponentLocator --> Component
```
