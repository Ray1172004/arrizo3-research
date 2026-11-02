# QDrive Android app — separate investigation

The phone-side QDrive package identified on the owner's Samsung is `com.neusoft.ssp.intlqdriveassistant`, version `1.1.23`, versionCode `69`, minSdk `14`, targetSdk `26`. The test handset ran Android 16 (API 36).

ADB connection to the owner's laptop succeeded; this proves **phone** ADB authorization, not access to the head unit. Observations included QDrive foreground activity transitions and a legacy QDrive service endpoint that timed out during a test. These observations do not prove an exploitable weakness or establish the cause of QDrive restarting its interface.

The reference archive also includes an Android APK and native ELF helpers. Future work: compare APK versions offline with JADX and map the documented USB/Bluetooth projection mechanism. Avoid requesting reusable ADB authorization from unknown devices.
