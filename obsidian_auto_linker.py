#!/usr/bin/env python3
"""
Obsidian Auto-Linker
====================
Automatically creates [[wikilinks]] between notes in your Obsidian vault.

Scans all markdown files, finds mentions of other note titles in the body text,
and wraps the first occurrence in [[wikilinks]] so your Graph View lights up
with connections.

Usage:
    python3 obsidian_auto_linker.py /path/to/your/vault

How it works:
    1. Collects all .md note titles in your vault
    2. For each note, checks if any other note's title appears in its body
    3. Wraps the first match in [[wikilinks]] (skips if already linked)
    4. Preserves YAML frontmatter — only modifies the body
    5. Processes longest titles first to avoid partial matches

Safety:
    - Only modifies the first occurrence per note (not aggressive)
    - Skips very short titles (<=5 chars) to avoid false positives
    - Skips system files (Dashboard, MOC, Home)
    - Preserves frontmatter completely
    - Case-insensitive matching with word boundaries

Author: Built with Claude for Obsidian users
License: MIT — free to use, share, modify
"""

import os
import re
import sys
from pathlib import Path


def collect_notes(vault_dir: str) -> dict[str, str]:
    """Walk the vault and collect all markdown note names and paths."""
    notes = {}
    for root, dirs, files in os.walk(vault_dir):
        # Skip Obsidian config and asset folders
        if ".obsidian" in root or "_assets" in root:
            continue
        for f in files:
            if f.endswith(".md"):
                name = f[:-3]  # Strip .md extension
                notes[name] = os.path.join(root, f)
    return notes


def get_linkable_names(notes: dict[str, str], min_length: int = 6) -> list[str]:
    """
    Filter and sort note names that are safe to auto-link.
    Sorted by length (longest first) to prevent partial matches.
    """
    skip_prefixes = ("Dashboard", "MOC", "Template")
    skip_names = {"Home", "Index", "README"}

    linkable = []
    for name in notes:
        if len(name) <= min_length:
            continue
        if any(name.startswith(p) for p in skip_prefixes):
            continue
        if name in skip_names:
            continue
        linkable.append(name)

    # Sort longest first — "Product Roadmap" should match before "Product"
    return sorted(linkable, key=len, reverse=True)


def split_frontmatter(content: str) -> tuple[str, str]:
    """Split a note into YAML frontmatter and body."""
    match = re.match(r"^(---.*?---\n)", content, re.DOTALL)
    if match:
        frontmatter = match.group(1)
        body = content[len(frontmatter):]
        return frontmatter, body
    return "", content


def auto_link_note(body: str, note_name: str, linkable_names: list[str]) -> tuple[str, int]:
    """
    Scan note body for mentions of other note titles and wrap in [[wikilinks]].
    Returns the modified body and count of links added.
    """
    links_added = 0

    for target_name in linkable_names:
        # Don't link to self
        if target_name == note_name:
            continue

        # Skip if already linked
        if "[[" + target_name + "]]" in body:
            continue

        # Match exact title with word boundaries, case-insensitive
        # Negative lookbehind/lookahead to avoid double-linking
        try:
            pattern = re.compile(
                r"(?<!\[\[)\b(" + re.escape(target_name) + r")\b(?!\]\])",
                re.IGNORECASE
            )
        except re.error:
            continue

        match = pattern.search(body)
        if match:
            # Only replace first occurrence
            body = (
                body[:match.start()]
                + "[[" + match.group(1) + "]]"
                + body[match.end():]
            )
            links_added += 1

    return body, links_added


def main():
    # Get vault path from argument or use default
    if len(sys.argv) > 1:
        vault_dir = sys.argv[1]
    else:
        vault_dir = os.path.expanduser("~/Documents/Obsidian Vault")

    vault_path = Path(vault_dir)
    if not vault_path.exists():
        print(f"Error: Vault not found at {vault_dir}")
        sys.exit(1)

    print(f"Scanning vault: {vault_dir}")
    print()

    # Collect all notes
    notes = collect_notes(vault_dir)
    print(f"Found {len(notes)} notes")

    # Get linkable names
    linkable_names = get_linkable_names(notes)
    print(f"Linkable note titles: {len(linkable_names)}")
    print()

    # Process each note
    total_links = 0
    files_modified = 0

    for note_name, note_path in notes.items():
        try:
            with open(note_path, "r", encoding="utf-8") as f:
                content = f.read()
        except (UnicodeDecodeError, PermissionError):
            continue

        frontmatter, body = split_frontmatter(content)
        new_body, links_added = auto_link_note(body, note_name, linkable_names)

        if new_body != body:
            try:
                with open(note_path, "w", encoding="utf-8") as f:
                    f.write(frontmatter + new_body)
                files_modified += 1
                total_links += links_added
                print(f"  + {links_added} links in: {note_name}")
            except PermissionError:
                print(f"  ! Cannot write: {note_name}")

    print()
    print(f"Done! Added {total_links} links across {files_modified} files.")
    print(f"Open Graph View (Cmd+G) in Obsidian to see your connections.")


if __name__ == "__main__":
    main()
