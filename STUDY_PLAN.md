# Plan de estudio

> **Prioridad según la plaza.** Lo que explícitamente pide la vacante pesa más: **C/C++ y Python (avanzado)** → **UART/I2C/1-Wire/CAN** → **Linux** → **esquemáticos y 3D** → **OT/IT/telemetría** (es el propósito del puesto) → **inglés intermedio**. Tu punto fuerte es Python/datos/sensores I2C; tu punto a reforzar es **C embebido, CAN y el marco OT**. Ver honestidad de perfil en el [`README`](README.md#perfil-del-estudiante-y-honestidad-técnica).

## Matriz de priorización

| Requisito de la plaza | Prioridad | Tu nivel actual (según perfil) | Módulos | Ejercicios / práctica |
|---|---|---|---|---|
| C/C++ avanzado | ⭐⭐⭐ (reforzar) | Medio (más fuerte en Python) | [03](docs/03_c_cpp.md), [06](docs/06_sistemas_embebidos.md) | [`examples/c`](examples/c), [`programming.md`](exercises/programming.md) |
| Python avanzado | ⭐⭐⭐ (mantener) | Alto | [04](docs/04_python.md), [11](docs/11_conectividad_y_telemetria.md) | [`examples/python`](examples/python) |
| UART, I2C, 1-Wire, CAN | ⭐⭐⭐ | I2C: práctico; resto: conceptual | [02](docs/02_protocolos_comunicacion.md) | [`protocols.md`](exercises/protocols.md) |
| Linux | ⭐⭐⭐ | Medio (Raspberry Pi/PostgreSQL) | [08](docs/08_linux.md) | [`linux.md`](exercises/linux.md), [`examples/linux`](examples/linux) |
| Esquemáticos + 3D | ⭐⭐ | 3D: práctico (Ender 3) | [10](docs/10_esquematicos_y_diseno_3d.md) | [`fundamentals.md`](exercises/fundamentals.md) F-A3 |
| Convergencia OT/IT | ⭐⭐⭐ (propósito del puesto) | Conceptual | [07](docs/07_redes_ot_it.md), [11](docs/11_conectividad_y_telemetria.md), [15](docs/15_caso_realista_arquitectura.md) | [`ot_it.md`](exercises/ot_it.md) |
| Diagnóstico | ⭐⭐⭐ | Medio | [12](docs/12_diagnostico_y_troubleshooting.md) | Casos [14](docs/14_casos_practicos.md) |
| Git | ⭐⭐ | Medio | [09](docs/09_git_y_control_versiones.md) | `programming.md` §C |
| Inglés intermedio | ⭐⭐ | Por confirmar | [13](docs/13_ingles_tecnico.md) | Práctica oral |

---

## Ruta A — 2 horas (repaso de emergencia)

**Objetivo:** cubrir lo más preguntado y no llegar en blanco.

| Min | Actividad | Material |
|---|---|---|
| 0–10 | Lee el **resumen ejecutivo** de los módulos 02, 03, 07, 12 | `docs/` |
| 10–35 | **Protocolos**: tabla comparativa, fórmulas de pull-up I2C, terminación CAN, DS18B20 (85/−127); mapa mental | [`QUICK_REFERENCE §1-2`](QUICK_REFERENCE.md), [`mindmaps.md`](diagrams/mindmaps.md) |
| 35–60 | **C/C++**: bits/máscaras, `volatile`, punteros, buffer circular; **compila y ejecuta** `05_bit_manipulation.c` y `02_circular_buffer.c` | [`examples/c`](examples/c) |
| 60–75 | **Python** práctico: ejecuta `01`, `08`, `09`; repasa `requests` + timeout + reintentos | [`examples/python`](examples/python) |
| 75–90 | **Linux**: comandos + `systemctl/journalctl` + permisos del puerto serial | [`QUICK_REFERENCE §4`](QUICK_REFERENCE.md) |
| 90–105 | **OT/IT y caso realista**: mira `architecture_case.html` y explica el flujo en voz alta | [`diagrams/archify/`](diagrams/archify) |
| 105–120 | **Simulacro parcial:** secciones 1 y 3 del examen; revisa checklist final | [`mock_exam/`](mock_exam/exam_60min.md), [`QUICK_REFERENCE §9`](QUICK_REFERENCE.md) |

---

## Ruta B — 1 día (≈ 7–8 h)

| Bloque | Duración | Contenido | Entregable |
|---|---|---|---|
| **1. Mañana: fundamentos y protocolos** | 2 h | Módulos 01 y 02 completos (con diagramas); ejercicios `fundamentals.md` básico/intermedio y `protocols.md` básico/intermedio | 10 respuestas correctas sin mirar |
| **2. Programación C** | 1.5 h | Módulo 03; ejecuta los 9 ejemplos C; resuelve `PG-B*` y `PG-I*` en papel | Explicar `volatile`, bits y buffer circular |
| **3. Python + telemetría** | 1 h | Módulo 04 y 11; ejecuta `06` con `mock_api_server.py --fail-first 2` y `08` | Explicar idempotencia y store & forward |
| **4. Almuerzo/descanso** | 0.5 h | | |
| **5. Linux + OT/IT** | 1.5 h | Módulos 08 y 07; `linux.md` básico/intermedio; `ot_it.md` básico | Comandos de memoria |
| **6. Diagnóstico y casos** | 1 h | Módulo 12 (escenarios 3, 4, 5, 10) y Caso D | Método de diagnóstico en voz alta |
| **7. Simulacro completo** | 1 h | [`exam_60min.md`](mock_exam/exam_60min.md) cronometrado | Puntaje y lista de fallas |
| **8. Repaso de fallas** | 0.5 h | Solo temas en que fallaste | |

Al final del día: repasa `QUICK_REFERENCE.md` y duerme.

---

## Ruta C — 1 semana

| Día | Tema | Actividades | Comprobación |
|---|---|---|---|
| **Lun** | Electrónica + sensores | Módulos 01, 05; `fundamentals.md` (todos los niveles) | Calcula ADC, divisores, NTC, RC sin ayuda |
| **Mar** | Protocolos | Módulo 02; `protocols.md`; decodifica J1939 con `can_j1939_decode.py`; dibuja buses en papel | Explica arbitraje CAN y pull-ups I2C |
| **Mié** | C/C++ + embebidos | Módulos 03 y 06; escribe **desde cero** un parser, un buffer circular y una FSM; compila con `-Wall -Wextra` y `-fsanitize` | Código sin warnings; explica cada línea |
| **Jue** | Python + telemetría | Módulos 04 y 11; construye un mini-gateway: serial simulado → validación → SQLite → API mock | Pérdida de red simulada sin perder datos |
| **Vie** | Linux + Git + 3D/esquemáticos | Módulos 08, 09, 10; `linux.md`; monta una VM y un servicio systemd; lee un esquemático de un módulo real | Diagnostica un servicio roto a propósito |
| **Sáb** | OT/IT + casos + inglés | Módulos 07, 12, 13, 14, 15; `ot_it.md`; **explica los casos A–D y el caso realista en voz alta, en español e inglés** | Grabarte y revisar |
| **Dom** | Simulacro + repaso | `exam_60min.md` cronometrado → corrige con `solutions.md` → repasa fallas; checklist | ≥ 70 puntos |

**Práctica de hardware (si tienes):** Raspberry Pi + DS18B20 + I2C; adaptador USB-serie con loopback; imprime una prueba de tolerancias y una carcasa en PETG/ASA.

---

## Técnica de repaso activo
1. **Explica en voz alta** (30–60 s) como en una entrevista; grábate.
2. **Pregunta → responde → verifica** con [`question_bank.md`](exercises/question_bank.md).
3. **Escribe código a mano/sin autocompletar** los patrones: bits, buffer, parser, FSM, request con reintentos.
4. **Un error, una nota:** lleva una lista de errores frecuentes personales.
5. **Espaciado:** repite las fallas a 1, 3 y 7 días.

## Si te quedan pocos minutos antes de la prueba
Solo [`QUICK_REFERENCE.md`](QUICK_REFERENCE.md) §1, §2, §6, §8 y §9.
