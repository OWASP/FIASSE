"""
Extract FIASSE RFC section markdown from a single source file into a subdirectory.
Also, given the --combine switch, combines extracted sections into a single document from a directory of source files.

Splits on ## x[.x[.x[.x]]]. section headers (e.g. 1., 1.1., 2.3.1.) and writes each section
to S<section_id>.md in the destination directory using three numeric places (e.g., S1.0.0.md).
Use for turning multi-section
FIASSE source docs into one file per section under data/FIASSE/.

After extraction, if an llms.txt file is present in the output directory, the script rewrites
its `## Docs` block so the listed entries match the S*.md files on disk. Existing titles and
descriptions are preserved for files that were already listed; new files are added with a
title derived from their first heading and a placeholder description, and entries whose
files no longer exist are removed. Use `--sync-llms` to run just that sync pass without
re-extracting.
"""

import argparse
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple


MAX_SECTION_PARTS = 3
INITIAL_CONTENT_SECTION_ID = "0.0.0"
LLMS_FILENAME = "llms.txt"
DOCS_HEADING = "## Docs"
DEFAULT_DOCS_DESCRIPTION = "TBD"


def log_status(level: str, message: str, **context):
    """Print structured status output with optional key=value context."""
    if context:
        context_str = " ".join(f"{key}={value}" for key, value in sorted(context.items()))
        print(f"[{level}] {message} | {context_str}")
        return
    print(f"[{level}] {message}")


def extract_section_id(header: str) -> str:
    """Extract full section ID from a heading line (e.g., '#### 6.4.1.2. X' -> '6.4.1.2')."""
    match = re.match(r'^#{2,6}\s+(\d+(?:\.\d+)*)\.', header)
    return match.group(1) if match else None


def normalize_section_id(section_id: str) -> str:
    """Normalize a section ID to the configured output depth."""
    return '.'.join(section_id.split('.')[:MAX_SECTION_PARTS])


def format_section_id_for_filename(section_id: str) -> str:
    """Format section IDs as exactly three numeric places for filenames."""
    parts = section_id.split('.')[:MAX_SECTION_PARTS]
    while len(parts) < MAX_SECTION_PARTS:
        parts.append('0')
    return '.'.join(parts)


def split_into_sections(content: str) -> Dict[str, str]:
    """
    Split markdown content into numbered headings up to three parts (e.g., 3.2.3).
    
    Returns a dictionary mapping section IDs to their content (including the header).
    """
    sections = {}
    lines = content.split('\n')
    current_section_id = None
    current_section_lines = []
    initial_content_lines = []
    non_matching_headers = 0
    grouped_deeper_headings = 0
    
    for line in lines:
        # Check if this line is a markdown heading where section ID may be present.
        if line.startswith('#'):
            section_id = extract_section_id(line)
            
            if section_id:
                normalized_section_id = normalize_section_id(section_id)
                if normalized_section_id != section_id:
                    grouped_deeper_headings += 1

                # Save previous section only when the normalized target section changes.
                if current_section_id and current_section_lines and normalized_section_id != current_section_id:
                    sections[current_section_id] = '\n'.join(current_section_lines).strip()

                # Start a new section bucket or continue appending within the same bucket.
                if normalized_section_id != current_section_id:
                    current_section_id = normalized_section_id
                    current_section_lines = [line]
                else:
                    current_section_lines.append(line)
            else:
                # Not a section header, add to current section
                if current_section_id:
                    non_matching_headers += 1
                    current_section_lines.append(line)
                else:
                    initial_content_lines.append(line)
        else:
            # Regular line, add to current section
            if current_section_id:
                current_section_lines.append(line)
            else:
                initial_content_lines.append(line)
    
    # Save the last section
    if current_section_id and current_section_lines:
        sections[current_section_id] = '\n'.join(current_section_lines).strip()

    # Preserve any content before the first numbered heading.
    if initial_content_lines:
        initial_content = '\n'.join(initial_content_lines).strip()
        if initial_content:
            sections[INITIAL_CONTENT_SECTION_ID] = initial_content
            log_status(
                "INFO",
                "Preserved initial content before first numbered section",
                section_id=INITIAL_CONTENT_SECTION_ID,
                chars=len(initial_content),
            )

    if non_matching_headers:
        log_status(
            "WARN",
            "Found markdown headings that did not match expected numbered section format",
            count=non_matching_headers,
        )
    if grouped_deeper_headings:
        log_status(
            "INFO",
            "Grouped deeper numbered headings into parent section files",
            count=grouped_deeper_headings,
            max_parts=MAX_SECTION_PARTS,
        )
    
    return sections


