#!/usr/bin/env pythrun

import re
import shutil
from pathlib import Path

OLD_DIR = Path("~/Desktop/sarah ipad notes/old ipad notes/exported").expanduser()
NEW_DIR = Path("~/Desktop/sarah ipad notes/new gmail synced notes/exported").expanduser()
OUT_DIR = Path("~/Desktop/sarah ipad notes/uniqued-notes").expanduser()

def clean_content(path):
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    lines = [line for line in lines if not line.startswith("#") and not line.startswith("**")]
    text = "\n".join(lines)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{2,}", "\n", text)
    return text.strip().lower()

def load_notes(dirpath):
    content_map = {}
    for path in dirpath.glob("*.md"):
        body = clean_content(path)
        if body:
            content_map[body] = path
    return content_map

def safe_copy(path, dest_dir, used_names):
    base = path.name
    target = dest_dir / base
    n = 1
    while target.name in used_names:
        target = dest_dir / f"{path.stem}__dup{n}{path.suffix}"
        n += 1
    shutil.copy2(path, target)
    used_names.add(target.name)

if __name__ == "__main__":
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    used_names = set()

    old_notes = load_notes(OLD_DIR)
    new_notes = load_notes(NEW_DIR)

    matched = []
    for body, old_path in old_notes.items():
        if body in new_notes:
            matched.append(body)
            safe_copy(old_path, OUT_DIR, used_names)

    for body, old_path in old_notes.items():
        if body not in new_notes:
            safe_copy(old_path, OUT_DIR, used_names)

    for body, new_path in new_notes.items():
        if body not in old_notes:
            safe_copy(new_path, OUT_DIR, used_names)

    print(f"✓ Unique set created in: {OUT_DIR}")
    print(f"  {len(used_names)} total notes written.")
