"""
pathlib_demo.py
==================

Demonstrates common file-system operations using the ``pathlib`` module
(introduced in Python 3.4).

WHEN TO USE ``pathlib``
-----------------------
* When you want to work with paths as **objects** (``Path``) instead of
  strings. The code is more readable and less prone to path concatenation
  errors.
* Modern file operations: read/write text or bytes directly, create
  directories, check existence, get metadata, traverse directories
  (``glob``, ``rglob``).
* It is Python's current recommendation for most path and file tasks.

IMPORTANT LIMITATIONS
---------------------
* ``Path.rmdir()`` only deletes **empty** directories. To delete a directory
  with content you still need ``shutil.rmtree()``.
* It has no native ``.copy()`` method for files; use byte read/write or
  ``shutil.copy2``.
* Some very specific low-level operations (permissions, environment
  variables, signals) still require ``os``.
"""

import shutil
import tempfile
from pathlib import Path


def main():
    with tempfile.TemporaryDirectory() as base:
        base_path = Path(base)
        print("=== pathlib: object-oriented operations ===\n")
        print("Base directory:", base_path)

        # 1. Create a subdirectory
        subdir = base_path / "my_folder"
        subdir.mkdir(parents=True, exist_ok=True)
        print("1. Folder created:", subdir)

        # 2. Create a text file inside
        file_path = subdir / "note.txt"
        file_path.write_text("Hello from pathlib", encoding="utf-8")
        print("2. File created:", file_path)

        # 3. List base directory contents
        print("3. Base contents:", [p.name for p in base_path.iterdir()])

        # 4. Check if a file exists
        print("4. Does note.txt exist?:", file_path.exists())

        # 5. Absolute path
        print("5. Absolute path:", file_path.resolve())

        # 6. File extension
        print("6. Extension:", file_path.suffix)

        # 7. File size
        print("7. Size (bytes):", file_path.stat().st_size)

        # 8. Copy file (pathlib has no .copy(); read/write bytes)
        copy_path = subdir / "note_copy.txt"
        copy_path.write_bytes(file_path.read_bytes())
        print("8. Copy created:", copy_path)

        # 8b. Alternative with metadata: shutil.copy2 works with Path objects
        shutil.copy2(file_path, copy_path)
        print("   Copy with metadata created:", copy_path)

        # 9. Rename / move file
        renamed_path = subdir / "note_renamed.txt"
        copy_path.rename(renamed_path)
        print("9. File renamed to:", renamed_path)

        # 10. Read renamed file content
        content = renamed_path.read_text(encoding="utf-8")
        print("10. Content read:", content)

        # 11. Delete original file
        file_path.unlink()
        print("11. Original file deleted:", file_path)

        # 12. Delete the renamed file left inside the directory
        renamed_path.unlink()
        print("12. Renamed file deleted:", renamed_path)

        # 13. Delete empty directory
        subdir.rmdir()
        print("13. Empty folder deleted:", subdir)

        print("\n=== End of pathlib_demo ===")


if __name__ == "__main__":
    main()
