# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

CoRex (Comment-based Review and Error Exploration System) is a Python project that analyzes code comments and explores errors. The project is in early development with minimal code infrastructure currently in place.

## Setup and Environment

This project uses `uv` for dependency management (Python 3.14+):

```bash
uv sync
source .venv/bin/activate
```

Pre-commit hooks are configured and should be installed:

```bash
pre-commit install
```

## Code Quality Tools

The project uses several automated code quality tools via pre-commit hooks:

- **ruff**: Linting and formatting (runs with `--fix` flag automatically)
- **ruff-format**: Code formatting
- **typos**: Spell checking
- **trailing-whitespace**: Removes trailing whitespace
- **check-added-large-files**: Prevents large file commits

Manual execution:

```bash
# Run all pre-commit hooks manually
pre-commit run --all-files

# Run ruff linting
ruff check --fix .

# Run ruff formatting
ruff format .
```

## Project Structure

```
CoRex/
├── corex/              # Main package directory
│   ├── agent.py        # Agent implementation (currently empty)
│   ├── main.py         # Main module (currently empty)
│   └── utils/          # Utility functions
├── experiments/        # Experimental code
│   ├── extract_py_comment.py   # Python comment extraction experiments
│   └── extract_cpp_comment.py  # C++ comment extraction experiments
├── prompt/             # Prompt templates
│   └── analysis_comment.md
└── main.py            # Entry point (prints "Hello from corex!")
```

## Dependencies

Core dependencies:
- **langchain** (>=1.0.3): LLM framework for building AI agents
- **pre-commit** (>=4.3.0): Git hook management
- **typos** (>=1.38.1): Spell checking

## Development Notes

- The project is in early stages with placeholder files in `corex/` directory
- `experiments/` contains research code for comment extraction from Python and C++ files
- The main application logic is not yet implemented
- Entry point is `main.py` which currently just prints a greeting

## Architecture

This appears to be an AI-powered code analysis tool leveraging LangChain for agent-based comment analysis and error exploration. The architecture involves:

- **Agent layer** (`corex/agent.py`): Will implement AI agents for code analysis
- **Main execution** (`corex/main.py`): Core application logic
- **Utilities** (`corex/utils/`): Supporting functions
- **Experiments**: Proof-of-concept code for comment extraction from multiple languages
