<div align="center">

# 🚘 R3TR0 | Arrizo 3 Research

**Reverse engineering a legacy automotive infotainment system: Chery Arrizo 3, CheryLink and Windows CE.**

[Español](README.md) · **English**

![Automotive](https://img.shields.io/badge/Automotive-Security-B49AFF) ![Windows CE](https://img.shields.io/badge/Windows_CE-ARMv4T-8A70DB) ![Ghidra](https://img.shields.io/badge/Ghidra-Reversing-7E65BD) ![Status](https://img.shields.io/badge/Status-Research_in_progress-orange)

*Static analysis · embedded firmware · Ghidra · reproducible research · no vehicle modification*

</div>

## About

**Arrizo 3 Research** is my learning and research project focused on the original head unit of a **2021 Chery Arrizo 3**. The goal is to identify its actual architecture and understand update mechanisms before considering any firmware acquisition or modification.

**Status: ongoing research.** I have documented the radio's visible software version and performed offline analysis of a **separate Tiggo 2 CheryLink update** as a comparative reference sample. **The Arrizo 3 OS is not yet identified, no original firmware has been extracted, and no vulnerability has been discovered.**

## Components and tools

| Component | Role |
|---|---|
| 2021 Chery Arrizo 3 | Unmodified OEM head unit under study |
| Tiggo 2 CheryLink package | Reference sample only; **not** proven compatible |
| Arch Linux | Analysis workstation |
| Ghidra | Windows CE ARMv4T binary reverse engineering |
| `file`, `7z`, `strings`, `sha256sum` | Offline triage and integrity tracking |
| JADX / ADB | Android QDrive companion investigation, phone-side only |
| Python | Original metadata and pre-publication scripts |
| Cardputer with Bit Pirate | Available for future isolated bench research; **not connected to the vehicle** |

## Initial results

| Evidence | Finding | Scope |
|---|---|---|
| OEM displayed version | `ARRIZO 3_02_31.01_170919_R` | Observed on Arrizo 3 |
| `CheryLink_Update.exe` | PE32, Windows CE 6.00, ARMv4T | **Tiggo 2** sample |
| `CheryLink.7z` | 1,515 files, 20 directories | Reference archive |
| Companion components | PE executables, Android APK and ARM ELF | Reference archive |
| `FUN_00011008` | Recursive directory cleanup and exceptions | [RE-001 finding](reports/RE-001-cherylink-cleanup.en.md) |

RE-001 describes a routine that traverses directories, skips `.` and `..`, excludes `EMMC_Check_File.txt`, and handles a special case for `ceusbkwrapperdrv.dll`. **This is behavioral reverse engineering, not an exploit.**

## Preview and evidence

**Coming soon:** sanitized Ghidra screenshots and update-flow diagrams. MachineID, personal identifiers, private key material and proprietary vendor binaries will not be published.

See the [public evidence policy](evidence/README.md).

## Repository structure

```text
docs/                # Observations, methodology, references and roadmap
├── INSTALACION.md   # Spanish lab setup
├── SETUP.md         # English lab setup
reports/             # RE-001 and subsequent technical findings
scripts/             # Original read-only Python utilities
tests/               # Tests for original scripts
evidence/            # Rules for publishing sanitized images
README.md            # Spanish — primary
README.es.md         # Spanish alias
README.en.md         # English — secondary
SECURITY.md          # Security and responsible disclosure
REVIEW_BEFORE_ANALYSIS.md
```

## Setup and reproducibility

Read [Lab setup (English)](docs/SETUP.md) **before handling a reference sample**. Work only on private offline copies, never on the installed vehicle.

```bash
git clone https://github.com/Ray1172004/arrizo3-research.git
cd arrizo3-research
python -m unittest discover -s tests -v
python scripts/pre_publish_check.py
```

Vendor firmware, executable update packages and proprietary APKs are intentionally not redistributed.

## Known limitations

- The reference package is for **Tiggo 2**, not verified for Arrizo 3.
- Actual Arrizo 3 head-unit OEM, processor, memory and OS remain unknown.
- No Arrizo 3 firmware dump or proven recovery path.
- Exact Windows CE import ordinal mappings require validation.
- Scripts are basic static-analysis aids and cannot replace a security review.
- No flashing, exploitation or vehicle modifications have occurred.

## Roadmap

- [x] Document the vehicle's displayed software version and interfaces
- [x] Classify Windows CE ARMv4T reference binary formats
- [x] Document initial Ghidra finding [RE-001](reports/RE-001-cherylink-cleanup.en.md)
- [x] Create Spanish and English project documentation
- [ ] Validate COREDLL ordinals and investigate update flow (RE-002)
- [ ] Add sanitized evidence and diagrams
- [ ] Identify the exact Arrizo 3 head-unit hardware
- [ ] Locate model-matched firmware and verify a recovery method

## Credits

Built with 💜 on Arch Linux by [@Ray1172004](https://github.com/Ray1172004). [LinkedIn](https://www.linkedin.com/in/matheo-camacho/) · [License for original work](LICENSE) · [Security policy](SECURITY.md).

Third-party names, firmware and software remain the property of their owners. Only original research and utilities are provided here.
