# Unique Characteristics: `os` vs `shutil` vs `pathlib`

This folder contains three scripts, each demonstrating features that are **unique** to one module and not available (or not directly available) in the other two.

## Files

| File | Module | Purpose |
|------|--------|---------|
| `os_unique.py` | `os` | Low-level OS operations |
| `shutil_unique.py` | `shutil` | High-level file/directory operations |
| `pathlib_unique.py` | `pathlib` | Object-oriented path operations |

---

## `os` — Unique features

- **Environment variables**: `os.environ`, `os.getenv()`, `os.putenv()` — no equivalent in `shutil` or `pathlib`.
- **Process management**: `os.getpid()`, `os.getppid()`, `os.getuid()`, `os.getgid()`, `os.getlogin()`, `os.system()`, `os.fork()` (Unix only).
- **File descriptors (low-level I/O)**: `os.open()`, `os.read()`, `os.write()`, `os.close()`, `os.dup()` — work with numeric descriptors, not file objects.
- **OS-specific path constants**: `os.sep`, `os.pathsep`, `os.curdir`, `os.pardir`, `os.linesep`.
- **Permissions**: `os.chmod()`, `os.chown()` (Unix), `os.umask()`.
- **Symlinks**: `os.symlink()`, `os.readlink()` — `os` is the underlying implementation.
- **Byte paths**: Can accept and return `bytes` paths.

## `shutil` — Unique features

- **`shutil.copy2()`**: Copies file content **plus metadata** (permissions, access/modification timestamps).
- **`shutil.copytree()`**: Recursively copies an entire directory tree.
- **`shutil.rmtree()`**: Recursively deletes a directory **and all its content**. The only one of the three that can remove a non-empty directory.
- **`shutil.move()`**: Moves files/directories, handling cross-filesystem moves (unlike `os.rename()`).
- **`shutil.disk_usage()`**: Returns total, used, and free disk space.
- **`shutil.which()`**: Locates an executable in the system `PATH`.
- **`shutil.make_archive()` / `shutil.unpack_archive()`**: Create and extract ZIP, TAR, and other archives.
- **`shutil.chown()`**: Change user/group ownership of a path.
- **`shutil.copyfileobj()`**: Copy between open file objects with configurable buffer size.

## `pathlib` — Unique features

- **Paths as objects**: `Path('/tmp') / 'file.txt'` uses the `/` operator instead of `os.path.join()`.
- **Pure vs concrete paths**: `PurePath` (manipulation only, no I/O) vs `Path` (concrete, can do I/O).
- **One-call read/write**: `.read_text()`, `.write_text()`, `.read_bytes()`, `.write_bytes()` — no `open()` needed.
- **Pattern search**: `.glob()` and `.rglob()` for glob-style file searching.
- **`.iterdir()`**: Yields `Path` objects directly (unlike `os.listdir()` which returns strings).
- **Path decomposition**: `.name`, `.stem`, `.suffix`, `.suffixes`, `.parent`, `.parts`.
- **`.resolve()` / `.expanduser()`**: Method-based absolute path resolution and home directory expansion.
- **`.touch()`**: Create a file or update its timestamp (like the Unix `touch` command).
- **`.samefile()`**: Inode-level comparison to check if two paths point to the same file.

---

## How to run

From the repository root:

```powershell
python unique_characteristics/os_unique.py
python unique_characteristics/shutil_unique.py
python unique_characteristics/pathlib_unique.py
```

Each script uses `tempfile.TemporaryDirectory()` internally, so nothing is left behind in the repository.
