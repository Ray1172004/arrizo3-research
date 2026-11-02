#!/usr/bin/env python3
"""Best-effort local Git prepublication check (not a substitute for human review)."""
import re
import subprocess
import sys
from pathlib import Path

BAD_SUFFIX = {".exe", ".dll", ".apk", ".rar", ".7z", ".zip", ".bin", ".img", ".rom", ".pem", ".key", ".dat", ".pcap", ".gpr", ".log", ".so"}
BAD_NAME = re.compile(r"ADBKEY|signature\\.dat|machine.?id|vin[-_]?raw", re.I)

def main():
    root = Path(__file__).resolve().parents[1]
    proc = subprocess.run(["git", "-C", str(root), "ls-files", "-z"], capture_output=True, check=True)
    paths = [p.decode("utf-8", "replace") for p in proc.stdout.split(b"\\0") if p]
    problems = [p for p in paths if Path(p).suffix.lower() in BAD_SUFFIX or BAD_NAME.search(p)]
    if problems:
        print("Potentially sensitive paths (do not publish):", *problems, sep="\\n")
        return 1
    print(f"Preflight passed for {len(paths)} tracked paths. Manual content and secret review still required.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
