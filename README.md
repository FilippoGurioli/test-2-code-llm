# Test 2 Code with LLMs (T2C)

**T2C** is an academic research project that explores the capabilities of Large Language Models (LLMs) in generating code from test specifications. Developed for the *Advanced Software Modeling and Design* course at the University of Bologna, T2C demonstrates how AI can shift the developer's role from code writer to test specification provider.

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/FilippoGurioli/test-2-code-llm.git
cd test-2-code-llm

# Install in development mode
make install-dev

# Verify installation
t2c --help
```

### Basic Usage

**Single Code Generation:**

```bash
# Generate code from tests in current directory
t2c generate

# Specify custom paths and model
t2c generate --tests ./my-tests --output ./generated --model mistral
```

**Experimental Comparison:**

```bash
# Run comparative experiment across multiple models
t2c experiment config/comparative_study.yml
```

Example experiment configuration:

```yaml
experiment:
  name: "T2C Comparative Study"
  output_dir: "./experiments/results"

models:
  - "mistral"
  - "smollm2"
  - "llama3"

test_suites:
  - name: "unit_tests"
    path: "./tests/unit"
    language: "python"
  - name: "integration_tests"
    path: "./tests/integration"
    language: "python"

strategies:
  max_retries: [1, 3, 5]
  matrix_testing: true
```

## Supported LLM Models

T2C evaluates and compares multiple language models:

| Model            | Provider     | Type        | API Support |
| ---------------- | ------------ | ----------- | ----------- |
| **Mistral**      | Mistral AI   | Open-source | ✅           |
| **DeepSeek R1**  | DeepSeek     | Commercial  | ✅           |
| **Smollm2**      | Hugging Face | Open-source | ✅           |
| **Qwen3**        | Alibaba      | Open-source | ✅           |
| **Llama3**       | Meta         | Open-source | ✅           |
| **Gemini Flash** | Google       | Commercial  | ✅           |

## Case Studies

The project evaluates LLM performance on increasingly complex software projects:

1. **Tic Tac Toe** - Simple game logic and state management
2. **Snake Game** - Moderate complexity with real-time interaction
3. **Space Invaders** - Higher complexity with graphics and physics

## Development

### Development Setup

```bash
# Install development dependencies
make install-dev

# Run tests
make test

# Format code
make format

# Type checking
make type-check
```

### Project Structure

```text
src/t2c/
├── cli/              # Command-line interface components
├── core/             # Core business logic and models
├── engines/          # Code generation, validation, reporting
├── experiments/      # Experiment management and execution
├── config/           # Configuration and settings management
└── utils/            # Shared utilities and helpers
```

## Documentation

Comprehensive documentation is available at the project's [GitHub Pages](https://filippogurioli.github.io/test-2-code-llm/).

## Contributing

This is an academic project, but contributions and suggestions are welcome:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/feature`)
3. Commit your changes (`git commit -m 'Add feature'`)
4. Push to the branch (`git push origin feature/feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
