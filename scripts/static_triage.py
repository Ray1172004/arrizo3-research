#!/usr/bin/env python3
"""Static, non-executing metadata triage of local binary samples."""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path

def triage(path):
    p = Path(path)
    if not p.is_file():
        raise FileNotFoundError(p)
    digest = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(chunk)
    try:
        result = subprocess.run(["file", "-b", "--", str(p)], capture_output=True, text=True, check=True, timeout=10)
        kind = result.stdout.strip()
    except (FileNotFoundError, subprocess.SubprocessError):
        kind = "Unavailable"
    return {"name": p.name, "size_bytes": p.stat().st_size, "sha256": digest.hexdigest(), "file_type": kind}

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    result = triage(args.path)
    print(json.dumps(result, indent=2) if args.json else "\\n".join(f"{k}: {v}" for k, v in result.items()))
