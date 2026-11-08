# Examples: `os` vs `shutil` vs `pathlib`

This folder contains three demo scripts that perform the **same 13 file-system operations** using three different Python modules. They are designed for side-by-side comparison.

## Files

| File | Module | Description |
|------|--------|-------------|
| `os_demo.py` | `os` + `os.path` | Low-level operations using strings and `os.path` |
| `shutil_demo.py` | `shutil` + `os.path` | High-level operations (copy with metadata, recursive delete, etc.) |
| `pathlib_demo.py` | `pathlib` | Object-oriented path operations using `Path` objects |

## Common operations demonstrated

All three demos execute the identical sequence of 13 operations inside a `tempfile.TemporaryDirectory()`:

1. Create a subdirectory
2. Create a text file inside it
3. List base directory contents
4. Check if a file exists
5. Get absolute path
6. Get file extension
7. Get file size (bytes)
8. Copy a file
9. Rename / move a file
10. Read file content
11. Delete the original file
12. Delete the renamed file
13. Delete the empty directory

## Key differences between demos

| Aspect | `os_demo.py` | `shutil_demo.py` | `pathlib_demo.py` |
|--------|-------------|------------------|-------------------|
| Path style | Strings + `os.path.join()` | Strings + `os.path.join()` | `Path` objects with `/` operator |
| File creation | `open().write()` | `open().write()` | `Path.write_text()` |
| File reading | `open().read()` | `open().read()` | `Path.read_text()` |
| Copy | Manual read/write | `shutil.copy2()` (metadata preserved) | `read_bytes()` / `write_bytes()` |
| Move/rename | `os.rename()` | `shutil.move()` | `Path.rename()` |
| Delete file | `os.remove()` | `os.remove()` | `Path.unlink()` |
| Delete folder | `os.rmdir()` (empty only) | `shutil.rmtree()` (with content) | `Path.rmdir()` (empty only) |
| Temp directory cleanup | Automatic | Automatic | Automatic |

## How to run

From the repository root:

```powershell
python examples/os_demo.py
python examples/shutil_demo.py
python examples/pathlib_demo.py
```

Each script creates its own temporary directory, runs the operations, prints the results, and cleans up automatically. Nothing is left behind in the repository.

## Related documentation

- `unique_characteristics/README.md` — Features unique to each module (`os`, `shutil`, `pathlib`)
- `unique_characteristics/os_unique.py` — Low-level OS features unique to `os`
- `unique_characteristics/shutil_unique.py` — High-level operations unique to `shutil`
- `unique_characteristics/pathlib_unique.py` — Object-oriented features unique to `pathlib`
