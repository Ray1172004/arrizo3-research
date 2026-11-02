# Ghidra workflow — Windows CE ARMv4T

1. Import `CheryLink_Update.exe` (from a separately obtained, private sample) into a Ghidra non-shared project.
2. Allow auto-analysis. A missing PDB warning only means original debug symbols were unavailable.
3. Locate strings `begin remove file`, `remove file OK`, `UPDATE END` using Defined Strings.
4. Follow Xrefs to `entry`; inspect call at `0x00011504` to `FUN_00011008`.
5. Examine recursive directory cleanup and return paths; see [RE-001](../reports/RE-001-cherylink-cleanup.md).

Observed UTF-16LE values: `*.*` at `0x0002e060`, `.` at `0x0002e068`, and `..` at `0x0002e06c`. The implementation checks directory attribute bit `0x10` and excludes `EMMC_Check_File.txt` from normal deletion.

Caution: `COREDLL.dll` imports often appear as `Ordinal_N`. Match exact API signatures against the relevant Windows CE export table rather than assigning names from guesses.
