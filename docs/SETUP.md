# Lab setup (English)

[Español](INSTALACION.md) · **English**

> Ongoing research: the Tiggo 2 update is a reference sample. Never install it on the original Arrizo 3 radio or execute its binaries.

## Requirements

Arch Linux, Git, Python 3, 7-Zip, `file`, `binwalk` and Ghidra. JADX and ADB are optional for analyzing QDrive on an owned lab phone only.

## Clone and inspect

```bash
git clone https://github.com/Ray1172004/arrizo3-research.git
cd arrizo3-research
find docs reports scripts tests -type f | sort
python -m unittest discover -s tests -v
python scripts/pre_publish_check.py
```

## Examine a privately stored sample

Do not commit or redistribute vendor files. Read-only inspection examples:

```bash
file 'T2 Android 10.rar'
sha256sum 'T2 Android 10.rar'
7z l -pcherydianos 'T2 Android 10.rar'
# If the updater was extracted privately:
python scripts/static_triage.py CheryLink_Update.exe --json
python scripts/pe_header_probe.py CheryLink_Update.exe
```

Windows CE binaries in a Tiggo 2 sample do not establish the operating system of the Arrizo 3 head unit.

## Limitations

No verified Arrizo 3 firmware or tested recovery mechanism. Scripts have not been validated on every platform. Ignore rules and automated checks cannot substitute for a manual review of files and Git history. See [Security](../SECURITY.md).