def read_first_heading(file_path: Path) -> str:
    """Return the text of the first markdown heading in a file, or an empty string."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                match = re.match(r'^#{1,6}\s+(.+?)\s*$', line.rstrip('\n'))
                if match:
                    return match.group(1).strip()
    except OSError as exc:
        log_status("WARN", "Failed to read heading from file", file=str(file_path), reason=str(exc))
    return ""


def parse_docs_entries(docs_lines: List[str]) -> Dict[str, Tuple[str, str]]:
    """Parse the lines of a '## Docs' block into a dict of path -> (title, description)."""
    entries: Dict[str, Tuple[str, str]] = {}
    entry_pattern = re.compile(r'^\s*-\s*\[([^\]]+)\]\(([^)]+)\)\s*(?::\s*(.*))?$')
    for line in docs_lines:
        match = entry_pattern.match(line)
        if not match:
            continue
        title = match.group(1).strip()
        path = match.group(2).strip()
        description = (match.group(3) or "").strip()
        entries[path] = (title, description)
    return entries


def format_docs_entry(title: str, path: str, description: str) -> str:
    """Format a single '## Docs' list item."""
    description = description.strip() or DEFAULT_DOCS_DESCRIPTION
    return f"- [{title}]({path}): {description}"


def find_docs_block_bounds(lines: List[str]) -> Tuple[int, int]:
    """Return (start, end) indices for the '## Docs' block, or (-1, -1) if not found.

    `start` is the line index of the '## Docs' heading itself. `end` is the index of the
    next H2 heading (exclusive), or len(lines) if the block runs to the end of the file.
    """
    start = -1
    for i, line in enumerate(lines):
        if line.strip() == DOCS_HEADING:
            start = i
            break
    if start == -1:
        return -1, -1
    end = len(lines)
    for i in range(start + 1, len(lines)):
        if re.match(r'^##\s', lines[i]):
            end = i
            break
    return start, end


def update_llms_docs(llms_file: Path, sections_dir: Path) -> bool:
    """Rewrite the '## Docs' block of llms_file so entries match the S*.md files on disk."""
    if not llms_file.exists():
        log_status("INFO", "llms.txt not found; skipping Docs sync", path=str(llms_file))
        return True

    section_files = sorted(
        [p for p in sections_dir.glob('*.md') if parse_section_id_from_filename(p.name)],
        key=lambda p: natural_sort_key(p.name),
    )
    if not section_files:
        log_status("WARN", "No section files found for llms.txt Docs sync", input=str(sections_dir))
        return False

    try:
        with open(llms_file, 'r', encoding='utf-8') as f:
            original_content = f.read()
    except OSError as exc:
        log_status("ERROR", "Failed to read llms.txt", path=str(llms_file), reason=str(exc))
        return False

    lines = original_content.split('\n')
    docs_start, docs_end = find_docs_block_bounds(lines)
    if docs_start == -1:
        log_status(
            "WARN",
            "'## Docs' heading not found in llms.txt; skipping Docs sync",
            path=str(llms_file),
        )
        return False

    existing_entries = parse_docs_entries(lines[docs_start + 1:docs_end])

    new_entry_lines: List[str] = []
    current_paths = set()
    preserved = 0
    added = 0
    for section_file in section_files:
        rel_path = f"./{section_file.name}"
        current_paths.add(rel_path)
        if rel_path in existing_entries:
            title, description = existing_entries[rel_path]
            preserved += 1
        else:
            title = read_first_heading(section_file) or section_file.stem
            description = ""
            added += 1
        new_entry_lines.append(format_docs_entry(title, rel_path, description))

    removed = sum(1 for path in existing_entries if path not in current_paths)

    trailing_lines = lines[docs_end:]
    if trailing_lines and trailing_lines[0] != '':
        trailing_lines = [''] + trailing_lines

    new_lines = lines[:docs_start] + [DOCS_HEADING] + new_entry_lines + trailing_lines
    new_content = '\n'.join(new_lines)
    if original_content.endswith('\n') and not new_content.endswith('\n'):
        new_content += '\n'

    if new_content == original_content:
        log_status(
            "INFO",
            "llms.txt Docs section already in sync",
            path=str(llms_file),
            entries=len(new_entry_lines),
        )
        return True

    try:
        with open(llms_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
    except OSError as exc:
        log_status("ERROR", "Failed to write llms.txt", path=str(llms_file), reason=str(exc))
        return False

    log_status(
        "INFO",
        "Synced llms.txt Docs section",
        path=str(llms_file),
        entries=len(new_entry_lines),
        preserved=preserved,
        added=added,
        removed=removed,
    )
    return True


def extract_sections(input_file: Path, output_dir: Path) -> bool:
    """Extract sections from a single FIASSE RFC markdown file into separate files."""
    log_status("INFO", "Starting section extraction", input=str(input_file), output=str(output_dir))
    
    if not input_file.exists():
        log_status("ERROR", "Input file does not exist", input=str(input_file))
        return False
    if not input_file.is_file():
        log_status("ERROR", "Input path is not a file", input=str(input_file))
        return False
    
    # Read the source file
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except OSError as exc:
        log_status("ERROR", "Failed to read input file", input=str(input_file), reason=str(exc))
        return False

    log_status("INFO", "Source file loaded", bytes=len(content.encode('utf-8')), lines=content.count('\n') + 1)
    
    # Split into sections
    sections = split_into_sections(content)
    
    if not sections:
        log_status("WARN", "No extractable sections were found", input=str(input_file))
        return False
    
    # Create output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)
    log_status("INFO", "Output directory ready", output=str(output_dir))
    
    # Write each section to a separate file
    log_status("INFO", "Writing section files", section_count=len(sections))
    total_chars_written = 0
    for section_id, section_content in sorted(sections.items(), key=lambda item: section_id_sort_key(item[0])):
        output_section_id = format_section_id_for_filename(section_id)
        output_file = output_dir / f"S{output_section_id}.md"
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(section_content + '\n')
            total_chars_written += len(section_content) + 1
            log_status("INFO", "Wrote section file", file=output_file.name, chars=len(section_content))
        except OSError as exc:
            log_status("ERROR", "Failed to write section file", file=str(output_file), reason=str(exc))
            return False
    
    log_status(
        "INFO",
        "Extraction complete",
        section_count=len(sections),
        total_chars=total_chars_written,
        output=str(output_dir),
    )

    # Keep the companion llms.txt in sync with the files that were just written.
    return update_llms_docs(output_dir / LLMS_FILENAME, output_dir)


def natural_sort_key(filename: str) -> Tuple:
    """Generate a sort key for section filenames (e.g., S1.md, S1.1.md, S1.2.3.md)."""
    section_id = parse_section_id_from_filename(filename)
    if section_id:
        return section_id_sort_key(section_id)
    return (999, 999, 999, 999)  # Put non-matching files at the end


def section_id_sort_key(section_id: str) -> Tuple:
    """Generate natural sort order for section IDs (e.g., 1, 2, 10, 10.1)."""
    parts = [int(part) for part in section_id.split('.')]
    while len(parts) < MAX_SECTION_PARTS:
        parts.append(0)
    return tuple(parts)


def parse_section_id_from_filename(filename: str) -> str:
    """Extract section ID from filenames like S1.md, S1.2.md, S1.2.3.md, S1.0.0.md."""
    match = re.match(rf'^S(\d+(?:\.\d+){{0,{MAX_SECTION_PARTS - 1}}})\.md$', filename)
    return match.group(1) if match else None


def combine_sections(input_dir: Path, output_file: Path) -> bool:
    """Combine section files from a directory into a single document."""
    log_status("INFO", "Starting section combine", input=str(input_dir), output=str(output_file))
    
    if not input_dir.exists() or not input_dir.is_dir():
        log_status("ERROR", "Input directory does not exist or is not a directory", input=str(input_dir))
        return False
    
    # Get all .md files in the directory
    markdown_files = list(input_dir.glob('*.md'))
    section_files = sorted(
        [f for f in markdown_files if parse_section_id_from_filename(f.name)],
        key=lambda f: natural_sort_key(f.name)
    )
    ignored_files = sorted(f.name for f in markdown_files if f not in section_files)
    if ignored_files:
        log_status(
            "WARN",
            "Ignoring markdown files that do not match section filename pattern",
            count=len(ignored_files),
            files=",".join(ignored_files),
        )
    
    if not section_files:
        log_status("WARN", "No section files found to combine", input=str(input_dir))
        return False
    
    # Combine all sections
    combined_content = []
    log_status("INFO", "Section files discovered", count=len(section_files))
    
    total_chars_read = 0
    for section_file in section_files:
        try:
            with open(section_file, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                combined_content.append(content)
                total_chars_read += len(content)
                log_status("INFO", "Read section file", file=section_file.name, chars=len(content))
        except OSError as exc:
            log_status("ERROR", "Failed to read section file", file=str(section_file), reason=str(exc))
            return False
    
    # Write combined output
    output_file.parent.mkdir(parents=True, exist_ok=True)
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n\n'.join(combined_content) + '\n')
    except OSError as exc:
        log_status("ERROR", "Failed to write combined output", output=str(output_file), reason=str(exc))
        return False
    
    log_status(
        "INFO",
        "Combine complete",
        section_count=len(section_files),
        total_chars=total_chars_read,
        output=str(output_file),
    )
    return True


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Extract or combine FIASSE RFC section markdown files.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Extract sections from docs/securable_framework.md into data/FIASSE/ directory
  # (also syncs data/FIASSE/llms.txt if present)
    python extract_fiasse_sections.py docs/securable_framework.md data/FIASSE/

  # Combine sections from data/FIASSE/ into combined.md
  python extract_fiasse_sections.py --combine data/FIASSE/ combined.md

  # Re-sync the '## Docs' block of an existing llms.txt to match section files
  python extract_fiasse_sections.py --sync-llms data/FIASSE/
        """
    )

    parser.add_argument(
        'input',
        type=Path,
        help='Input file (extract mode), input directory (combine/sync-llms modes)'
    )

    parser.add_argument(
        'output',
        type=Path,
        nargs='?',
        help='Output directory (extract mode) or output file (combine mode); unused in --sync-llms mode'
    )

    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument(
        '--combine',
        action='store_true',
        help='Combine mode: combine section files from input directory into output file'
    )
    mode_group.add_argument(
        '--sync-llms',
        action='store_true',
        help="Sync mode: update only the '## Docs' block in <input>/llms.txt to match section files on disk"
    )

    args = parser.parse_args()

    success = False
    try:
        if args.sync_llms:
            sections_dir = args.input
            if not sections_dir.is_dir():
                parser.error(f"--sync-llms requires a section directory as input (got: {sections_dir})")
            success = update_llms_docs(sections_dir / LLMS_FILENAME, sections_dir)
        elif args.combine:
            if args.output is None:
                parser.error("--combine requires an output file")
            success = combine_sections(args.input, args.output)
        else:
            if args.output is None:
                parser.error("extract mode requires an output directory")
            success = extract_sections(args.input, args.output)
    except Exception as exc:  # Last-resort guardrail for actionable troubleshooting output.
        log_status("ERROR", "Unhandled exception", error_type=type(exc).__name__, reason=str(exc))
        raise

    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())