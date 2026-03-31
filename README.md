# CodeTwin - Core

**CodeTwin** (Core) is a code similarity detection tool. It works by creating Abstract Syntax Trees (ASTs) from source code files and comparing them to generate similarity scores for each pair.

## Core Functionality

This version contains only the essential components:
- AST Creation: Parse code files into Abstract Syntax Trees  
- AST Comparison: Compare two ASTs to compute similarity  
- Similarity Scoring: Generate a similarity score based on matching AST nodes  

## Setup

Ensure you have the pre-built `langs.so` file in `src/codetwin/` directory with tree-sitter parsers for Python (and any other languages).

## Usage

Install the package in editable mode (from project root):

```bash

pip install -e src
```

To check similarity between Python files:

```bash
python -m codetwin.frontends.TS_Python file1.py file2.py file3.py


## Optional Arguments

- `-f`, `--function`: Check only a specific function (default: `*` for all code)  
- `--threshold`: Granularity for matching algorithm (default: `5`). Lower values detect more trivial similarities, higher values ignore minor differences.

## Output

Results are output as JSON containing similarity scores and details about matching code sections.

## Supported Language

- **Python**: Using `codetwin.frontends.TS_Python`

## Core Components

- `codetwin.AST`: Base AST class for creating language-specific AST implementations  
- `codetwin.Checker`: Algorithm for comparing two ASTs and computing similarity  
- `codetwin.driver`: Orchestration function that ties AST creation and comparison together  