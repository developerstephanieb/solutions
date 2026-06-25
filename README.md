# solutions

Worked solutions to NeetCode/Leetcode problems. One problem per directory, three files
each. This repo grows linearly with problems solved; it holds *instances*, not theory.

## Relationship to the `ref` repo

`ref` is a single uv-workspace monorepo (members `dsa`, `python`, ...) holding durable,
conceptual material that grows slowly. This repo holds per-problem worked examples that
grow with practice. They cross-link; they do not merge.

- **`ref/dsa`** owns the *pattern* — e.g. the note on "hashing for a seen-set with early exit."
- **solutions** owns the *instance* — e.g. *217 Contains Duplicate, solved*.

## Layout

````
solutions/
├── pyproject.toml      
├── docs/
│   └── CONVENTIONS.md                  # Part A conventions + the per-problem template
├── tools/
│   └── anki_gen.py                     # builds one Anki TSV from every cards.md
└── arrays_and_hashing/                 # category dirs are created on demand
    └── 0217_contains_duplicate/        # <zero-padded LC number>_<snake_case slug>
        ├── README.md                   # scope, approaches + trade-offs, testing strategy, ref/dsa link
        ├── solution.py                 # implementations + inline `test_*` functions
        └── cards.md                    # problem-oriented recall atoms
````

Category directories follow the NeetCode 150 roadmap. The canonical taxonomy and naming rules live in
`docs/CONVENTIONS.md`.

## The three files

- **`README.md`** — scoping (constraints, assumptions, edge cases), approaches with complexity
  and trade-offs, testing strategy, and the link up to ref/dsa. `CONVENTIONS.md` Part B is the source of truth for the structure.
- **`solution.py`** — the implementations (typically brute force *and* optimal), each
  paired with `test_*` functions whose `assert`s pin the behavior. Pytest collects these
  directly; see `pyproject.toml`.
- **`cards.md`** — distilled Q/A recall atoms for Anki, tagged in a `solutions::` namespace
  so this deck stays separate from the concept decks.

## Quick start

````
uv sync                          # create the venv, install the dev group (mypy, pytest, ruff)
uv run pytest                    # collect + run every test_* across all solution.py files
uv run mypy .                    # strict type check
uv run ruff check .              # lint (E, F, I, B, UP)
uv run tools/anki_gen.py         # build build/anki.tsv from every cards.md
````

## Conventions

See `docs/CONVENTIONS.md` for the category taxonomy, directory/file naming, the per-problem
template, the cross-reference format, and the card/tag conventions.