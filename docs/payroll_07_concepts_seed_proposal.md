# Propuesta Etapa 3A.1 - Conceptos y tarifas base

Estado: PENDIENTE DE APROBACIÓN. No se insertaron datos.

Después de revisar todas las ocurrencias de tarifas:

- `66` conceptos están marcados `CONFLICTO` y quedan excluidos del seed.
- `6` conceptos tienen una única tarifa detectada.
- Ningún concepto será insertado antes de la aprobación manual del seed.

Reporte completo:

```text
docs/payroll_07_rate_alternatives_report.md
docs/payroll_07_rate_alternatives_report.csv
```

Fuente:

```text
ref/PRODUCCION D&R 2.xlsx
Hoja: May-26
SHA256: 0EB9878074D080515ED70CDACE2BCA3FD757EEACDAE7974F42023FDD05AFEE01
```

Se propone utilizar el primer bloque completo de liquidación, filas 7 a 79.
Este es el único bloque encabezado explícitamente con `Cargo = Chofer`.

Los prefijos visuales `Aux`, `Servicio Chofer` y `Servicio Aux` se eliminan del
nombre visible porque el contexto ya queda identificado mediante `cost_center`
y `role_type`. El orden relativo y las tarifas se conservan.

## D&R - DRIVER

| Orden | Concepto | Tarifa |
|---:|---|---:|
| 1 | Despacho / Retiro | 751.4100 |
| 2 | Entrada < 19:30 | 2506.3674 |
| 3 | Salida > 19:30 | 8772.2858 |
| 4 | Feria Semana 01 | 10025.4695 |
| 5 | Feria Semana 02 | 12531.8369 |
| 6 | Fuera Radio Normal | 3759.5511 |
| 7 | Fuera Radio V Región | 6265.9184 |
| 8 | Sabado Semana 01 | 20050.9390 |
| 9 | Domingo Semana 01 | 25063.6738 |
| 10 | Viajes Por Cliente | 6265.9184 |
| 11 | Sábado > 16:00 | 10025.4695 |
| 12 | Domingo > 16:00 | 11278.6532 |
| 13 | Sabado Semana 02 | 23810.4901 |
| 14 | Domingo Semana 02 | 28823.2249 |
| 15 | Secado Fin de Semana | 550.9788 |
| 16 | Evento | 751.4413 |
| 17 | Punto de Agua | 1492.1098 |
| 18 | Basurero Grande | 1056.7350 |
| 19 | Basurero chico | 263.9250 |
| 20 | Fosa | 1492.4700 |

## D&R - ASSISTANT

| Orden | Concepto | Tarifa |
|---:|---|---:|
| 1 | Despacho / Retiro | 376.3068 |
| 2 | Entrada < 19:30 | 1253.1837 |
| 3 | Salida > 19:30 | 7519.1021 |
| 4 | Feria Semana 01 | 7519.1021 |
| 5 | Feria Semana 02 | 10652.6475 |
| 6 | Fuera Radio Normal | 2819.3702 |
| 7 | Fuera Radio V Región | 5012.7348 |
| 8 | Sabado Semana 01 | 15038.2043 |
| 9 | Domingo Semana 01 | 20050.9390 |
| 10 | Viajes Por Cliente | 5012.7348 |
| 11 | Sábado > 16:00 | 8772.2858 |
| 12 | Domingo > 16:00 | 10025.4695 |
| 13 | Sabado Semana 02 | 18797.7553 |
| 14 | Domingo Semana 02 | 23810.4901 |
| 15 | Secado Fin de Semana | 275.3100 |
| 16 | Evento | 376.7400 |
| 17 | Punto de Agua | 728.6400 |
| 18 | Basurero Grande | 951.1650 |
| 19 | Basurero chico | 238.0500 |
| 20 | Fosa | 1458.3150 |

## SERVICES - DRIVER

| Orden | Concepto | Tarifa |
|---:|---|---:|
| 1 | Aseo | 313.2959 |
| 2 | Secado | 275.7004 |
| 3 | Despacho / Retiro | 751.9102 |
| 4 | Entrada < 07:30 | 2506.3674 |
| 5 | Salida > 19:30 | 8772.2858 |
| 6 | Fuera Radio Normal | 3759.5511 |
| 7 | Fuera Radio V Región | 6265.9184 |
| 8 | Entrega Kit | 313.2959 |
| 9 | Carga Lavamanos | 31.3296 |
| 10 | Sabado | 11905.2450 |
| 11 | Domingo | 15038.2043 |
| 12 | Aseo Fin de Semana | 17.4319 |
| 13 | Secado Fin de Semana | 551.4008 |
| 14 | Sabado > 16:00 | 10025.4695 |
| 15 | Domingo > 16:00 | 11278.6532 |
| 16 | Succión Riles (M3) | 2527.4700 |

## SERVICES - ASSISTANT

| Orden | Concepto | Tarifa |
|---:|---|---:|
| 1 | Aseo | 138.6900 |
| 2 | Secado | 138.6900 |
| 3 | Despacho / Retiro | 376.7400 |
| 4 | Entrada < 07:30 | 1253.3850 |
| 5 | Salida > 19:30 | 7519.2750 |
| 6 | Fuera Radio Normal | 2820.3750 |
| 7 | Fuera Radio V Región | 5012.5050 |
| 8 | Entrega Kit | 138.6900 |
| 9 | Carga Lavamanos | 24.8400 |
| 10 | Sabado | 11905.6050 |
| 11 | Domingo | 15038.5500 |
| 12 | Aseo Fin de Semana | 275.3100 |
| 13 | Secado Fin de Semana | 275.3100 |
| 14 | Sabado > 16:00 | 8772.6600 |
| 15 | Domingo > 16:00 | 10025.0100 |
| 16 | Succión Riles (M3) | 1253.3850 |

## Ambigüedades detectadas

La planilla contiene más de una tarifa para numerosos conceptos dentro del
mismo `cost_center + role_type`. En general aparece una segunda variante cercana
al 75% de la tarifa del primer bloque. El modelo actual permite una sola tarifa
activa por concepto/contexto y no incluye una dimensión para distinguir estas
variantes.

También se observa una anomalía destacable en `SERVICES / DRIVER / Aseo Fin de
Semana`: el primer bloque utiliza `17.4319`, mientras otros bloques utilizan
`413.5506`.

Por esta razón, la propuesta no debe insertarse hasta confirmar que el primer
bloque es la tarifa base oficial para todos los trabajadores de cada contexto.

## Exclusiones

No se incluyen:

- Estado.
- Bonos fuera de producción.
- Vacaciones.
- Total a Pagar.
- Variable Diario.
- Día Trabajado.
- Semana Corrida.
- Producción Total.
- `retrieval_flag`.
- `septic_tank_flag`.

## Script controlado

```text
backend/seed_payroll_concepts.py
```

Por defecto sólo muestra la propuesta. Para aplicar requiere `--apply`, valida
el hash de la fuente y está bloqueado explícitamente para MySQL/Azure.

El manifiesto completo con todos los campos propuestos está disponible en:

```text
docs/payroll_07_concepts_seed_manifest.csv
```
