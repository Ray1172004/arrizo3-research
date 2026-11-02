# Chery Arrizo 3 OEM Head Unit Research — English

![Research status](https://img.shields.io/badge/status-in_progress-blue) ![Method](https://img.shields.io/badge/method-static_analysis-green) ![Vehicle](https://img.shields.io/badge/vehicle-unmodified-green)

[🇪🇸 Versión principal en español](README.md)

**Automotive security · Legacy infotainment · Firmware reverse engineering · Windows CE / ARM · Android projection**

> **Provenance matters:** The project studies a stock **2021 Chery Arrizo 3** infotainment unit. The update package analyzed to date is a **third-party Tiggo 2 CheryLink reference sample**. These findings **do not** establish that the Arrizo 3 uses the same hardware, firmware or operating system.

## Executive summary

This is an ongoing, non-invasive investigation into automotive infotainment. We observed the Arrizo 3 OEM interface, examined the QDrive mobile companion, and then analyzed a Tiggo 2 CheryLink package offline with `7z`, `file`, `strings` and Ghidra.

**Research question:** How does the reference CheryLink updater operate, and what must be established before safely acquiring the exact Arrizo 3 firmware?

**Safety boundary:** No firmware has been flashed or extracted from the installed vehicle. No ECU access, CAN injection, vehicle exploitation or proprietary binary redistribution.

## Verified findings vs unknowns

| Area | Observed finding | Scope / caveat |
| --- | --- | --- |
| Arrizo 3 version | `ARRIZO 3_02_31.01_170919_R` | Seen on OEM settings screen |
| OEM interfaces | USB-A, Bluetooth, Cloudrive, Radio, Media, CarInfo | Observed on vehicle |
| `T2 Android 10.rar` | RAR5; SHA-256 documented | **Tiggo 2 sample only** |
| `CheryLink.7z` | 1,515 files, 20 directories | Reference package |
| `CheryLink_Update.exe` | PE32 / Windows CE 6.00 / ARMv4T | Reference updater, **not proof of Arrizo OS** |
| Other programs | PE32 ARMv4T, Android APK and ELF components | Reference package |
| `FUN_00011008` | Directory traversal, recursion, deletion and named exceptions | Static analysis [RE-001](reports/RE-001-cherylink-cleanup.md) |
| Arrizo 3 firmware dump | **Not obtained** | OEM hardware/OS still unknown |
| Vulnerability or exploit | **Not found or claimed** | Research is behavioral, not exploitation |

## First reverse-engineering finding

Ghidra static analysis of `CheryLink_Update.exe` identifies a recursive directory-cleanup routine. It traverses the `CheryLink` tree, distinguishes files from directories, skips `EMMC_Check_File.txt`, handles a special deletion-failure condition for `ceusbkwrapperdrv.dll`, excludes `.` and `..` in recursion, and treats the top-level directory differently.

This does **not** mean the updater is a vulnerability, or that it can run on the Arrizo 3.

Read [RE-001](reports/RE-001-cherylink-cleanup.md) and [Ghidra workflow](docs/03-ghidra-wince.md).

## Project map

- [OEM observations](docs/01-oem-observations.md)
- [Tiggo 2 reference package triage](docs/02-reference-package.md)
- [Windows CE / ARM reversing with Ghidra](docs/03-ghidra-wince.md)
- [QDrive Android observations](docs/04-qdrive-android.md)
- [Safety and recovery boundary](docs/05-safety-and-recovery.md)
- [Next milestones](docs/06-roadmap.md)
- [Sources](docs/references.md)
- [Security and disclosure](SECURITY.md)

## Repeat the offline analysis

Obtain your own lawfully distributed reference sample in a private local directory. **Do not connect it to the car or install it on the head unit.**

```bash
file 'T2 Android 10.rar'
sha256sum 'T2 Android 10.rar'
7z l -pcherydianos 'T2 Android 10.rar'
# In a privately extracted directory:
7z l CheryLink.7z
python scripts/static_triage.py CheryLink_Update.exe --json
python scripts/pe_header_probe.py CheryLink_Update.exe
python -m unittest discover -s tests -v
python scripts/pre_publish_check.py
```

These original Python tools read local file metadata or headers; they **never execute vendor firmware**.

## Why no original update files, APKs or keys?

The reference package includes vendor binaries and names consistent with ADB private key material (`ADBKEY`). This repo publishes only original research, scripts and sanitized evidence, never manufacturer firmware, secrets, VIN, MachineID or private device logs.

## What's next?

1. Validate Windows CE API imports against the appropriate COREDLL ordinal exports.
2. Trace copy/extraction paths in the updater (RE-002).
3. Identify the real Arrizo 3 head-unit manufacturer and hardware revision.
4. Seek a model-matched firmware export and a tested recovery procedure before attempting modifications.

**Researcher:** [Ray1172004](https://github.com/Ray1172004) · **Status:** ongoing · **License:** MIT for original work only.
