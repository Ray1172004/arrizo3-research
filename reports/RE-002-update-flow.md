# RE-002 — Copia y preparación de extracción en CheryLink_Update.exe

[English](RE-002-update-flow.en.md)

Muestra: `CheryLink_Update.exe`, incluida en una actualización comunitaria de CheryLink para **Tiggo 2**. Análisis estático con Ghidra sobre un ejecutable PE32 ARMv4T para Windows CE. Este informe **no** describe el firmware original del Arrizo 3.

## Secuencia observada

El punto de entrada (`entry`) registra `begin remove file` y llama a `FUN_00011008`, documentada en [RE-001](RE-001-cherylink-cleanup.md). Si esa función devuelve cero, continúa el proceso:

1. Construye una ruta de origen terminada en `\\CheryLink.7z` mediante `Ordinal_56`.
2. Abre el origen con `Ordinal_1145` (compatible con `_wfopen`).
3. Abre `CHERYLINK//CheryLink.7z` como destino con `Ordinal_1113` (compatible con `fopen`).
4. Utiliza `Ordinal_1130`, `Ordinal_1131` y `Ordinal_1130` para ir al final, consultar la posición y regresar al inicio del origen (`fseek`, `ftell`, `fseek`).
5. Lee bloques de hasta `0x400` bytes (1024) con `Ordinal_1120` (`fread`) y los escribe con `Ordinal_1121` (`fwrite`).
6. Compara el total contabilizado como escrito (`local_8a0`) con la posición final del origen (`local_8b4`). Cuando coinciden, registra `copy data success` y cierra ambos flujos mediante `Ordinal_1118` (`fclose`).
7. Llama a `FUN_000141c0(0x2e51c, 0x2e510)`. Si su resultado es cero, registra `ExtractFile OK` e intenta eliminar el archivo temporal `CHERYLINK//CheryLink.7z` con `Ordinal_165` (compatible con `DeleteFileW`). Si devuelve otro valor, registra `ExtractFile fail`.

Las correspondencias por ordinal se apoyan en tablas comunitarias de COREDLL para Windows Mobile 6.0 y en las firmas de la biblioteca C documentadas por Microsoft. No se dispone de la tabla de exportación exacta usada al compilar esta muestra.

## Bucle de lectura y escritura

El siguiente fragmento fue copiado de la decompilación compartida por el investigador; los nombres permanecen tal como los genera Ghidra.

```c
local_898 = Ordinal_1120(auStack_684, 1, 0x400, local_8ac);
if ((local_898 == 0) || (local_898 == -1)) goto LAB_00011844;

local_8a4 = auStack_684;
while (true) {
    local_8b0 = Ordinal_1121(local_8a4, 1, local_898, local_8a8);
    if ((local_8b0 == 0) || (local_8b0 == -1)) goto LAB_00011830;
    if (local_8b0 == local_898) break;
    if (0 < local_8b0) {
        local_8a4 = local_8a4 + local_8b0;
        local_898 = local_898 - local_8b0;
    }
    local_8a0 = local_8a0 + local_8b0;
}
local_8a0 = local_8a0 + local_8b0;
```

Ante una escritura parcial positiva, mueve el puntero del búfer, reduce la cantidad pendiente y vuelve a escribir. La comprobación final compara **cantidad** de bytes, no el contenido mediante un hash. No se puede descartar una validación adicional dentro de la función de extracción sin analizarla.

## Tratamiento de errores

El código registra condiciones de fallo distintas para apertura del origen, apertura del destino, copia y extracción.

Se observó una diferencia relevante: en la rama donde ambos archivos se abren correctamente, `entry` asigna `local_74 = 0` al finalizar incluso si se registró `copy data fail` o `ExtractFile fail`. Esto puede dificultar que un programa externo distinga los fallos si solo consulta el valor de retorno. No se ha demostrado que exista un proceso que dependa de ese valor ni que sea una vulnerabilidad explotable.

Las cadenas de modo de apertura están referenciadas mediante `DAT_0002e388` y `DAT_0002e408`; no se han inspeccionado aún. El comportamiento interno de `FUN_000141c0` sigue pendiente de analizarse.

## Referencias

- [RE-001 — Limpieza recursiva](RE-001-cherylink-cleanup.md).
- [fopen / _wfopen (Windows CE), Microsoft](https://learn.microsoft.com/en-us/previous-versions/windows/embedded/ms859631%28v%3Dmsdn.10%29).
- [fwrite (Windows CE), Microsoft](https://learn.microsoft.com/en-us/previous-versions/windows/embedded/ms859645%28v%3Dmsdn.10%29).
- [ftell (Windows CE), Microsoft](https://learn.microsoft.com/en-us/previous-versions/windows/embedded/ms859644%28v%3Dmsdn.10%29).
- [COREDLL Windows Mobile 6.0, tabla comunitaria](https://www.cnblogs.com/huanglong/archive/2012/03/13/2393275.html).
