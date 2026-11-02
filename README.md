# Investigación de la unidad multimedia del Chery Arrizo 3

[![Estado](https://img.shields.io/badge/estado-en_investigación-blue)](docs/06-roadmap.md) ![Método](https://img.shields.io/badge/método-análisis_estático-green) ![Vehículo](https://img.shields.io/badge/vehículo-sin_modificar-green)

**Idioma principal: español · [Read in English](README.en.md)**

**Ciberseguridad automotriz · Ingeniería inversa de firmware · Windows CE / ARM · Ghidra · Proyección Android**

> **Aviso de alcance:** el vehículo que motiva la investigación es un **Chery Arrizo 3 de 2021** con pantalla original. El paquete de actualización examinado hasta ahora corresponde a un **Tiggo 2** y se utiliza solo como muestra de referencia. No se ha demostrado que ambas pantallas compartan hardware, firmware ni sistema operativo.

## ¿Qué quiero investigar?

Comprender la arquitectura de la unidad multimedia original, identificar cómo funcionan sus mecanismos de actualización y estudiar posibles métodos **de solo lectura** para obtener el firmware correspondiente a su hardware. El propósito es aprender ingeniería inversa de sistemas embebidos sin comprometer el vehículo.

**Estado:** investigación en desarrollo. No se ha extraído el firmware original del Arrizo 3, no se ha modificado su memoria y **no se ha descubierto ni explotado una vulnerabilidad**.

## Resultados observados

| Área | Resultado | Alcance |
| --- | --- | --- |
| Versión visible en Arrizo 3 | `ARRIZO 3_02_31.01_170919_R` | Fotografiada en la pantalla original |
| Interfaces | USB-A, Bluetooth, Cloudrive, Radio, Media, CarInfo | Observación del vehículo |
| Paquete de referencia | `T2 Android 10.rar` (RAR5) | Distribuido para Tiggo 2, **no compatible confirmado con Arrizo 3** |
| Archivo `CheryLink.7z` | 1.515 archivos y 20 directorios | Listado local con 7-Zip |
| Actualizador | `CheryLink_Update.exe` es PE32 Windows CE 6.00 ARMv4T | **Solo** binario de referencia |
| Otros componentes | PE32 ARMv4T, APK y ELF ARM para Android | Paquete de referencia |
| Función de Ghidra | `FUN_00011008`: recorrido recursivo y eliminación condicional | [Hallazgo RE-001](reports/RE-001-cherylink-cleanup.md) |
| SO, SoC y memoria de la radio Arrizo 3 | Desconocidos | Falta identificar el hardware |

## Hallazgo RE-001: limpieza recursiva de CheryLink

Al analizar estáticamente `CheryLink_Update.exe` con **Ghidra**, se estudió `FUN_00011008`, una rutina que recorre directorios, distingue carpetas y archivos, utiliza llamadas de Windows CE importadas por ordinal y procesa condiciones especiales para `EMMC_Check_File.txt` y `ceusbkwrapperdrv.dll`. También excluye las entradas `.` y `..` y trata de manera diferenciada la carpeta principal `\\CheryLink`.

El hallazgo describe **cómo trabaja un actualizador**, no una vulnerabilidad de seguridad ni una ejecución confirmada en nuestro automóvil. Las correspondencias exactas de algunos ordinales todavía requieren validación con la versión correspondiente de `COREDLL.dll`.

Más información: [Informe RE-001](reports/RE-001-cherylink-cleanup.md) · [Guía de Ghidra](docs/03-ghidra-wince.md).

## Estructura del proyecto

- [Observaciones del vehículo](docs/01-oem-observations.md)
- [Análisis del paquete de referencia](docs/02-reference-package.md)
- [Metodología Ghidra / Windows CE](docs/03-ghidra-wince.md)
- [Investigación de QDrive en Android](docs/04-qdrive-android.md)
- [Seguridad y recuperación](docs/05-safety-and-recovery.md)
- [Próximos pasos](docs/06-roadmap.md)
- [Referencias](docs/references.md)
- [Política de divulgación](SECURITY.md)
- [Código de análisis](scripts/) y [pruebas](tests/)

**Nota sobre idiomas:** el README principal está en español; [README.en.md](README.en.md) ofrece la descripción en inglés. La documentación técnica detallada conserva por ahora títulos y contenido en inglés y puede traducirse progresivamente.

## Reproducir el análisis de forma local

Descarga por tus propios medios una muestra legítima en una carpeta **privada**, sin copiarla al USB del automóvil ni ejecutar el actualizador.

```bash
file 'T2 Android 10.rar'
sha256sum 'T2 Android 10.rar'
7z l -pcherydianos 'T2 Android 10.rar'
# Desde la carpeta local donde extrajiste el paquete:
7z l CheryLink.7z
python scripts/static_triage.py CheryLink_Update.exe --json
python scripts/pe_header_probe.py CheryLink_Update.exe
python -m unittest discover -s tests -v
python scripts/pre_publish_check.py
```

Los scripts propios inspeccionan metadatos y cabeceras de archivos locales; **no ejecutan firmware de terceros**.

## Seguridad y ética

No se ha realizado flasheo, explotación de la pantalla instalada, inyección CAN ni modificación de la ECU u otros sistemas de conducción. La muestra de referencia contiene nombres de posibles claves ADB; por ese motivo, aquí **no se publican binarios propietarios, claves, VIN, MachineID ni registros privados**. Tener una copia de firmware tampoco implica contar con un método de recuperación demostrado.

## Siguientes hitos

1. Validar correspondencias de funciones importadas mediante ordinales de Windows CE.
2. Analizar la secuencia de copia y extracción del actualizador (**RE-002**).
3. Identificar fabricante y referencia de hardware de la unidad Arrizo 3.
4. Buscar firmware específico compatible y un procedimiento de recuperación probado antes de plantear modificaciones.

## Fuentes principales

- [CheryTeamEcuador — Actualización de la radio](https://cheryteamecuador.wixsite.com/team/post/actualizaci%C3%B3n-de-la-radio-carro) (paquete comunitario para Tiggo 2).
- [Ghidra — NSA](https://github.com/NationalSecurityAgency/ghidra).
- [Android Debug Bridge — Android Developers](https://developer.android.com/tools/adb).

**Investigador:** [Ray1172004](https://github.com/Ray1172004) · **Licencia:** MIT para el código y contenido originales de este repositorio.
