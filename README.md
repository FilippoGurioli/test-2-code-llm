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
  name: "experiment_1"
  output_dir: "./output"
  language: "python"
  upper_bound: 3

models:
  - "mistral"
  - "deepseek-r1"
  - "gemini"

test_kinds:
  - name: "UT"
    path: "./case_studies/tic_tac_toe/tests/unit"
  - name: "IT"
    path: "./case_studies/tic_tac_toe/tests/integration"
  - name: "AT"
    path: "./case_studies/tic_tac_toe/tests/acceptance"
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
2. **Connect Four** - Moderate complexity with gravity-based piece placement
3. **2048** - Higher complexity with merging tiles and scoring

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
├── core/             # Core business logic and models (code generation and test validation)
└── dispatcher/       # Command dispatching and handling
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
