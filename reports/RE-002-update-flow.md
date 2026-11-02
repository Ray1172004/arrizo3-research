# RE-002 — Flujo inicial de CheryLink_Update.exe

**Muestra:** `CheryLink_Update.exe` del paquete CheryLink distribuido para Tiggo 2.  
**Método:** análisis estático en Ghidra (PE32, Windows CE / ARMv4T).  
**Estado:** análisis parcial.

## Entrada del actualizador

En `entry`, después del mensaje de registro `begin remove file`, se observa una llamada a `FUN_00011008(0x2e2d0)` (alrededor de `0x00011504`). El argumento corresponde a la cadena Unicode `\CheryLink`.

El valor de retorno se compara con cero. La ruta del resultado cero está asociada al registro `remove file OK` y continúa con otras operaciones.

```text
entry()
  ├─ registro: begin remove file
  ├─ FUN_00011008("\CheryLink")   [RE-001]
  └─ comprobar valor devuelto
       ├─ igual a cero → registro remove file OK; continúa
       └─ distinto de cero → otra rama pendiente de examinar
```

La función de limpieza `FUN_00011008` ya se documentó en [RE-001](RE-001-cherylink-cleanup.md). El registro de éxito no garantiza que todas las operaciones internas de borrado se hayan completado sin incidencia.

## Otras cadenas identificadas

En la muestra se encontraron `begin copy data`, `copy data success`, `ExtractFile OK`, `ExtractFile fail`, `UPDATE END` y la ruta `CHERYLINK//CheryLink.7z`.

Estas cadenas **sugieren** una fase de transferencia o extracción del archivo, pero por sí solas no establecen el orden, los controles de integridad, los destinos ni las condiciones de error. Para confirmar el comportamiento debemos seguir sus referencias cruzadas y revisar las funciones invocadas.

## Apertura del archivo y lectura en bloques

Un fragmento adicional de `entry`, obtenido directamente del Decompiler de Ghidra, permite identificar la preparación del flujo de lectura:

```c
Ordinal_56(&local_ac0, L"%s\\CheryLink.7z", &local_894);
local_8ac = Ordinal_1145(&local_ac0, &DAT_0002e388);
if (local_8ac == 0) { /* open fromfile fail */ }
else {
    local_8a8 = Ordinal_1113("CHERYLINK//CheryLink.7z", &DAT_0002e408);
    if (local_8a8 == 0) { /* open tofile fail */ }
    else {
        Ordinal_1130(local_8ac, 0, 2);
        local_8b4 = Ordinal_1131(local_8ac);
        Ordinal_1130(local_8ac, 0, 0);
        do {
            local_898 = Ordinal_1120(auStack_684, 1, 0x400, local_8ac);
            if ((local_898 == 0) || (local_898 == -1)) goto LAB_00011844;
            /* continuación aún no examinada */
        } while (/* condición pendiente */);
    }
}
```

La tabla comunitaria de exportaciones de COREDLL de Windows Mobile 6.0 relaciona los ordinales `56`, `1145`, `1113`, `1130`, `1131` y `1120` con `wsprintfW`, `_wfopen`, `fopen`, `fseek`, `ftell` y `fread` respectivamente. La API `fwrite` figura como ordinal `1121`, pero **todavía no se ha localizado su llamada en el código compartido**. La documentación de Microsoft confirma las firmas funcionales; las correspondencias ordinales concretas deben verificarse para la biblioteca usada por esta muestra.

**Interpretación:** primero se prepara una ruta con el nombre `CheryLink.7z`, se intenta abrir el origen y después el destino. El programa lleva el puntero de lectura al final, consulta su posición (presumiblemente para conocer el tamaño), vuelve al inicio y solicita hasta `0x400` (1024) bytes por iteración con una llamada compatible con `fread`.

Los modos de apertura se reciben desde `DAT_0002e388` y `DAT_0002e408`, cuyo contenido aún no se ha inspeccionado. Todavía **no está confirmado el código que escribe los bloques, la validación del tamaño final ni el procedimiento de extracción**. Por ello, este documento describe la *preparación y lectura del archivo*, no una copia íntegra verificada.

## Referencias técnicas

- [RE-001 — Limpieza recursiva](RE-001-cherylink-cleanup.md).
- [Microsoft — FindFirstFile en Windows CE](https://learn.microsoft.com/en-us/previous-versions/windows/embedded/ms923968%28v%3Dmsdn.10%29).
- [Microsoft — FindNextFile en Windows CE](https://learn.microsoft.com/en-us/previous-versions/windows/embedded/ms923971%28v%3Dmsdn.10%29).
- [Microsoft — FindClose en Windows CE](https://learn.microsoft.com/en-us/previous-versions/ms960590%28v%3Dmsdn.10%29).

- [Microsoft — fopen / _wfopen (Windows CE)](https://learn.microsoft.com/en-us/previous-versions/windows/embedded/ms859631%28v%3Dmsdn.10%29).
- [Microsoft — fseek (Windows CE)](https://learn.microsoft.com/en-us/previous-versions/windows/embedded/ms859641%28v%3Dmsdn.10%29).
- [Microsoft — ftell (Windows CE)](https://learn.microsoft.com/en-us/previous-versions/windows/embedded/ms859644%28v%3Dmsdn.10%29).
- [Listado comunitario de exportaciones COREDLL (Windows Mobile 6.0)](https://www.cnblogs.com/huanglong/archive/2012/03/13/2393275.html) — útil como referencia, no confirmado para este dispositivo.

La radio original del Arrizo 3 no ha sido identificada como Windows CE. Este informe analiza una **muestra de referencia para Tiggo 2**, no firmware extraído del vehículo.
