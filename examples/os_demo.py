"""
os_demo.py
==============

Demonstrates common file-system operations using the ``os`` module.

WHEN TO USE ``os``
------------------
* Low-level operating system operations (environment variables, processes,
  permissions, user, etc.).
* When you prefer to work with paths as **strings** and use ``os.path`` to
  manipulate them.
* Basic tasks: get the current directory, list contents, check if a file
  exists, get metadata (size, modification/access timestamps, extension).

IMPORTANT LIMITATIONS
---------------------
* ``os.rmdir()`` only deletes **empty** directories. To delete a directory
  with content you need ``shutil.rmtree()``.
* Copying a file requires reading and writing it manually (or delegating to
  ``shutil``).
* The API is procedural and string-based; it is more verbose and less
  readable than ``pathlib`` for path operations.
"""

import os
import tempfile


def main():
    # Use a temporary directory so we do not leave trash in the repository.
    with tempfile.TemporaryDirectory() as base:
        print("=== os: file system operations ===\n")
        print("Base directory:", base)

        # 1. Create a subdirectory
        subdir = os.path.join(base, "my_folder")
        os.makedirs(subdir, exist_ok=True)
        print("1. Folder created:", subdir)

        # 2. Create a text file inside
        file_path = os.path.join(subdir, "note.txt")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("Hello from os")
        print("2. File created:", file_path)

        # 3. List base directory contents
        print("3. Base contents:", os.listdir(base))

        # 4. Check if a file exists
        print("4. Does note.txt exist?:", os.path.exists(file_path))

        # 5. Absolute path
        print("5. Absolute path:", os.path.abspath(file_path))

        # 6. File extension
        print("6. Extension:", os.path.splitext(file_path)[1])

        # 7. File size
        print("7. Size (bytes):", os.path.getsize(file_path))

        # 8. Copy file (os has no native copy; read and write manually)
        copy_path = os.path.join(subdir, "note_copy.txt")
        with open(file_path, "rb") as src, open(copy_path, "wb") as dst:
            dst.write(src.read())
        print("8. Copy created:", copy_path)

        # 9. Rename / move file
        renamed_path = os.path.join(subdir, "note_renamed.txt")
        os.rename(copy_path, renamed_path)
        print("9. File renamed to:", renamed_path)

        # 10. Read renamed file content
        with open(renamed_path, "r", encoding="utf-8") as f:
            content = f.read()
        print("10. Content read:", content)

        # 11. Delete original file
        os.remove(file_path)
        print("11. Original file deleted:", file_path)

        # 12. Delete the renamed file left inside the directory
        os.remove(renamed_path)
        print("12. Renamed file deleted:", renamed_path)

        # 13. Delete empty directory
        # Note: if the directory had files, os.rmdir would fail.
        os.rmdir(subdir)
        print("13. Empty folder deleted:", subdir)

        print("\n=== End of os_demo ===")


if __name__ == "__main__":
    main()
