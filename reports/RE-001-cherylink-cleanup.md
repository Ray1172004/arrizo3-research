# RE-001 — Análisis de limpieza recursiva en CheryLink_Update.exe

[Read this report in English](RE-001-cherylink-cleanup.en.md)

**Tipo:** ingeniería inversa de comportamiento; **no es un hallazgo de vulnerabilidad**.  
**Muestra:** actualización comunitaria de CheryLink para Tiggo 2 (referencia externa).  
**Método:** decompilación estática con Ghidra, PE32 ARMv4T orientado a Windows CE.

## Resumen del hallazgo

La función identificada provisionalmente como `FUN_00011008` recibe una ruta, enumera sus entradas y examina el atributo de directorio mediante el bit `0x10`. Procesa archivos de forma condicional y llama a sí misma para recorrer subdirectorios, excluyendo `.` y `..`.

Contiene dos casos especiales: evita borrar el archivo `EMMC_Check_File.txt` y permite continuar cuando falla la eliminación de `ceusbkwrapperdrv.dll`. Trata de forma diferente el directorio raíz `\\CheryLink`. Una ruta de error estudiada devuelve `0xffffffff`; el flujo de finalización normal devuelve cero. Esto último no demuestra que todas las operaciones de eliminación hayan tenido éxito.

## Evidencias obtenidas

| Indicador | Evidencia del análisis |
| --- | --- |
| Punto de llamada | `entry` alrededor de `0x00011504` llama a `FUN_00011008(0x2e2d0)` |
| Patrón de búsqueda | `*.*` codificado en UTF-16LE, dirección `0x0002e060` |
| Directorio actual | `.` en `0x0002e068` |
| Directorio padre | `..` en `0x0002e06c` |
| Identificación de directorios | Expresión `local_344[0] & 0x10` |
| Excepción de archivo | Comparación con `EMMC_Check_File.txt` |
| Excepción de error | Tratamiento especial de `ceusbkwrapperdrv.dll` |
| Recursividad | Llamada a la propia `FUN_00011008` |
| Carpeta principal | Comparación con `\\CheryLink` antes de intentar eliminar el directorio |

## Reconstrucción conceptual

Este pseudocódigo **no es el código fuente del fabricante**. Solo resume el comportamiento observado:

```text
limpiar_directorio(ruta):
    enumerar entradas de ruta
    para cada entrada:
        si es archivo:
            omitir EMMC_Check_File.txt
            intentar eliminar el archivo
            si falla y no es ceusbkwrapperdrv.dll:
                devolver error
        si es directorio y no es "." ni "..":
            llamar limpiar_directorio(ruta_hija)
            si falla:
                devolver error
    si ruta es diferente de "\CheryLink":
        intentar eliminar el directorio
    devolver finalización normal
```

## Nivel de confianza y limitaciones

- **Alto:** estructura recursiva, comparaciones de cadenas, condiciones y rutas de control visibles en Ghidra.
- **Medio:** correspondencia exacta entre ordinales importados y nombres de funciones de Windows CE; pendiente de contrastar con la tabla de exportaciones de la versión adecuada de `COREDLL.dll`.
- **No determinado:** arquitectura y sistema operativo de la pantalla original del Arrizo 3.

**No se ha ejecutado este actualizador sobre el automóvil, no se ha extraído firmware del Arrizo 3 y no se afirma la existencia de una vulnerabilidad.**
