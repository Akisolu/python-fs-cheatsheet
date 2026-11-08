# Comparison: `os` vs `shutil` vs `pathlib`

This document is a **decision guide and cross-reference** for choosing between Python's `os`, `shutil`, and `pathlib` modules. It complements `README.md` (which covers the basic demos) by focusing on **when to choose one over another**, **how to migrate between them**, and **common pitfalls to avoid**.

It is **not** a beginner tutorial. It assumes you already know what each module does and need practical guidance for real-world architecture decisions.

---

## 1. Quick Decision Flow

Use this logic to pick the right tool for the job:

```
Need environment variables, processes, or low-level file descriptors?
    └─▶ Use `os`

Need to copy, move, or delete directories WITH content (recursive)?
    └─▶ Use `shutil`

Need clean path manipulation, glob search, or object-oriented paths?
    └─▶ Use `pathlib`

Need more than one of the above?
    └─▶ Combine them (see Section 3)
```

---

## 2. API Cross-Reference

Same task, three different modules:

| Task | `os` / `os.path` | `shutil` | `pathlib` |
|------|------------------|----------|-----------|
| Join paths | `os.path.join(a, b)` | N/A | `a / b` |
| Check if file exists | `os.path.exists(p)` | N/A | `Path(p).exists()` |
| Get absolute path | `os.path.abspath(p)` | N/A | `Path(p).resolve()` |
| Get file extension | `os.path.splitext(p)[1]` | N/A | `Path(p).suffix` |
| Get file size | `os.path.getsize(p)` | N/A | `Path(p).stat().st_size` |
| List directory contents | `os.listdir(p)` | N/A | `[x.name for x in Path(p).iterdir()]` |
| Read text file | `open(p, "r").read()` | N/A | `Path(p).read_text()` |
| Write text file | `open(p, "w").write(t)` | N/A | `Path(p).write_text(t)` |
| Copy file (content only) | manual read/write | `shutil.copy(a, b)` | `shutil.copy(a, b)` (supports Path) |
| Copy file (+ metadata) | manual read/write | `shutil.copy2(a, b)` | `shutil.copy2(a, b)` (supports Path) |
| Move / rename file | `os.rename(a, b)` | `shutil.move(a, b)` | `Path(a).rename(b)` |
| Delete file | `os.remove(p)` | `os.remove(p)` | `Path(p).unlink()` |
| Delete empty directory | `os.rmdir(p)` | `os.rmdir(p)` | `Path(p).rmdir()` |
| Delete directory with content | ❌ Cannot alone | `shutil.rmtree(p)` | ❌ Cannot alone |
| Copy directory tree | ❌ Cannot alone | `shutil.copytree(a, b)` | ❌ Cannot alone |
| Create archive (zip/tar) | ❌ Cannot alone | `shutil.make_archive()` | ❌ Cannot alone |
| Extract archive | ❌ Cannot alone | `shutil.unpack_archive()` | ❌ Cannot alone |
| Get disk usage | ❌ Cannot alone | `shutil.disk_usage(p)` | ❌ Cannot alone |
| Find executable in PATH | ❌ Cannot alone | `shutil.which(cmd)` | ❌ Cannot alone |
| Environment variables | `os.environ` | N/A | N/A |
| Process management | `os.getpid()`, `os.fork()`, etc. | N/A | N/A |
| File descriptors (low-level I/O) | `os.open()`, `os.read()`, etc. | N/A | N/A |
| Permissions (chmod/chown) | `os.chmod()`, `os.chown()` | `shutil.chown()` | N/A |

---

## 3. Complementary Pattern: The Trio Works Together

These modules are **not mutually exclusive**. The most robust scripts combine them:

| Responsibility | Module |
|----------------|--------|
| Path construction and manipulation | `pathlib` |
| Heavy file/directory operations (copy tree, delete tree, archives) | `shutil` |
| Low-level OS tasks (env vars, processes, permissions, descriptors) | `os` |

