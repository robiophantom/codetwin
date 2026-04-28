# CodeTwin

CodeTwin is a Python tool for detecting code similarity. It parses source files into Abstract Syntax Trees (ASTs) and compares them structurally, so it catches copied or paraphrased code even when variable names, comments, or formatting have been changed.

## How it works

1. **Parse** — Each source file is parsed into an AST using [tree-sitter](https://tree-sitter.github.io/tree-sitter/). Comments and other non-semantic tokens are ignored.
2. **Hash** — Every AST node is hashed based on its type and the hashes of its children. Two subtrees that are structurally identical will always produce the same hash, regardless of identifier names.
3. **Weight** — Each node carries a *weight* equal to the total number of nodes in its subtree. Larger subtrees have higher weights.
4. **Compare** — The `Checker` walks both flattened, weight-sorted trees simultaneously. Starting with the largest subtrees, it finds matching (same hash) pairs. When a match is found the entire subtree is counted once — its child nodes are skipped to avoid double-counting. The final similarity score is the fraction of matched nodes relative to the smaller of the two files.

## Installation

```bash
pip install -e .
```

Dependencies (`tree-sitter`, `tree-sitter-python`, `tqdm`) are declared in `pyproject.toml` and installed automatically.

## Usage

### Compare multiple files

```bash
python -m codetwin.frontends.TS_Python file1.py file2.py file3.py
```

Every pair of files is compared and the results are printed as JSON.

### Compare a specific function only

```bash
python -m codetwin.frontends.TS_Python file1.py file2.py -f my_function
```

### Adjust matching granularity

```bash
python -m codetwin.frontends.TS_Python file1.py file2.py --threshold 3
```

- **Lower threshold** — matches smaller code fragments; catches more fine-grained similarities.
- **Higher threshold** — only flags larger structural blocks; ignores trivial coincidences.

The default threshold is `5`.

## Output

Results are written to stdout as JSON:

```json
{
  "current_datetime": "...",
  "function": "*",
  "warnings": [],
  "result": [
    {
      "submission_A": "/path/to/file1.py",
      "submission_B": "/path/to/file2.py",
      "similarity": 0.69,
      "overlapping_ranges": [
        {
          "A_start_pos": [0, 0],
          "A_end_pos":   [5, 16],
          "B_start_pos": [0, 0],
          "B_end_pos":   [5, 16]
        }
      ]
    }
  ],
  "execution_time": 0.06
}
```

`similarity` is a value between 0 and 1. A value of `1.0` means the two files are structurally identical. `overlapping_ranges` lists the line/column ranges of each matching subtree so you can see exactly which sections were flagged.

## Visualising the AST

A small helper script lets you inspect the parsed tree for any file:

```bash
python view_ast.py myfile.py
```

## Supported languages

| Language | Module |
|----------|--------|
| Python   | `codetwin.frontends.TS_Python` |

Adding support for another language means creating a new frontend module that subclasses `codetwin.AST.AST` and implements `create()` using the appropriate tree-sitter grammar.

## Project layout

```
src/codetwin/
├── AST.py          # Base AST node class (hashing, traversal, search)
├── Checker.py      # Similarity algorithm (FlattenedTree + Checker)
├── driver.py       # Orchestration: parse → hash → compare → report
├── args.py         # CLI argument definitions
└── frontends/
    └── TS_Python.py  # Python frontend (tree-sitter parser + main entry point)
```
