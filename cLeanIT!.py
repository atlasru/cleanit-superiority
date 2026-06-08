#!/usr/bin/env python3

import os
import sys
import ctypes
import subprocess
from pathlib import Path
from typing import Set
import winreg

if sys.stdout.isatty():
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    GRAY = "\033[90m"
    WHITE = "\033[97m"
    RESET = "\033[0m"
else:
    GREEN = RED = YELLOW = GRAY = WHITE = RESET = ""

def color_text(text: str, color: str) -> str:
    return f"{color}{text}{RESET}"

def print_border():
    print(color_text("+" + "-" * 51 + "+", RED))

def print_divider():
    print(color_text("+" + "-" * 51 + "+", RED))

def print_row(text: str, color: str = WHITE):
    padded = text.ljust(52)[:52]
    sys.stdout.write(color_text("| ", RED))
    sys.stdout.write(color_text(padded, color))
    print(color_text("|", RED))

def print_ok(msg: str):
    print(f"      {color_text('[+]', GREEN)} {msg}")

def print_del(msg: str):
    print(f"      {color_text('[-]', YELLOW)} {msg}")

def print_warn(msg: str):
    print(f"      {color_text('[!]', GRAY)} {msg}")

def print_step(step: str, title: str):
    print()
    sys.stdout.write(f"  {color_text(f'[{step}]', RED)} ")
    print(color_text(title, WHITE))

def print_banner():
    os.system("cls" if os.name == "nt" else "clear")
    ascii_art = r"""
               __                     _____  _____  _        
__/\__   ___  / /  ___  __ _ _ __     \_   \/__   \/ \ __/\__
\    /  / __|/ /  / _ \/ _` | '_ \     / /\/  / /\/  / \    /
/_  _\ | (__/ /__|  __/ (_| | | | | /\/ /_   / / /\_/  /_  _\
  \/    \___\____/\___|\__,_|_| |_| \____/   \/  \/      \/
"""
    for line in ascii_art.splitlines():
        if line.strip():
            print(color_text(line, YELLOW))
    print_border()
    print_row("  Superiority Cleaner V1.0", RED)
    print_row("  by d9vh  ", GRAY)
    print_divider()
    print_row("")
    print_row("  Removes all traces of Superiority:", WHITE)
    for line in [
        "    * AppData (Roaming / Local)",
        "    * Temp, Program Files, ProgramData",
        "    * Documents, Downloads, Desktop",
        "    * Windows Registry",
        "    * USN Journal (NTFS traces)",
        "    * Windows Event Logs",
    ]:
        print_row(line, GRAY)
    print_row("")
    print_border()
    print()

def is_admin() -> bool:
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def elevate_and_run():
    script = os.path.abspath(sys.argv[0])
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f'"{script}"', None, 1)
    sys.exit()

def scan_and_delete(path: str, pattern: str = "superiority") -> int:
    deleted = 0
    path = Path(path)
    if not path.exists():
        return 0
    try:
        for root, dirs, files in os.walk(path, topdown=False):
            root_path = Path(root)
            for f in files:
                if pattern.lower() in f.lower():
                    file_path = root_path / f
                    try:
                        file_path.unlink()
                        print_del(f"File:   {f}")
                        deleted += 1
                    except Exception:
                        print_warn(f"Locked: {f}")
            for d in dirs:
                if pattern.lower() in d.lower():
                    dir_path = root_path / d
                    try:
                        import shutil
                        shutil.rmtree(dir_path, ignore_errors=False)
                        print_del(f"Folder: {d}")
                        deleted += 1
                    except Exception:
                        print_warn(f"Locked folder: {d}")
    except Exception:
        pass
    return deleted

def delete_registry_key(key_path: str) -> bool:
    try:
        parts = key_path.split('\\', 1)
        hive_str = parts[0]
        subkey = parts[1] if len(parts) > 1 else ""
        hive_map = {
            "HKCU": winreg.HKEY_CURRENT_USER,
            "HKLM": winreg.HKEY_LOCAL_MACHINE,
        }
        if hive_str not in hive_map:
            return False
        hive = hive_map[hive_str]
        winreg.DeleteKeyEx(hive, subkey, access=winreg.KEY_WOW64_64KEY)
        return True
    except WindowsError as e:
        if e.winerror == 2:  # key not found
            return False
        try:
            with winreg.OpenKeyEx(hive, subkey, 0, winreg.KEY_SET_VALUE | winreg.KEY_WOW64_64KEY) as key:
                winreg.DeleteKey(key, "")
            return True
        except:
            return False
    except:
        return False

def remove_autorun_entry() -> bool:
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                             r"Software\Microsoft\Windows\CurrentVersion\Run",
                             0, winreg.KEY_SET_VALUE | winreg.KEY_WOW64_64KEY)
        winreg.DeleteValue(key, "Superiority")
        winreg.CloseKey(key)
        return True
    except:
        return False

def clear_usn_journal(drive: str) -> bool:
    if not Path(drive).exists():
        return False
    try:
        subprocess.run(f'fsutil usn deletejournal /D {drive}', shell=True, check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except:
        return False

def clear_event_log(log_name: str) -> bool:
    try:
        subprocess.run(f'wevtutil cl "{log_name}"', shell=True, check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except:
        return False

def main():
    if not is_admin():
        print(color_text("  [!] Requesting admin rights...", YELLOW))
        elevate_and_run()

    print_banner()

    input(color_text("  Press ENTER to start, Ctrl+C to cancel.", GRAY))
    print()

    total_deleted = 0

    print_step("1/4", "Scanning file system...")

    scan_paths: Set[str] = set()
    for env in ["APPDATA", "LOCALAPPDATA", "TEMP", "ProgramFiles", "ProgramFiles(x86)", "ProgramData"]:
        p = os.environ.get(env)
        if p and Path(p).exists():
            scan_paths.add(p)

    user = os.environ.get("USERPROFILE", "")
    for sub in ["Documents", "Downloads", "Desktop"]:
        p = Path(user) / sub
        if p.exists():
            scan_paths.add(str(p))

    for path in sorted(scan_paths):
        print(f"    -> {path}")
        total_deleted += scan_and_delete(path)

    print_step("2/4", "Cleaning registry...")
    registry_keys = [
        "HKCU\\Software\\Superiority",
        "HKLM\\Software\\Superiority",
        "HKCU\\Software\\Classes\\superiority"
    ]
    for key in registry_keys:
        if delete_registry_key(key):
            print_ok(f"Deleted: {key}")
            total_deleted += 1
        else:
            print_warn(f"Cannot delete: {key}")

    if remove_autorun_entry():
        print_ok("Removed autorun")
        total_deleted += 1
    else:
        print_warn("Cannot remove autorun")

    print_step("3/4", "Clearing USN Journal...")
    for drive in "CDEFG":
        if clear_usn_journal(f"{drive}:"):
            print_ok(f"USN cleared: {drive}:")
            total_deleted += 1
        else:
            print_warn(f"USN {drive}: failed")

    print_step("4/4", "Clearing event logs...")
    logs = ["Microsoft-Windows-NTFS/Operational", "System", "Security", "Application"]
    for log in logs:
        if clear_event_log(log):
            print_ok(f"Log cleared: {log}")
            total_deleted += 1
        else:
            print_warn(f"Log {log}: error")

    print()
    print_border()
    if total_deleted > 0:
        print_row(f"  DONE!  Objects removed: {total_deleted}", GREEN)
    else:
        print_row("  Clean -- no Superiority traces found.", GREEN)
    print_border()
    print()
    input(color_text("  Press ENTER to exit...", GRAY))

if __name__ == "__main__":
    main()