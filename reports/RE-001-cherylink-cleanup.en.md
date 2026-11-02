[Leer en español](RE-001-cherylink-cleanup.md)

# RE-001 — Recursive directory-cleanup logic in CheryLink_Update.exe

**Type:** behavioral reverse engineering, NOT a vulnerability finding.  
**Sample:** third-party Tiggo 2 CheryLink reference update.  
**Method:** offline Ghidra static decompilation, ARMv4T PE32 / Windows CE.

## Finding

Function `FUN_00011008` accepts a directory path, enumerates child entries, checks the directory bit `0x10`, recursively visits child directories (excluding `.` and `..`), and uses conditional file deletion. It treats `EMMC_Check_File.txt` as an exception; a failed deletion of `ceusbkwrapperdrv.dll` is tolerated. The top-level `\\CheryLink` folder is treated differently from children. An examined error path returns `0xffffffff`; regular completion returns zero.

## Evidence

| Observation | Evidence |
| --- | --- |
| Callsite | `entry` at approximately `0x00011504` calls `FUN_00011008(0x2e2d0)` |
| Wildcard | UTF-16LE `*.*` at `0x0002e060` |
| Avoid self and parent | `.` at `0x0002e068`; `..` at `0x0002e06c` |
| File/directory check | `local_344[0] & 0x10` |
| Skip one file | `wcscmp`-like comparison with `EMMC_Check_File.txt` |
| Tolerated delete failure | `ceusbkwrapperdrv.dll` special case |
| Recurse | Self-call to `FUN_00011008` |
| Preserve base folder | Special comparison with `\\CheryLink` before directory removal |

## Behavioral reconstruction (original summary, not vendor source)

```text
cleanup(path):
    enumerate entries in path
    for entry in entries:
        if regular file:
            skip EMMC_Check_File.txt
            try deletion
            if deletion fails and filename != ceusbkwrapperdrv.dll:
                return failure
        elif directory and name not in {'.','..'}:
            if cleanup(child_path) fails:
                return failure
    if path != '\\CheryLink':
        attempt directory removal
    return normal completion
```

## Confidence / limitations

**High:** observed static control flow, recursion, comparisons, special paths. **Medium:** assignments of specific Windows CE APIs to imported ordinals, pending validation against matching COREDLL exports. **Unknown:** anything about installed Arrizo 3 firmware; this sample is for Tiggo 2. No code execution on a vehicle, no security exploit.
