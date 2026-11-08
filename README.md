# os vs shutil vs pathlib

A side-by-side comparison of Python's three main modules for file-system operations: **`os`**, **`shutil`**, and **`pathlib`**.

This repository contains example scripts and reference documentation showing how to perform the same file-system tasks with each module, plus the unique features of each.

## Repository structure

```
os_shutil_pathlib/
├── README.md                    # This file
├── LICENSE
├── examples/                    # Demo scripts with identical 13 operations
│   ├── README.md
│   ├── os_demo.py
│   ├── shutil_demo.py
│   └── pathlib_demo.py
└── unique_characteristics/      # Features unique to each module
    ├── README.md
    ├── os_unique.py
    ├── shutil_unique.py
    └── pathlib_unique.py
```

## What this repo demonstrates

### `examples/` — Common operations (same 13 steps in each demo)

Each demo script performs the **identical sequence of 13 file-system operations** inside a `tempfile.TemporaryDirectory()`, so you can compare them directly:

1. Create a subdirectory
2. Create a text file
3. List directory contents
4. Check if a file exists
5. Get absolute path
6. Get file extension
7. Get file size
8. Copy a file
9. Rename / move a file
10. Read file content
11. Delete the original file
12. Delete the renamed file
13. Delete the empty directory

| File | Module | Style |
|------|--------|-------|
| `examples/os_demo.py` | `os` + `os.path` | Strings + `os.path.join()` |
| `examples/shutil_demo.py` | `shutil` + `os.path` | High-level ops (`copy2`, `move`, `rmtree`) |
| `examples/pathlib_demo.py` | `pathlib` | Object-oriented `Path` objects |

### `unique_characteristics/` — Features unique to each module

Scripts that demonstrate capabilities only available in one module:

| File | Unique features |
|------|-----------------|
| `unique_characteristics/os_unique.py` | Environment variables, process management, file descriptors (low-level I/O), OS path constants, permissions (`chmod`), symlinks |
| `unique_characteristics/shutil_unique.py` | Copy with metadata (`copy2`), recursive copy/delete (`copytree`, `rmtree`), cross-filesystem move (`move`), disk usage (`disk_usage`), executable lookup (`which`), archive operations (`make_archive`, `unpack_archive`) |
| `unique_characteristics/pathlib_unique.py` | Paths as objects (`/` operator), pure vs concrete paths, one-call read/write (`read_text`/`write_text`), glob pattern search (`glob`/`rglob`), path decomposition (`.suffix`, `.stem`, `.name`), `resolve()`, `expanduser()`, `touch()`, `samefile()` |

## Quick reference: when to use each module

| Use case | Recommended module |
|----------|-------------------|
| Environment variables, processes, low-level I/O, permissions | `os` |
| Copy files with metadata, delete non-empty directories, move across filesystems, archives, disk usage | `shutil` |
| Readable path manipulation, glob search, one-call read/write, modern Python code | `pathlib` |
| Most general file tasks | `pathlib` (Python's current recommendation) |

## How to run the examples

From the repository root:

```powershell
python examples/os_demo.py
python examples/shutil_demo.py
python examples/pathlib_demo.py
```

```powershell
python unique_characteristics/os_unique.py
python unique_characteristics/shutil_unique.py
python unique_characteristics/pathlib_unique.py
```

Each script uses `tempfile.TemporaryDirectory()` internally, so nothing is left behind in the repository.

## Related documentation

- `examples/README.md` — Details about the demo scripts
- `unique_characteristics/README.md` — Details about the unique feature scripts