**Example pattern:**
```python
from pathlib import Path
import shutil
import os

# pathlib: clean path handling
backup_dir = Path("/backups") / "daily"

# shutil: heavy lifting
shutil.make_archive(str(backup_dir / "data"), "zip", "/source")

# os: low-level OS task
os.chmod(backup_dir / "data.zip", 0o600)
```

---

## 4. Gotchas and Anti-Patterns

| Issue | Explanation | Fix |
|-------|-------------|-----|
| `os.chmod()` on Windows | Only toggles read-only; cannot set Unix-style permissions | Accept Windows limitation; use `stat` module for portable checks |
| `os.rename()` across filesystems | Raises `OSError` if source and destination are on different drives | Use `shutil.move()` instead |
| `Path.rmdir()` on non-empty dir | Raises `OSError`; unlike `shutil.rmtree()` it does not delete contents | Use `shutil.rmtree()` for non-empty dirs |
| `pathlib.Path` has no `.copy()` | Must use `read_bytes()`/`write_bytes()` or `shutil.copy2()` | Use `shutil.copy2()` for metadata preservation |
| Mixing strings and `Path` objects | Some `os` functions expect strings, not `Path` objects | Cast with `str(path_obj)` when passing to legacy `os` functions |
| `pathlib` performance on massive file counts | Creating `Path` objects for thousands of files is slower than `os.path` strings | Use `os.path` or `os.scandir()` for high-performance bulk operations |

---

## 5. Migration Guide: From `os` to `pathlib`

If you are modernizing legacy `os`-based code:

| Legacy (`os`) | Modern (`pathlib`) |
|---------------|--------------------|
| `os.path.join(base, "file.txt")` | `Path(base) / "file.txt"` |
| `os.path.exists(p)` | `Path(p).exists()` |
| `os.path.abspath(p)` | `Path(p).resolve()` |
| `os.path.splitext(p)[1]` | `Path(p).suffix` |
| `os.path.getsize(p)` | `Path(p).stat().st_size` |
| `os.listdir(p)` | `[x.name for x in Path(p).iterdir()]` |
| `open(p, "r").read()` | `Path(p).read_text()` |
| `open(p, "w").write(t)` | `Path(p).write_text(t)` |
| `os.remove(p)` | `Path(p).unlink()` |
| `os.rmdir(p)` | `Path(p).rmdir()` |
| `os.rename(a, b)` | `Path(a).rename(b)` |

---

## 6. Real-World Scenarios (Mixing Modules)

### Scenario A: Backup script with compression
```python
from pathlib import Path
import shutil

source = Path("/data")
backup = Path("/backups")
backup.mkdir(parents=True, exist_ok=True)
shutil.make_archive(str(backup / "daily"), "zip", source)
```

### Scenario B: Log rotation (delete old files)
```python
from pathlib import Path
import os

log_dir = Path("/var/log/myapp")
for log in log_dir.glob("*.log"):
    if log.stat().st_mtime < cutoff_time:
        log.unlink()  # pathlib for path handling + deletion
```

### Scenario C: Organize downloads by extension
```python
from pathlib import Path
import shutil

downloads = Path.home() / "Downloads"
for file in downloads.iterdir():
    if file.is_file():
        dest = downloads / file.suffix[1:] / file.name
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(file), str(dest))  # shutil for cross-filesystem move
```

---

## 7. Performance Notes

| Concern | Guidance |
|---------|----------|
| Path construction (`os.path.join` vs `/` operator) | Negligible difference; prefer `pathlib` for readability |
| Iterating 10,000+ files | `os.scandir()` or `os.listdir()` is faster than `pathlib.Path.iterdir()` because it avoids object creation overhead |
| One-off scripts | Readability of `pathlib` outweighs micro-optimization |
| Production bulk processing | Profile first; if path object creation is a bottleneck, switch to `os.path` strings |

---

## 8. Summary Rule of Thumb

> **Use `pathlib` for paths, `shutil` for heavy file operations, and `os` for everything else the operating system provides.**

If you find yourself writing `os.path.join()` inside a `shutil` call, consider switching to `Path` objects. If you find yourself needing `shutil.rmtree()` inside a `pathlib` script, that is expected — import `shutil` and keep going.
