# Tiggo 2 CheryLink update — independent reference package

Source: [CheryTeamEcuador community article](https://cheryteamecuador.wixsite.com/team/post/actualizaci%C3%B3n-de-la-radio-carro). This is an offline sample advertised for the **Tiggo 2**, not a verified update for the Arrizo 3. References to Android 10 in the article concern phone compatibility; they do not establish the operating system of the head unit.

## Container

| Artifact | Observation |
| --- | --- |
| `T2 Android 10.rar` | RAR5, 10,705,537 bytes |
| SHA-256 | `407169979b4d8f8a7123dac36ec8be821b20528ec73de3099c49dbb10a571d3c` |
| `CheryLink.7z` | 10,112,887 bytes; 1,515 files, 20 folders |
| `CheryLink_Update.exe` | PE32 for Windows CE 6.00, ARMv4T |
| `signature.dat` | 524,288 bytes; function unverified |
| `7寸屏Android10.0升级包.txt` | Small note referring to 7-inch screen / Android 10 |

## Identified executable formats

- `SSPLink.exe`: PE32 ARMv4T, Windows version header 5.00.
- `SSPMain.exe`: PE32 ARMv4T, Windows version header 5.00.
- `applink/upgrade.exe`: PE32 Windows CE 6.00 ARMv4T.
- `cherylink_upg/Temp/QDintlqdrive.apk`: Android APK.
- `cherylink_upg/Temp/app_hclink/ooomserver27`: ELF32 ARM Android 26.

Strings in the updater include `Desay_SDK_TI_DM37x (ARMV4I)` and `COREDLL.dll`. This supports a Windows CE development context but does **not** prove an Arrizo 3 CPU or OS. Names `rsa_public_key.pem`, `ADBKEY` and `ADBKEY.PUB` appear in the archive; no key material is distributed here.

Static analysis only. Never execute or flash the sample on the vehicle.
