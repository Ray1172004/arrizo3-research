# Preparación del laboratorio (español)

**Español** · [English](SETUP.md)

> Investigación en curso: el paquete Tiggo 2 es una muestra de referencia. No introducirlo en la radio original del Arrizo 3 ni ejecutar sus archivos.

## Requisitos

Arch Linux, Git, Python 3, 7-Zip, `file`, `binwalk` y Ghidra. JADX y ADB son opcionales para estudiar QDrive exclusivamente en un teléfono propio de laboratorio.

## Descargar y revisar

```bash
git clone https://github.com/Ray1172004/arrizo3-research.git
cd arrizo3-research
find docs reports scripts tests -type f | sort
python -m unittest discover -s tests -v
python scripts/pre_publish_check.py
```

## Analizar una muestra privada

Conserva los archivos de terceros fuera de GitHub. Ejemplos de inspección **sin ejecutar código**:

```bash
file 'T2 Android 10.rar'
sha256sum 'T2 Android 10.rar'
7z l -pcherydianos 'T2 Android 10.rar'
# Con el ejecutable previamente extraído a un directorio privado:
python scripts/static_triage.py CheryLink_Update.exe --json
python scripts/pe_header_probe.py CheryLink_Update.exe
```

Los resultados deben contextualizarse: un ejecutable para Windows CE del Tiggo 2 no confirma el SO del Arrizo 3.

## Limitaciones

No hay firmware Arrizo 3 verificado, recuperación comprobada ni pruebas de los scripts en todos los sistemas. El `.gitignore` y la revisión automática no sustituyen una inspección manual de archivos y del historial Git antes de publicar. Consulta [Seguridad](../SECURITY.md).
