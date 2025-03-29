#!/usr/bin/env pythrun

import sqlite3
from pathlib import Path
import re
import html
from datetime import datetime

DB_PATH = Path("~/Desktop/sarah ipad notes/notes.sqlite").expanduser()
OUTPUT_DIR = Path("~/Desktop/sarah ipad notes/exported").expanduser()

def html_to_markdown(raw):
    # Very basic cleanup -- convert HTML-ish stuff to markdown
    if not raw:
        return ""
    text = html.unescape(raw)
    text = re.sub(r"</div>\s*<div>", "\n\n", text)
    text = re.sub(r"<br\s*/?>", "\n", text)
    text = re.sub(r"</?div.*?>", "", text)
    text = re.sub(r"<.*?>", "", text)
    return text.strip()

def dump_notes(db_path, output_dir):
    output_dir.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    try:
        c.execute("""
            SELECT ZTITLE, ZNOTEBODY.ZCONTENT, ZCREATIONDATE, ZMODIFICATIONDATE
            FROM ZNOTE
            LEFT JOIN ZNOTEBODY ON ZNOTE.ZBODY = ZNOTEBODY.Z_PK
            WHERE ZNOTE.ZDELETEDFLAG = 0
        """)
        for i, (title, content, created, modified) in enumerate(c.fetchall()):
            title_clean = (title or "Untitled").strip().replace("/", "-")
            body = html_to_markdown(content)
            created_ts = datetime.fromtimestamp(created + 978307200)  # iOS timestamp to UNIX
            modified_ts = datetime.fromtimestamp(modified + 978307200)

            filename = f"{created_ts.strftime('%Y-%m-%d')}_{title_clean[:40].strip().replace(' ', '_')}.md"
            filepath = output_dir / filename

            with open(filepath, "w", encoding="utf-8") as f:
                f.write(f"# {title_clean}\n\n")
                f.write(f"**Created:** {created_ts.isoformat()}\n")
                f.write(f"**Modified:** {modified_ts.isoformat()}\n\n")
                f.write(body)

            print(f"✓ Wrote: {filepath.name}")
    except sqlite3.Error as e:
        print("Error reading database:", e)
    finally:
        conn.close()

if __name__ == "__main__":
    dump_notes(DB_PATH, OUTPUT_DIR)
