#!/usr/bin/env python3
"""Read-only PE signature / architecture triage for local samples."""
import argparse
import json
import struct
from pathlib import Path

MACHINES = {0x1c0: "ARM", 0x1c2: "Thumb", 0x1c4: "ARMv7", 0x14c: "x86", 0x8664: "x86-64", 0xaa64: "ARM64"}

def inspect(path):
    p = Path(path)
    with p.open("rb") as f:
        hdr = f.read(64)
        if len(hdr) < 64 or hdr[:2] != b"MZ":
            raise ValueError("Not a valid DOS/MZ header")
        pe_offset = struct.unpack_from("<I", hdr, 0x3c)[0]
        if pe_offset > p.stat().st_size - 24:
            raise ValueError("PE offset outside file")
        f.seek(pe_offset)
        pe = f.read(24)
    if len(pe) < 24 or pe[:4] != b"PE\\0\\0":
        raise ValueError("Missing PE signature")
    machine, sections, stamp = struct.unpack_from("<HHI", pe, 4)
    return {"file": str(p), "machine_hex": f"0x{machine:04x}", "machine": MACHINES.get(machine, "Unknown"), "sections": sections, "timestamp": stamp}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file")
    args = parser.parse_args()
    try:
        print(json.dumps(inspect(args.file), indent=2))
    except (ValueError, OSError) as exc:
        parser.exit(1, f"error: {exc}\\n")
