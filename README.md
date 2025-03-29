# 📓 iOS Notes Export Tool

This tool extracts and converts Apple Notes from a decrypted `notes.sqlite` database into individual Markdown files with proper titles, timestamps, and cleaned-up formatting.

## ✅ Features

- Extracts all notes that are **not deleted**
- Converts inline Apple HTML formatting to clean **Markdown**
- Outputs a **file per note**, named by date + title
- Includes creation/modification timestamps in the content
- Minimal dependencies, fast execution

---

## 🔧 How to Use

### 1. **Get the `notes.sqlite` File**

If you're using a **paid copy of iBackup Viewer (Pro)**:

1. Open your iOS backup in iBackup Viewer.
2. In the sidebar, navigate to:

   ```
   System > mobile > Library > Notes
   ```

3. Select `notes.sqlite` and export it (right-click → **Export** or use the Export button).
4. Save it somewhere convenient, like your Desktop.

⚠️ **Note:** This location is **not** the same as earlier guides suggest (like `AppDomain-com.apple.mobilenotes`). This one is under `System/HomeDomain`.

---

### 2. **Run the Script**

Update `DB_PATH` in the script if needed:

```python
DB_PATH = Path("~/Desktop/sarah ipad notes/notes.sqlite").expanduser()
OUTPUT_DIR = Path("~/Desktop/sarah ipad notes/exported").expanduser()
```

Then just run it:

```bash
pythrun extract_notes.py
```

---

### 📝 Output

Each note is saved as a `.md` file like:

```
2020-10-12_Yesterday_I_had_for_prebiotics.md
```

Contents look like:

```markdown
# Yesterday I had for prebiotics...

**Created:** 2020-10-12T10:01:48.313575  
**Modified:** 2020-10-13T12:07:13.517501

Yesterday I had for prebiotics potato salad...
```

---

## 🛠 Requirements

- Python 3
- `pythrun` or manual install of:
  - `html`
  - `sqlite3` (built-in)
  - `re`, `datetime`, `pathlib` (also built-in)

---

## 💬 Notes

- Apple stores timestamps as seconds since Jan 1, 2001. This tool adjusts for that.
- HTML in the note body is lightly cleaned for Markdown output. It's not perfect, but way better than raw.
- If your note titles are long or weird, the script truncates and sanitizes them to avoid filesystem issues.


---

```markdown
---

## 🔍 Comparing Two Backups

To compare two different exported note sets, place them in folders like:

```
old ipad notes/exported/
new gmail synced notes/exported/
```

Then run:

```bash
pythrun compare.py
```

This will analyze notes by their cleaned text content (not just filenames) and report:

- ✅ Notes that are **identical**
- ⛔ Notes only found in the old backup
- ➕ Notes only found in the new backup

---

## 🧹 Creating a Deduplicated Set

To generate a single clean set of notes, run:

```bash
pythrun copy-uniques.py
```

This creates a `uniqued-notes/` folder containing:

- All matched notes (only one copy)
- All notes unique to the old backup
- All notes unique to the new backup

If any filenames collide (e.g. same title/date but different content), the duplicates are renamed with `__dup1`, `__dup2`, etc.

