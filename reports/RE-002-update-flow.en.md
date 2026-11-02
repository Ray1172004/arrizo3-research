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

## Technical references

- [RE-001 — Recursive directory cleanup](RE-001-cherylink-cleanup.en.md).
- [Microsoft — FindFirstFile on Windows CE](https://learn.microsoft.com/en-us/previous-versions/windows/embedded/ms923968%28v%3Dmsdn.10%29).
- [Microsoft — FindNextFile on Windows CE](https://learn.microsoft.com/en-us/previous-versions/windows/embedded/ms923971%28v%3Dmsdn.10%29).
- [Microsoft — FindClose on Windows CE](https://learn.microsoft.com/en-us/previous-versions/ms960590%28v%3Dmsdn.10%29).

Nothing in this reference Tiggo 2 sample establishes the operating system of the Arrizo 3 head unit.
