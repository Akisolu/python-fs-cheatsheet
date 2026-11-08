"""
pathlib_unique.py
=================

Demonstrates features UNIQUE to the ``pathlib`` module that are not available
in ``os`` or ``shutil``.

These are object-oriented path operations: paths as objects with the `/`
operator, pure vs concrete paths, one-call read/write, glob pattern search,
path decomposition attributes, and more.
"""

import os
import tempfile
from pathlib import Path, PurePath


def main():
    print("=== Unique features of the `pathlib` module ===\n")

    with tempfile.TemporaryDirectory() as base:
        base_path = Path(base)

        # 1. Paths as objects with the / operator (no os.path.join)
        print("1. Paths as objects with the `/` operator:")
        subdir = base_path / "my_folder" / "nested"
        print("   Constructed path:", subdir)
        print("   Type:", type(subdir).__name__)

        # 2. Pure vs concrete paths (os has no such distinction)
        print("\n2. Pure vs concrete paths:")
        pure = PurePath("/tmp/some/file.txt")
        concrete = Path("/tmp/some/file.txt")
        print("   PurePath (manipulation only):", pure)
        print("   Path (can do I/O):", concrete)
        print("   PurePath has no I/O methods (no .read_text, .exists, etc.)")

        # 3. One-call read/write (no open() needed)
        print("\n3. One-call read/write:")
        text_file = subdir / "hello.txt"
        subdir.mkdir(parents=True, exist_ok=True)
        text_file.write_text("Hello from pathlib!", encoding="utf-8")
        print("   Written with write_text():", text_file.read_text(encoding="utf-8"))
        text_file.write_bytes(b"raw bytes content")
        print("   Written with write_bytes():", text_file.read_bytes())

        # 4. Glob / rglob pattern search
        print("\n4. Glob / rglob pattern search:")
        (subdir / "a.py").write_text("x = 1", encoding="utf-8")
        (subdir / "b.txt").write_text("y = 2", encoding="utf-8")
        (subdir / "c.py").write_text("z = 3", encoding="utf-8")
        py_files = list(subdir.glob("*.py"))
        print("   *.py files:", [p.name for p in py_files])
        # rglob searches recursively
        all_py = list(base_path.rglob("*.py"))
        print("   **/*.py (recursive):", [str(p.relative_to(base_path)) for p in all_py])

        # 5. iterdir yields Path objects directly (os.listdir yields strings)
        print("\n5. iterdir yields Path objects:")
        for p in base_path.iterdir():
            print("   -", p.name, "is_dir:", p.is_dir(), "type:", type(p).__name__)

        # 6. Path decomposition attributes
        print("\n6. Path decomposition attributes:")
        demo = subdir / "archive" / "notes.tar.gz"
        print("   Path:", demo)
        print("   .name:", demo.name)
        print("   .stem:", demo.stem)
        print("   .suffix:", demo.suffix)
        print("   .suffixes:", demo.suffixes)
        print("   .parent:", demo.parent)
        print("   .parts:", demo.parts)

        # 7. resolve() and expanduser() as methods
        print("\n7. resolve() and expanduser():")
        rel = subdir / ".." / "hello.txt"
        print("   Relative:", rel)
        print("   Resolved (absolute + symlinks resolved):", rel.resolve())
        home_expanded = Path("~/pathlib_demo").expanduser()
        print("   Expanded ~:", home_expanded)

        # 8. touch() - create file or update timestamp (like Unix touch)
        print("\n8. touch():")
        touched = subdir / "touched_file.txt"
        touched.touch()
        print("   Created/touched:", touched)
        print("   Exists:", touched.exists())
        touched.unlink()

        # 9. samefile() - inode-level comparison
        print("\n9. samefile():")
        f1 = subdir / "same_a.txt"
        f2 = subdir / "same_b.txt"
        f1.write_text("same content", encoding="utf-8")
        f2.write_text("same content", encoding="utf-8")
        # Different paths, different inodes -> not same file
        print("   Different paths, same content:", f1.samefile(f2))
        # Create hard link (same inode) if supported
        try:
            os.link(f1, f2)
            print("   After hard link, f1.samefile(f2):", f1.samefile(f2))
        except (OSError, NotImplementedError):
            print("   Hard links not supported on this system")

    print("\n=== End of pathlib_unique ===")


if __name__ == "__main__":
    main()
