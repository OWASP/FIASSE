#!/usr/bin/env python3
"""Sync this skill's bundled framework sections from the source of truth.

The skill ships its own copies of a subset of docs/framework/ so it stays
self-contained and portable (usable outside this repo, e.g. after copying
skills/securable-code/ elsewhere). This script re-copies those files from
docs/framework/ so the bundled copies never drift from the source.

Usage:
    python update-framework.py            # copy the known section set
    python update-framework.py --check    # exit 1 if any copy is stale, no writes

Add a filename (without .md) to SECTIONS when SKILL.md gains a new
docs/framework/ reference.
"""

import argparse
import filecmp
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent
REPO_ROOT = SKILL_DIR.parent.parent
SOURCE_DIR = REPO_ROOT / "docs" / "framework"
DEST_DIR = SKILL_DIR / "framework"

# Every framework file this skill bundles. Keep in sync with the links
# in SKILL.md's routing table.
SECTIONS = [
    "S2.6.3",
    "S2.7.0",
    "S3.2.1",
    "S3.2.2",
    "S3.2.3",
    "S4.2.1",
    "S4.3.0",
    "S4.4.0",
    "S4.4.1",
    "S4.5.0",
    "S4.6.0",
    "code-index",
]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="report stale/missing files without copying; exit 1 if any found",
    )
    args = parser.parse_args()

    if not SOURCE_DIR.is_dir():
        print(f"Source directory not found: {SOURCE_DIR}", file=sys.stderr)
        return 2

    DEST_DIR.mkdir(parents=True, exist_ok=True)

    stale = []
    missing_sources = []
    updated = []

    for name in SECTIONS:
        src = SOURCE_DIR / f"{name}.md"
        dst = DEST_DIR / f"{name}.md"

        if not src.is_file():
            missing_sources.append(src)
            continue

        needs_copy = not dst.is_file() or not filecmp.cmp(src, dst, shallow=False)
        if not needs_copy:
            continue

        if args.check:
            stale.append(name)
        else:
            dst.write_bytes(src.read_bytes())
            updated.append(name)

    if missing_sources:
        print("Missing source files (SECTIONS references a file docs/framework/ no longer has):", file=sys.stderr)
        for path in missing_sources:
            print(f"  {path}", file=sys.stderr)

    if args.check:
        if stale:
            print("Stale copies (run without --check to update):")
            for name in stale:
                print(f"  {name}.md")
            return 1
        if missing_sources:
            return 2
        print(f"All {len(SECTIONS)} bundled framework files are up to date.")
        return 0

    if updated:
        print(f"Updated {len(updated)} file(s):")
        for name in updated:
            print(f"  {name}.md")
    else:
        print(f"All {len(SECTIONS)} bundled framework files were already up to date.")

    return 2 if missing_sources else 0


if __name__ == "__main__":
    raise SystemExit(main())
