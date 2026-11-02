# RE-002 — Initial CheryLink_Update.exe control flow

**Sample:** `CheryLink_Update.exe` from a Tiggo 2 community CheryLink update.  
**Method:** Ghidra static analysis (PE32, Windows CE / ARMv4T).  
**Status:** partial analysis.

## Entry point

Within `entry`, a `begin remove file` log is followed by a call to `FUN_00011008(0x2e2d0)` near address `0x00011504`. The argument points to the Unicode string `\CheryLink`.

The return value is compared against zero. The zero-value branch logs `remove file OK` and continues into other updater operations.

```text
entry()
  ├─ log begin remove file
  ├─ FUN_00011008("\CheryLink")   [RE-001]
  └─ inspect return value
       ├─ zero → log remove file OK; continue
       └─ nonzero → alternative branch not yet traced
```

The recursive cleanup routine is documented in [RE-001](RE-001-cherylink-cleanup.en.md). A success log is not proof that every internal deletion succeeded.

## Additional observed strings

The sample contains `begin copy data`, `copy data success`, `ExtractFile OK`, `ExtractFile fail`, `UPDATE END` and `CHERYLINK//CheryLink.7z`.

These strings **suggest** a copy or archive-extraction stage, but do not alone establish sequence, integrity checks, destinations or error handling. These claims require following cross-references and reading the relevant functions.

## File opening and chunked reading

A further `entry` decompiler excerpt shows preparation of a file-read loop:

```c
Ordinal_56(&local_ac0, L"%s\\CheryLink.7z", &local_894);
local_8ac = Ordinal_1145(&local_ac0, &DAT_0002e388);
if (local_8ac == 0) { /* open fromfile fail */ }
else {
    local_8a8 = Ordinal_1113("CHERYLINK//CheryLink.7z", &DAT_0002e408);
    if (local_8a8 == 0) { /* open tofile fail */ }
    else {
        Ordinal_1130(local_8ac, 0, 2);
        local_8b4 = Ordinal_1131(local_8ac);
        Ordinal_1130(local_8ac, 0, 0);
        do {
            local_898 = Ordinal_1120(auStack_684, 1, 0x400, local_8ac);
            if ((local_898 == 0) || (local_898 == -1)) goto LAB_00011844;
            /* remaining body not yet examined */
        } while (/* condition not yet examined */);
    }
}
```

A community Windows Mobile 6.0 COREDLL export table maps ordinals `56`, `1145`, `1113`, `1130`, `1131`, `1120` to `wsprintfW`, `_wfopen`, `fopen`, `fseek`, `ftell`, `fread`. Ordinal `1121` is listed as `fwrite`, but **its call has not yet been observed in the provided excerpt**. Microsoft documents the API signatures; exact ordinal assignments for the sampled library remain to be validated.

**Interpretation:** the updater builds a source filename ending in `CheryLink.7z`, opens source and destination streams, seeks to the source end, obtains the file position (likely size), returns to its beginning and requests chunks of at most `0x400` (1024) bytes.

The file modes reside at `DAT_0002e388` and `DAT_0002e408`, not yet inspected. The actual write operation, completed-byte checks and archive extraction stage are **not yet demonstrated**. This section documents setup and reading, not a verified complete copy.

## Technical references

- [RE-001 — Recursive directory cleanup](RE-001-cherylink-cleanup.en.md).
- [Microsoft — FindFirstFile on Windows CE](https://learn.microsoft.com/en-us/previous-versions/windows/embedded/ms923968%28v%3Dmsdn.10%29).
- [Microsoft — FindNextFile on Windows CE](https://learn.microsoft.com/en-us/previous-versions/windows/embedded/ms923971%28v%3Dmsdn.10%29).
- [Microsoft — FindClose on Windows CE](https://learn.microsoft.com/en-us/previous-versions/ms960590%28v%3Dmsdn.10%29).

- [Microsoft — fopen / _wfopen (Windows CE)](https://learn.microsoft.com/en-us/previous-versions/windows/embedded/ms859631%28v%3Dmsdn.10%29).
- [Microsoft — fseek (Windows CE)](https://learn.microsoft.com/en-us/previous-versions/windows/embedded/ms859641%28v%3Dmsdn.10%29).
- [Microsoft — ftell (Windows CE)](https://learn.microsoft.com/en-us/previous-versions/windows/embedded/ms859644%28v%3Dmsdn.10%29).
- [Listado comunitario de exportaciones COREDLL (Windows Mobile 6.0)](https://www.cnblogs.com/huanglong/archive/2012/03/13/2393275.html) — útil como referencia, no confirmado para este dispositivo.

Nothing in this reference Tiggo 2 sample establishes the operating system of the Arrizo 3 head unit.
