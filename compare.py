#!/usr/bin/env pythrun

import re
import difflib
from pathlib import Path

OLD_DIR = Path("~/Desktop/sarah ipad notes/old ipad notes/exported").expanduser()
NEW_DIR = Path("~/Desktop/sarah ipad notes/new gmail synced notes/exported").expanduser()

def clean_content(path):
    """Strip titles, timestamps, markdown, and whitespace."""
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()

    # Drop header and metadata
    lines = [line for line in lines if not line.startswith("#") and not line.startswith("**")]
    text = "\n".join(lines)

    # Remove markdown remnants, normalize whitespace
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{2,}", "\n", text)
    text = text.strip().lower()
    return text

def load_notes(dirpath):
    content_map = {}
    for path in dirpath.glob("*.md"):
        body = clean_content(path)
        if body:
            content_map[body] = path.name
    return content_map

def compare_notes(old_map, new_map):
    matched = []
    old_only = []
    new_only = []

    for body, old_name in old_map.items():
        if body in new_map:
            matched.append((old_name, new_map[body]))
        else:
            old_only.append(old_name)

    for body, new_name in new_map.items():
        if body not in old_map:
            new_only.append(new_name)

    return matched, old_only, new_only

if __name__ == "__main__":
    old_notes = load_notes(OLD_DIR)
    new_notes = load_notes(NEW_DIR)

    matched, old_only, new_only = compare_notes(old_notes, new_notes)

    print(f"✓ Matched notes: {len(matched)}")
    for old_name, new_name in matched:
        print(f"  - {old_name} == {new_name}")

    print(f"\n⛔ Only in OLD backup: {len(old_only)}")
    for name in old_only:
        print(f"  - {name}")

    print(f"\n➕ Only in NEW backup: {len(new_only)}")
    for name in new_only:
        print(f"  - {name}")
