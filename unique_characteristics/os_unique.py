"""
os_unique.py
============

Demonstrates features UNIQUE to the ``os`` module that are not available
in ``shutil`` or ``pathlib``.

These are low-level operating system operations: environment variables,
processes, file descriptors, user/group info, and OS-specific path
constants.
"""

import os
import platform
import tempfile


def main():
    print("=== Unique features of the `os` module ===\n")

    # 1. Environment variables (no equivalent in shutil or pathlib)
    print("1. Environment variables:")
    print("   PATH:", os.environ.get("PATH", "")[:80], "...")
    print("   USER:", os.environ.get("USER", os.environ.get("USERNAME", "")))
    os.environ["MY_DEMO_VAR"] = "hello-from-os"
    print("   MY_DEMO_VAR set to:", os.environ.get("MY_DEMO_VAR"))

    # 2. Process information
    print("\n2. Process information:")
    print("   Current PID:", os.getpid())
    print("   Parent PID:", os.getppid())
    if platform.system() != "Windows":
        print("   User ID (uid):", os.getuid())
        print("   Group ID (gid):", os.getgid())
        print("   Login name:", os.getlogin())

    # 3. File descriptors (low-level I/O, not file objects)
    print("\n3. File descriptors (low-level I/O):")
    fd, tmp_path = tempfile.mkstemp()
    os.write(fd, b"low-level write via os.write\n")
    os.close(fd)
    with open(tmp_path, "r", encoding="utf-8") as f:
        print("   Content written via os.write:", f.read().strip())
    os.remove(tmp_path)

    # 4. OS-specific path constants
    print("\n4. OS-specific path constants:")
    print("   Separator (os.sep):", repr(os.sep))
    print("   Path separator (os.pathsep):", repr(os.pathsep))
    print("   Current dir (os.curdir):", repr(os.curdir))
    print("   Parent dir (os.pardir):", repr(os.pardir))
    print("   Line separator (os.linesep):", repr(os.linesep))

    # 5. Permissions (chmod / umask)
    print("\n5. Permissions:")
    demo_file = os.path.join(tempfile.gettempdir(), "os_demo_perms.txt")
    with open(demo_file, "w", encoding="utf-8") as f:
        f.write("permission demo")
    print("   Before chmod:", oct(os.stat(demo_file).st_mode & 0o777))
    os.chmod(demo_file, 0o600)
    print("   After chmod 600:", oct(os.stat(demo_file).st_mode & 0o777))
    os.remove(demo_file)

    # 6. Symlinks (os is the underlying implementation)
    print("\n6. Symbolic links:")
    target = os.path.join(tempfile.gettempdir(), "os_symlink_target.txt")
    link = os.path.join(tempfile.gettempdir(), "os_symlink_link.txt")
    with open(target, "w", encoding="utf-8") as f:
        f.write("symlink target")
    try:
        os.symlink(target, link)
        print("   Symlink created:", link)
        print("   Read link:", os.readlink(link))
        os.remove(link)
    except (OSError, NotImplementedError) as e:
        print("   Symlink not supported/privileged:", e)
    finally:
        if os.path.exists(target):
            os.remove(target)

    print("\n=== End of os_unique ===")


if __name__ == "__main__":
    main()
