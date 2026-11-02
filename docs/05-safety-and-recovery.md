# Safety and recovery boundary

**No vehicle firmware flashing performed.** The car's ECU, brakes, immobilizer and safety systems are explicitly out of scope.

A backup is not equivalent to proven recoverability: a reliable recovery plan requires identification of the exact head-unit hardware revision, boot chain, storage type, read method, compatible image and independently tested recovery procedure.

Permitted current work: vendor documentation, metadata inspection, local archive extraction, hashing and static analysis with Ghidra. No live fuzzing, exploit payloads or write operations against the installed radio. For any future hardware diagnostics, use a spare bench unit, controlled power and verified signal levels. The Cardputer GPIOs are not 12-V- or direct-CAN-safe.
