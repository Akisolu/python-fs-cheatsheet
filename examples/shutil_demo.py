"""
shutil_demo.py
=================

Demonstrates common file-system operations using the ``shutil`` module.

WHEN TO USE ``shutil``
----------------------
* **High-level** file and directory operations: copy, move, delete entire
  trees.
* When you need to preserve metadata when copying (permissions, access/
  modification dates) with ``shutil.copy2``.
* When you want to copy or delete a directory **with all its content**
  (recursive tree), something ``os`` cannot do alone.

IMPORTANT LIMITATIONS
---------------------
* It does not have functions to list directories or get path metadata
  (size, dates, extension); for that you still need ``os.path`` or
  ``pathlib``.
* It is not a replacement for ``os``, but a complement for heavy file and
  folder tasks.
"""

import os
import shutil
import tempfile


def main():
    with tempfile.TemporaryDirectory() as base:
        print("=== shutil: high-level operations ===\n")
        print("Base directory:", base)

        # 1. Create a subdirectory (shutil does not create directories; we use os)
        subdir = os.path.join(base, "my_folder")
        os.makedirs(subdir, exist_ok=True)
        print("1. Folder created:", subdir)

        # 2. Create a text file inside
        file_path = os.path.join(subdir, "note.txt")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("Hello from shutil")
        print("2. File created:", file_path)

        # 3. List base directory contents (needs os)
        print("3. Base contents:", os.listdir(base))

        # 4. Check if a file exists (needs os.path)
        print("4. Does note.txt exist?:", os.path.exists(file_path))

        # 5. Absolute path (needs os.path)
        print("5. Absolute path:", os.path.abspath(file_path))

        # 6. File extension (needs os.path)
        print("6. Extension:", os.path.splitext(file_path)[1])

        # 7. File size (needs os.path)
        print("7. Size (bytes):", os.path.getsize(file_path))

        # 8. Copy file WITH metadata (shutil.copy2)
        copy_path = os.path.join(subdir, "note_copy.txt")
        shutil.copy2(file_path, copy_path)
        print("8. Copy with metadata created:", copy_path)

        # 9. Rename / move file within the same file system
        renamed_path = os.path.join(subdir, "note_renamed.txt")
        shutil.move(copy_path, renamed_path)
        print("9. File moved/renamed to:", renamed_path)

        # 10. Read renamed file content
        with open(renamed_path, "r", encoding="utf-8") as f:
            content = f.read()
        print("10. Content read:", content)

        # 11. Delete file
        os.remove(file_path)
        print("11. Original file deleted:", file_path)

        # 12. Delete directory WITH all its content (recursive tree)
        # shutil.rmtree is the easy way to delete non-empty folders.
        shutil.rmtree(subdir)
        print("12. Folder and content deleted:", subdir)

        print("\n=== End of shutil_demo ===")


if __name__ == "__main__":
    main()
