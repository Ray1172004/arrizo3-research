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

## Referencias técnicas

- [RE-001 — Limpieza recursiva](RE-001-cherylink-cleanup.md).
- [Microsoft — FindFirstFile en Windows CE](https://learn.microsoft.com/en-us/previous-versions/windows/embedded/ms923968%28v%3Dmsdn.10%29).
- [Microsoft — FindNextFile en Windows CE](https://learn.microsoft.com/en-us/previous-versions/windows/embedded/ms923971%28v%3Dmsdn.10%29).
- [Microsoft — FindClose en Windows CE](https://learn.microsoft.com/en-us/previous-versions/ms960590%28v%3Dmsdn.10%29).

La radio original del Arrizo 3 no ha sido identificada como Windows CE. Este informe analiza una **muestra de referencia para Tiggo 2**, no firmware extraído del vehículo.
