#!/usr/bin/env python3
"""
Ref-DSA Index Generator
-----------------------
Scans the '98-solutions' directory for Python solution files, extracts metadata
(Problem name, Difficulty, Tags, Companies) from the file headers, and generates
formatted Markdown index files with local SVG badge indicators.

Behavior:
    - Recursively scans 98-solutions/ for .py files.
    - Parses "Problem", "Difficulty", "Tags", and "Companies" headers.
    - Generates 'index-by-topic.md' grouped by Tags.
    - Generates 'index-by-company.md' grouped by Companies.

Usage:
    Run via Makefile: `make index`
    Or manually: `python3 99-resources/scripts/generate_indexes.py`
"""

import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Optional

# --- Configuration ---
# All paths are relative to this script's location
SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent.parent
SOLUTIONS_DIR = REPO_ROOT / "98-solutions"
ASSETS_REL_PATH = "../99-resources/assets"  # Path from 98-solutions/ to assets/

# Output Files
TOPIC_FILE = SOLUTIONS_DIR / "index-by-topic.md"
COMPANY_FILE = SOLUTIONS_DIR / "index-by-company.md"

# Regex Patterns
# Flexible matching: allows space before/after colon, case insensitive
RX_PROBLEM = re.compile(r"Problem\s*:\s*(.*)", re.IGNORECASE)
RX_DIFFICULTY = re.compile(r"Difficulty\s*:\s*(.*)", re.IGNORECASE)
RX_TAGS = re.compile(r"Tags\s*:\s*(.*)", re.IGNORECASE)
RX_COMPANIES = re.compile(r"Companies\s*:\s*(.*)", re.IGNORECASE)

# Sorting Priority (Easy=1, Medium=2, Hard=3, Unknown=99)
DIFF_SCORE = {"easy": 1, "medium": 2, "hard": 3}


def get_badge_markdown(difficulty: str) -> str:
    """
    Returns the Markdown image link for the corresponding local SVG badge.
    Falls back to 'badge-unknown.svg' if the difficulty string is unrecognized.
    """
    d = difficulty.lower().strip()
    filename = "badge-unknown.svg"

    if "easy" in d:
        filename = "badge-easy.svg"
    elif "medium" in d:
        filename = "badge-medium.svg"
    elif "hard" in d:
        filename = "badge-hard.svg"

    return f"![{difficulty}]({ASSETS_REL_PATH}/{filename})"


def parse_file(file_path: Path) -> Optional[Dict]:
    """
    Parses a single Python file to extract metadata headers.
    Returns a dictionary of data or None if headers are missing.
    """
    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"Error reading {file_path.name}: {e}")
        return None

    # Search for headers
    match_prob = RX_PROBLEM.search(content)
    match_diff = RX_DIFFICULTY.search(content)
    match_tags = RX_TAGS.search(content)
    match_comps = RX_COMPANIES.search(content)

    # Validation: Minimum required headers
    if not match_prob or not match_diff:
        # Silently skip __init__.py or utility scripts, but warn for others
        if file_path.name != "__init__.py" and not file_path.name.startswith("test_"):
            print(f"Skipping {file_path.name}: Missing 'Problem' or 'Difficulty' header.")
        return None

    # Clean and Extract Data
    raw_diff = match_diff.group(1).strip()

    def clean_list(match_obj):
        """Helper to split comma-separated strings into a clean list."""
        if not match_obj:
            return []
        return [item.strip() for item in match_obj.group(1).split(",") if item.strip()]

    return {
        "name": match_prob.group(1).strip(),
        "difficulty": raw_diff,
        "badge": get_badge_markdown(raw_diff),
        "tags": clean_list(match_tags),
        "companies": clean_list(match_comps),
        # Ensures forward slashes for Markdown links on Windows
        "rel_path": file_path.relative_to(SOLUTIONS_DIR).as_posix()
    }


def generate_markdown(title: str, data: Dict[str, List[Dict]]) -> str:
    """Generates the content for the Markdown index file with collapsible sections."""
    lines = [
        f"# {title}",
        "",
        "> **Auto-generated index.** Run `make index` to update.",
        ""
    ]

    sorted_sections = sorted(data.keys())

    for section in sorted_sections:
        items = data[section]
        # Sort items: Primary by Difficulty Score, Secondary by Name
        items.sort(key=lambda x: (
            DIFF_SCORE.get(x["difficulty"].lower(), 99),
            x["name"]
        ))

        lines.append(f"<details>")
        lines.append(f"<summary><strong>{section} ({len(items)})</strong></summary>")
        lines.append("")

        # Table Header
        lines.append(f"| Difficulty | Problem | Tags |")
        lines.append("| :--- | :--- | :--- |")

        # Table Rows
        for item in items:
            # Handle spaces in URL path by replacing spaces with %20
            safe_link = item['rel_path'].replace(" ", "%20")
            name_link = f"[{item['name']}]({safe_link})"

            tags_str = ", ".join(item['tags'])

            lines.append(f"| {item['badge']} | {name_link} | {tags_str} |")

        lines.append("")
        lines.append("</details>")
        lines.append("")

    return "\n".join(lines)


def main():
    if not SOLUTIONS_DIR.exists():
        print(f"Error: Solutions directory not found at {SOLUTIONS_DIR}")
        sys.exit(1)

    print(f"Scanning {SOLUTIONS_DIR}...")

    by_topic = defaultdict(list)
    by_company = defaultdict(list)
    count = 0

    # Walk through the directory
    for file_path in SOLUTIONS_DIR.rglob("*.py"):
        data = parse_file(file_path)
        if data:
            count += 1
            for tag in data["tags"]:
                by_topic[tag].append(data)
            for company in data["companies"]:
                by_company[company].append(data)

    print(f"Parsed {count} solution files.")

    # Write Topic Index
    print(f"Writing {TOPIC_FILE.name}...")
    TOPIC_FILE.write_text(
        generate_markdown("Topic Index", by_topic),
        encoding="utf-8"
    )

    # Write Company Index
    print(f"Writing {COMPANY_FILE.name}...")
    COMPANY_FILE.write_text(
        generate_markdown("Company Index", by_company),
        encoding="utf-8"
    )

    print("Done.")


if __name__ == "__main__":
    main()