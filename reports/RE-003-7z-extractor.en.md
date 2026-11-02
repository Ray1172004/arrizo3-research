# RE-003 — Identifying the embedded 7z extractor in CheryLink

[Español](RE-003-7z-extractor.md)

**Sample:** `CheryLink_Update.exe`, from a **Tiggo 2** community reference update. **Environment:** Ghidra, Windows CE ARMv4T PE32.

## Decoder identification

Following `entry → FUN_000141c0 → FUN_000135c8` revealed a routine that opens a 7z archive, walks its file entries, decompresses data and creates output directories and files.

The function closely matches **`7zMain.c`, the 7z decoder sample bundled with Igor Pavlov's LZMA SDK**: initialization order, the ten-parameter extraction call, UTF-16 name handling, directory creation, output file operations, error messages and the final `Everything is Ok` string all align with the sample implementation.

This provides **high-confidence source-family attribution**, but not binary-identical proof or an exact SDK revision.

## Reconstructed function mapping

| Ghidra | Likely LZMA SDK equivalent | Supporting behavior |
| --- | --- | --- |
| `FUN_00014eb4` | `SzArEx_Open` | Opens archive structure |
| `FUN_00014d70` | `SzArEx_GetFileNameUtf16` | Queries name length and fills buffer |
| `FUN_00019978` | `SzArEx_Extract` | Matching call signature and context |
| `FUN_00013ef0` | `MyCreateDir` | Creates directories from entry paths |
| `FUN_00013f4c` | `OutFile_OpenUtf16` | Opens extracted output file |
| `FUN_0001a100` | `File_Write` | Writes extracted data |
| `FUN_00019f6c` | `File_Close` | Closes output file |
| `FUN_000149f4` | `SzArEx_Init` | Initializes archive state |
| `FUN_00014a68` | `SzArEx_Free` | Frees archive resources |

These names are **analyst-assigned functional equivalents**, not symbols recovered from the binary.

## Reconstructed flow

```text
entry()
  └── FUN_000141c0()
        └── FUN_000135c8()
              ├── open CheryLink.7z
              ├── initialize extraction context
              ├── parse 7z archive structure
              ├── iterate archived entries
              │     ├── retrieve UTF-16 filename
              │     ├── decompress file data
              │     ├── prepare paths and directories
              │     └── open, write and close output files
              ├── release buffers and close archive
              └── return 0 on success, 1 on error
```

The sample's `can not open input file`, `can not open output file`, `can not write output file`, `can not close output file` and `Everything is Ok` messages also occur in the public LZMA SDK example.

## Confirmed extraction paths

Inspecting the string constants passed to `FUN_000141c0` in Ghidra revealed two ASCII values:

| Address | String | Role |
| --- | --- | --- |
| `0x0002e51c` | `CHERYLINK//CheryLink.7z` | 7z input archive |
| `0x0002e510` | `CHERYLINK` | Base directory for extracted output |

The `entry` call can therefore be read as follows (illustrative notation, not original source code):

```c
FUN_000141c0("CHERYLINK//CheryLink.7z", "CHERYLINK");
```

`FUN_000141c0` forwards the first argument to `FUN_000135c8`; it prepares the second argument in a local buffer before passing it as an output directory. Both strings are **relative paths**, so the absolute location depends on the updater's execution context. This finding concerns a **Tiggo 2** reference package, not firmware extracted from an Arrizo 3.

## Relevant decompiled calls

Archive entry extraction:

```c
local_4950 = FUN_00019978(
    aiStack_494c, auStack_46f0, local_49c,
    local_498 + 1, local_498,
    (uint *)(local_498 + 2),
    &local_480, (int *)&local_484,
    &local_6c0, &local_6c8
);
```

Output writing:

```c
local_18 = FUN_0001a100(
    &iStack_47c, local_498[0] + local_480, &local_60
);
```

The function also creates intermediate directories from archive entry separators. **Path handling with malicious archive names has not been validated, and this is not a vulnerability claim.**

## Verifying `FUN_00013ef0`: directory creation

Ghidra exposes the following code:

```c
iVar1 = Ordinal_160(param_1, 0);
if (iVar1 == 0) {
    local_14 = Ordinal_516();
} else {
    local_14 = 0;
}
return local_14;
```

A historical `COREDLL.dll` export mapping associates `Ordinal_160` with `CreateDirectoryW` and `Ordinal_516` with `GetLastError`. This exactly matches the behavior of `MyCreateDir` in the 2010 `7zMain.c` example: **return zero when a directory is created, otherwise return the OS error code**.

Some calls to `FUN_00013ef0` in `FUN_000135c8` do not immediately check the return value. This resembles the upstream example and alone does not demonstrate a security vulnerability. `CreateDirectoryW` creates only the final path component; parent directories must be prepared by the caller.

Sources: [`7zMain.c`](https://android.googlesource.com/platform/external/lzma/+/kitkat-dev/C/Util/7z/7zMain.c) · [Microsoft: CreateDirectory on Windows CE](https://learn.microsoft.com/en-us/previous-versions/windows/embedded/aa517316%28v%3Dmsdn.10%29) · [Historical COREDLL ordinals](https://blog.ch3cooh.jp/entry/20100803/1280838036).

This analysis concerns a **Tiggo 2** reference package, not the installed **Arrizo 3** firmware. No vehicle modifications have occurred.

## Source comparison

- [LZMA SDK — `7zMain.c` historical source hosted by Android Open Source Project](https://android.googlesource.com/platform/external/lzma/+/kitkat-dev/C/Util/7z/7zMain.c).
- [LZMA SDK — 7-Zip project site](https://sevenzip.sourceforge.io/sdk.html).
- [RE-002 — File copy and extractor invocation](RE-002-update-flow.en.md).
