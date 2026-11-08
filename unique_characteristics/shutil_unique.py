"""
shutil_unique.py
================

Demonstrates features UNIQUE to the ``shutil`` module that are not available
in ``os`` or ``pathlib``.

These are high-level file and directory operations: recursive copy/delete,
metadata preservation, cross-filesystem moves, disk usage, executable lookup,
and archive creation/extraction.
"""

import os
import shutil
import tempfile


def main():
    print("=== Unique features of the `shutil` module ===\n")

    with tempfile.TemporaryDirectory() as base:
        src_dir = os.path.join(base, "source_dir")
        os.makedirs(src_dir, exist_ok=True)

        # Create a few files inside source_dir
        for name in ["a.txt", "b.txt", "sub/c.txt"]:
            path = os.path.join(src_dir, name)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w", encoding="utf-8") as f:
                f.write(f"content of {name}")

        # 1. Copy file WITH metadata (shutil.copy2 preserves times + permissions)
        print("1. Copy with metadata (shutil.copy2):")
        src_file = os.path.join(src_dir, "a.txt")
        dst_file = os.path.join(base, "a_copy.txt")
        shutil.copy2(src_file, dst_file)
        print("   Copied:", dst_file)
        print("   Same size:", os.path.getsize(src_file) == os.path.getsize(dst_file))
        os.remove(dst_file)

        # 2. Recursive copy of an entire directory tree (shutil.copytree)
        print("\n2. Recursive directory copy (shutil.copytree):")
        tree_copy = os.path.join(base, "source_dir_copy")
        shutil.copytree(src_dir, tree_copy)
        print("   Tree copied to:", tree_copy)
        print(
            "   Contains sub/c.txt:",
            os.path.exists(os.path.join(tree_copy, "sub", "c.txt")),
        )
        shutil.rmtree(tree_copy)

        # 3. Recursive delete of a directory with content (shutil.rmtree)
        # os.rmdir and pathlib.Path.rmdir fail on non-empty directories.
        print("\n3. Recursive directory delete (shutil.rmtree):")
        print("   Deleting source_dir with all content...")
        shutil.rmtree(src_dir)
        print("   source_dir exists after rmtree:", os.path.exists(src_dir))

        # 4. Cross-filesystem move (shutil.move handles it; os.rename fails)
        # We recreate src_dir for the following movement demonstration.
        print("\n4. Cross-filesystem move (shutil.move):")
        os.makedirs(src_dir, exist_ok=True)
        move_src = os.path.join(src_dir, "to_move.txt")
        with open(move_src, "w", encoding="utf-8") as f:
            f.write("move me")
        move_dst = os.path.join(base, "moved.txt")
        shutil.move(move_src, move_dst)
        print("   Moved to:", move_dst)
        print("   Source exists after move:", os.path.exists(move_src))
        os.remove(move_dst)

        # 5. Disk usage (shutil.disk_usage)
        print("\n5. Disk usage (shutil.disk_usage):")
        usage = shutil.disk_usage(base)
        print("   Total:", usage.total, "bytes")
        print("   Used:", usage.used, "bytes")
        print("   Free:", usage.free, "bytes")

        # 6. Find executable in PATH (shutil.which)
        print("\n6. Find executable in PATH (shutil.which):")
        for cmd in ["python", "python3", "notepad", "nonexistent_cmd_xyz"]:
            found = shutil.which(cmd)
            print(f"   {cmd}: {found}")

        # 7. Create and extract archives (shutil.make_archive / unpack_archive)
        print("\n7. Archive operations (shutil.make_archive / unpack_archive):")
        archive_base = os.path.join(base, "my_archive")
        os.makedirs(os.path.join(src_dir, "archive_inner"), exist_ok=True)
        with open(
            os.path.join(src_dir, "archive_inner", "z.txt"), "w", encoding="utf-8"
        ) as f:
            f.write("inside archive")
        shutil.make_archive(archive_base, "zip", src_dir)
        print("   Archive created:", archive_base + ".zip")
        extract_dir = os.path.join(base, "extracted")
        shutil.unpack_archive(archive_base + ".zip", extract_dir)
        print("   Extracted to:", extract_dir)
        print(
            "   Contains archive_inner/z.txt:",
            os.path.exists(os.path.join(extract_dir, "archive_inner", "z.txt")),
        )

    print("\n=== End of shutil_unique ===")


if __name__ == "__main__":
    main()
