# RE-003 — Identificación del extractor 7z integrado en CheryLink

[English](RE-003-7z-extractor.en.md)

**Muestra:** `CheryLink_Update.exe`, procedente de una actualización de referencia para Tiggo 2. **Entorno:** Ghidra, PE32 ARMv4T para Windows CE.

## Identificación del decodificador

Al seguir la llamada `entry → FUN_000141c0 → FUN_000135c8`, se encontró una rutina que abre un archivo 7z, enumera sus entradas, descomprime su contenido y escribe archivos y carpetas en disco.

El flujo coincide de forma muy específica con **`7zMain.c`, aplicación de ejemplo del decodificador 7z incluido en el SDK LZMA de Igor Pavlov**. Entre las coincidencias aparecen el orden de inicialización, la llamada de extracción con diez argumentos, el recorrido de nombres UTF-16, la creación de carpetas, los mensajes de error y el texto final `Everything is Ok`.

El parecido permite identificar con **confianza alta la familia de código** y formular correspondencias funcionales entre las rutinas descompiladas y el SDK. No se ha hecho una comparación binaria, ni se conoce la revisión exacta que empleó el fabricante.

## Correspondencias funcionales

| Ghidra | Rutina equivalente en el ejemplo LZMA SDK | Evidencia |
| --- | --- | --- |
| `FUN_00014eb4` | `SzArEx_Open` | Abre la estructura del archivo antes de iterar sus entradas |
| `FUN_00014d70` | `SzArEx_GetFileNameUtf16` | Primero solicita longitud, luego recupera el nombre |
| `FUN_00019978` | `SzArEx_Extract` | Coinciden cantidad, posición y uso de argumentos |
| `FUN_00013ef0` | `MyCreateDir` | Crea directorios al recorrer los nombres |
| `FUN_00013f4c` | `OutFile_OpenUtf16` | Abre archivos de salida |
| `FUN_0001a100` | `File_Write` | Escribe los bytes descomprimidos |
| `FUN_00019f6c` | `File_Close` | Cierra el archivo tras escribir |
| `FUN_000149f4` | `SzArEx_Init` | Inicializa el estado del archivo |
| `FUN_00014a68` | `SzArEx_Free` | Libera las estructuras de archivo |

Los nombres de la segunda columna son *correspondencias reconstruidas*, no símbolos recuperados del ejecutable.

## Flujo observado

```text
entry()
  └── FUN_000141c0()
        └── FUN_000135c8()
              ├── abre CheryLink.7z
              ├── inicializa la biblioteca de extracción
              ├── abre la estructura del archivo 7z
              ├── recorre cada entrada del archivo
              │     ├── obtiene el nombre UTF-16
              │     ├── descomprime entradas que contienen archivos
              │     ├── prepara rutas y crea carpetas
              │     └── abre, escribe y cierra los archivos
              ├── libera la memoria y cierra el archivo
              └── devuelve 0 si todo finalizó correctamente, 1 ante error
```

Las cadenas `can not open input file`, `can not open output file`, `can not write output file`, `can not close output file` y `Everything is Ok` refuerzan la identificación: también aparecen en el ejemplo público `7zMain.c`.

## Fragmentos relevantes

La llamada que probablemente descomprime cada entrada:

```c
local_4950 = FUN_00019978(
    aiStack_494c, auStack_46f0, local_49c,
    local_498 + 1, local_498,
    (uint *)(local_498 + 2),
    &local_480, (int *)&local_484,
    &local_6c0, &local_6c8
);
```

La llamada que escribe el contenido extraído:

```c
local_18 = FUN_0001a100(
    &iStack_47c, local_498[0] + local_480, &local_60
);
```

El código también contempla la creación de subdirectorios a partir de los separadores `/` de los nombres almacenados en el archivo. En esta revisión no se ha comprobado cómo maneja nombres maliciosos o rutas fuera del directorio de destino: **no se afirma una vulnerabilidad de extracción**.

## Relación con el vehículo

El comportamiento descrito pertenece a un actualizador obtenido como referencia para **Tiggo 2**. No demuestra qué procesador, sistema operativo o firmware utiliza la unidad original del **Arrizo 3**. El vehículo no ha sido modificado.

## Referencia de comparación

- [LZMA SDK — `7zMain.c`, versión histórica publicada en Android Open Source Project](https://android.googlesource.com/platform/external/lzma/+/kitkat-dev/C/Util/7z/7zMain.c).
- [LZMA SDK — sitio del proyecto 7-Zip](https://sevenzip.sourceforge.io/sdk.html).
- [RE-002 — Copia del archivo y llamada al extractor](RE-002-update-flow.md).
