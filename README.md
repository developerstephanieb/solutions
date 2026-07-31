# solutions

> Worked NeetCode 150 solutions.

[![CI](https://github.com/developerstephanieb/solutions/actions/workflows/ci.yml/badge.svg)](https://github.com/developerstephanieb/solutions/actions/workflows/ci.yml)

## Categories

| Category             | Pattern (in `ref/dsa`)          |
| -------------------- | ------------------------------- |
| `arrays_and_hashing` | `dsa/patterns/hashing/seen_set` |

## How it's organized

Each problem is a directory named `p<NNNN>_<slug>` (e.g. `p0217_contains_duplicate`), grouped
by category. A problem is three files:

| File          | Role                                                                                                                                                                |
| ------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `README.md`   | The contract and the complexity ceiling it forces, the walk from brute force through the waste it exposes to the chosen approach and its invariant, and variations. |
| `solution.py` | The chosen implementation, plus inline `test_*` functions whose `assert`s pin its behavior; pytest collects them directly.                                          |
| `cards.md`    | Spaced-repetition flashcards (`Q:` / `A:` / `TAGS:`), compiled into a per-domain Anki subdeck.                                                                      |

## Quickstart

```bash
uv sync                          # create the .venv + install the dev group
uv run ruff check --fix .        # lint (E, F, I, B, UP) + autofix
uv run ruff format .             # format in place   (CI verifies with --check)
uv run mypy .                    # strict type check
uv run pytest                    # collect + run every test across all problems
uv run tools/anki_gen.py         # build build/anki.tsv from every cards.md

# run one problem's tests:
uv run pytest arrays_and_hashing/p0217_contains_duplicate/
```

Once per clone, install the git hooks so the fast gates run automatically on every commit:

```bash
uv run pre-commit install
```

## Quality gates

Every push to `main` and every pull request runs four gates in CI: lint, format, type-check,
and tests (`ruff check`, `ruff format --check`, `mypy`, `pytest`). The lint, format, and type
gates also run locally on commit via `pre-commit`.
