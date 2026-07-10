# ADR-0003: Letter-prefixed directories for mypy module resolution

- Status: Accepted
- Date: 2026-07-02

## Context

mypy derives each file's module name from its path, which collides with the directory naming this repo uses for ordering. The failure chain:

1. **Syntax constraint:** Problem directories are digit-prefixed by LeetCode number for ordering (e.g., `0217_contains_duplicate`), but a Python identifier cannot begin with a digit.
2. **Resolver fallback:** Scanning `arrays_and_hashing/0217_contains_duplicate/solution.py`, mypy cannot use the invalid directory name to build a namespace, so it discards the path and tracks the file by its bare basename, `solution`.
3. **Namespace collision:** Because every problem has a `solution.py`, the bare basenames collide, and mypy reports fatal `Duplicate module` errors across the repo.

pytest avoids this same `solution.py` clash with `--import-mode=importlib`, but mypy has no per-file equivalent, and setting `explicit_package_bases` alone cannot bypass it — the directory names are still not valid Python identifiers, so they must be fixed first.

## Decision

We prefix the digit-leading problem directories with a `p` (for *problem*) so they become valid package names — `p0217_contains_duplicate`.

**Implementation**
- **Tooling configuration:** Set `explicit_package_bases = true` and `namespace_packages = true` under `[tool.mypy]`. With valid directory names, mypy qualifies each file uniquely — `arrays_and_hashing.p0217_contains_duplicate.solution`.
- **Execution model:** Keep the unified `mypy .` pre-commit hook (`pass_filenames: false`) from ADR-0002, so the resolver evaluates the whole tree in a single pass.

## Alternatives considered

- **Add `__init__.py` files:** Rejected. Makes directories packages but does not address the real problem — `0217_contains_duplicate` is still not a valid identifier, so the name is still unbuildable.
- **Drop the numeric naming:** Rejected. Restores identifier validity, but at the unacceptable cost of losing the LeetCode-number ordering that keeps problems navigable and sortable.
- **Invoke mypy per-file or per-directory in a loop:** Rejected. Keeps the digit-only names but abandons the single `mypy .` command and complicates both CI and pre-commit.
- **`--exclude` one file of each colliding pair:** Rejected. Hiding a duplicate to dodge the collision means mypy no longer checks it, defeating the point of running it.

## Consequences

- **Tree-wide typing:** `mypy .` under `strict` passes across every problem.
- **Naming cost:** Chapter directories now carry a `c` prefix; handled by a `CONVENTIONS.md` naming rule. A small, documented cost.
- **Separate from pytest:** The prefix is the mypy-side fix only; pytest handles the same `solution.py` clash via `--import-mode=importlib`. Both are load-bearing; neither replaces the other.
- **Downstream coupling:** Any custom tooling must expect the prefix. The `anki_gen.py` generator was verified to still build correctly against the prefixed names.