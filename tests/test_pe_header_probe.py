"""Unit tests for the original read-only PE header parser."""
import struct
import tempfile
import unittest
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from pe_header_probe import inspect

class ProbeTests(unittest.TestCase):
    def test_arm_pe(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "sample.exe"
            data = bytearray(256)
            data[:2] = b"MZ"
            struct.pack_into("<I", data, 0x3c, 0x80)
            data[0x80:0x84] = b"PE\\0\\0"
            struct.pack_into("<HHI", data, 0x84, 0x1c0, 4, 0)
            p.write_bytes(data)
            found = inspect(p)
            self.assertEqual(found["machine"], "ARM")
            self.assertEqual(found["sections"], 4)

    def test_invalid_file(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "bad"
            p.write_bytes(b"not a PE")
            with self.assertRaises(ValueError):
                inspect(p)

if __name__ == "__main__":
    unittest.main()
