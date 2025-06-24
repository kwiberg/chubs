# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is `chubs`, a simple Python script that generates XKCD-style passwords (passphrases) from word lists. The script analyzes text files to extract valid words and creates secure passphrases with a specified entropy level.

## Development Commands

### Dependencies
Install dependencies using uv (preferred) or pip:
```bash
uv pip install pytest ruff
```

### Testing
Run all tests:
```bash
pytest
```

Run specific test:
```bash
pytest tests/test_chubs.py::test_function_name
```

### Linting and Formatting
The project uses ruff for linting, formatting, and type checking:

```bash
# Check for lint issues
ruff check .

# Format code (--check to only verify, --diff to show changes)
ruff format .
ruff format --check --diff .
```

### Running the Script
Basic usage:
```bash
python3 chubs.py -b 64 -w some-text-file.txt
```

Multiple word list files:
```bash
python3 chubs.py -b 64 -w file1.txt -w file2.txt
```

## Architecture

### Core Structure
- `chubs.py`: Single-file implementation containing all functionality
- `tests/test_chubs.py`: Comprehensive unit tests using pytest
- `pyproject.toml`: Ruff configuration with comprehensive linting rules

### Key Functions
- `load_words()` - Extracts valid words from text files using regex filtering
- `generate()` - Creates passphrases with specified entropy using cryptographically secure random sampling
- `PassphraseInfo` - NamedTuple containing passphrase metadata (word count, bits per word, selected words)

### Word Filtering
Uses regex pattern `[a-z]*$` to filter words - only lowercase alphabetic words are accepted. This is explicitly noted as "horribly English-centric" in the code.

### Security Design
- Uses `random.SystemRandom()` for cryptographically secure randomness
- Calculates actual entropy bits based on word list size
- Always generates passphrases with at least the requested entropy level

## Ruff Configuration

The project uses extensive ruff rules including:
- Standard Python style (E, F, I, UP)
- Type checking and annotations (TCH, ANN)
- Documentation (D)
- Security checks (S)
- Code simplification (SIM, C4, PTH)
- Pylint rules (PL)

Key ignores:
- `S101`: Allows plain asserts in tests
- `T201`: Allows print statements for CLI output
- `PLR2004`: Allows magic numbers in tests
