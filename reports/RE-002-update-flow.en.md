# RE-002 — CheryLink_Update.exe copy and extraction preparation

[Español](RE-002-update-flow.md)

Sample: `CheryLink_Update.exe` from a community **Tiggo 2** CheryLink update. Offline Ghidra static analysis of a Windows CE ARMv4T PE32 binary. This is **not** an Arrizo 3 firmware dump.

## Observed execution flow

The `entry` function logs `begin remove file` and calls `FUN_00011008` (see [RE-001](RE-001-cherylink-cleanup.en.md)). On a zero return code:

1. Format a source path ending in `\\CheryLink.7z` via `Ordinal_56`.
2. Open the source with `Ordinal_1145` (consistent with `_wfopen`).
3. Open destination `CHERYLINK//CheryLink.7z` with `Ordinal_1113` (consistent with `fopen`).
4. Seek to the end, read the source position, then return to the beginning using `Ordinal_1130`, `Ordinal_1131` and `Ordinal_1130` (consistent with `fseek` / `ftell`).
5. Read up to `0x400` bytes (1024) via `Ordinal_1120` (`fread`) and write with `Ordinal_1121` (`fwrite`).
6. Compare counted written bytes (`local_8a0`) against source end position (`local_8b4`). If equal, log `copy data success` and close both streams using `Ordinal_1118` (`fclose`).
7. Call `FUN_000141c0(0x2e51c, 0x2e510)`. A zero return produces `ExtractFile OK` and an attempt to delete the temporary `CHERYLINK//CheryLink.7z` through `Ordinal_165` (consistent with `DeleteFileW`). Otherwise the program logs `ExtractFile fail`.

Ordinal mappings are consistent with Windows Mobile 6.0 COREDLL community exports and Microsoft C runtime documentation. The exact export table used by this binary has not been obtained.

## Read/write loop

The following fragment is taken from the shared Ghidra decompilation:

```c
local_898 = Ordinal_1120(auStack_684, 1, 0x400, local_8ac);
if ((local_898 == 0) || (local_898 == -1)) goto LAB_00011844;

local_8a4 = auStack_684;
while (true) {
    local_8b0 = Ordinal_1121(local_8a4, 1, local_898, local_8a8);
    if ((local_8b0 == 0) || (local_8b0 == -1)) goto LAB_00011830;
    if (local_8b0 == local_898) break;
    if (0 < local_8b0) {
        local_8a4 = local_8a4 + local_8b0;
        local_898 = local_898 - local_8b0;
    }
    local_8a0 = local_8a0 + local_8b0;
}
local_8a0 = local_8a0 + local_8b0;
```

After a positive partial write, it advances the buffer pointer and retries the remaining bytes. The comparison is a **byte-count check**, not a cryptographic content check. Additional validation could occur inside the extraction routine; that has not been inspected.

## Error handling observation

Source-open, destination-open, copy and extraction failures have separate log messages.

When both streams opened successfully, `entry` ultimately sets `local_74 = 0` even after logging `copy data fail` or `ExtractFile fail`. An external caller relying only on the exit status might therefore miss these failures. No such caller or exploitable impact has been demonstrated.

The actual mode strings at `DAT_0002e388` and `DAT_0002e408` have not yet been inspected. The body of `FUN_000141c0` remains to be reviewed.

## References

- [RE-001 — Recursive cleanup](RE-001-cherylink-cleanup.en.md).
- [fopen / _wfopen, Microsoft Windows CE](https://learn.microsoft.com/en-us/previous-versions/windows/embedded/ms859631%28v%3Dmsdn.10%29).
- [fwrite, Microsoft Windows CE](https://learn.microsoft.com/en-us/previous-versions/windows/embedded/ms859645%28v%3Dmsdn.10%29).
- [ftell, Microsoft Windows CE](https://learn.microsoft.com/en-us/previous-versions/windows/embedded/ms859644%28v%3Dmsdn.10%29).
- [COREDLL Windows Mobile 6.0 community exports](https://www.cnblogs.com/huanglong/archive/2012/03/13/2393275.html).
