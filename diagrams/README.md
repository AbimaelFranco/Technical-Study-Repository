# Diagramas

| Tipo | Archivos | Cómo verlos |
|---|---|---|
| **Mermaid** | [`*.mmd`](.) y bloques ` ```mermaid ` en `docs/*.md` | GitHub los renderiza; alternativa: https://mermaid.live o extensión de VS Code |
| **Mapas mentales** | [`mindmaps.md`](mindmaps.md) | GitHub |
| **Comparativas** | [`comparativas.md`](comparativas.md) | GitHub (usa `quadrantChart` y `xychart-beta`, que requieren un Mermaid reciente) |
| **Interactivos (archify)** | [`archify/*.html`](archify) | Abrir el `.html` en el navegador (GitHub no los ejecuta) |

## Diagramas archify

| HTML | Especificación (JSON) | Tipo |
|---|---|---|
| [architecture_case.html](archify/architecture_case.html) | [architecture_case.json](archify/architecture_case.json) | Arquitectura |
| [dataflow_sensor_to_dashboard.html](archify/dataflow_sensor_to_dashboard.html) | [dataflow_sensor_to_dashboard.json](archify/dataflow_sensor_to_dashboard.json) | Flujo de datos |
| [lifecycle_firmware.html](archify/lifecycle_firmware.html) | [lifecycle_firmware.json](archify/lifecycle_firmware.json) | Ciclo de vida / máquina de estados |
| [sequence_offline_recovery.html](archify/sequence_offline_recovery.html) | [sequence_offline_recovery.json](archify/sequence_offline_recovery.json) | Secuencia |

**Uso del visor:** tema claro/oscuro, zoom/paneo, búsqueda, trazado de relaciones, vistas guiadas (en la arquitectura) y exportación (PNG/SVG…).

**Regenerar** (requiere el skill *archify* y Node ≥ 18):
```bash
node <ruta-al-skill>/bin/archify.mjs validate architecture diagrams/archify/architecture_case.json --quality showcase
node <ruta-al-skill>/bin/archify.mjs deliver  architecture diagrams/archify/architecture_case.json diagrams/archify/architecture_case.html --quality showcase
```
(Sustituye `architecture` por `dataflow`, `lifecycle` o `sequence` según el archivo.)

## Nota sobre circuitos
Mermaid/archify no representan circuitos eléctricos con precisión. Para circuitos se usan **diagramas ASCII conceptuales** y **tablas de conexiones** (ver `docs/02` y `docs/10`). Son **didácticos**: verifica pines, límites y protecciones con los datasheets antes de construir.
