# Ejercicios · Redes OT/IT, conectividad y telemetría

> Soluciones en [`answer_key.md`](answer_key.md) (sección **OT/IT**). Teoría: [`docs/07`](../docs/07_redes_ot_it.md), [`docs/11`](../docs/11_conectividad_y_telemetria.md), [`docs/14`](../docs/14_casos_practicos.md), [`docs/15`](../docs/15_caso_realista_arquitectura.md).

## Nivel básico
**OT-B1 (C).** Define OT e IT y da 3 diferencias clave (prioridades, ciclo de vida, actualizaciones).
**OT-B2 (C).** ¿Diferencia entre monitoreo y control? ¿Por qué el alcance del proyecto es monitoreo?
**OT-B3 (MC).** ¿Cuál protocolo es publicar/suscribir con broker?
a) HTTP b) MQTT c) UDP d) SSH
**OT-B4 (C).** ¿Qué es un gateway y por qué se usa entre la máquina y el servidor?
**OT-B5 (C).** ¿Qué son PLC, SCADA, HMI, MES y ERP? Una línea cada uno.
**OT-B6 (C).** TCP vs UDP: dos diferencias y un uso de cada uno.
**OT-B7 (MC).** Puerto por defecto de MQTT sin y con TLS:
a) 80/443 b) 1883/8883 c) 502/5020 d) 22/2222

## Nivel intermedio
**OT-I1 (C).** ¿Qué ocurre cuando se pierde Internet? Describe qué hace el gateway y qué debe cumplir el servidor al recuperar.
**OT-I2 (C).** ¿Qué significa QoS 0, 1 y 2 en MQTT? ¿Por qué QoS 1 puede generar duplicados?
**OT-I3 (DIS).** Define un mensaje JSON de telemetría con los campos mínimos y justifica cada uno.
**OT-I4 (DIS).** Diseña la estructura de topics MQTT para 20 máquinas en 3 sitios y las ACL básicas.
**OT-I5 (C).** Explica ISA-95, modelo Purdue e IEC 62443 y por qué **no** son equivalentes.
**OT-I6 (C).** Lista 6 riesgos de conectar directamente una red de control a Internet y sus mitigaciones.
**OT-I7 (CAL).** 20 máquinas envían 1 mensaje/s de 350 B. Calcula MB/día por máquina y por flota; ¿cuánto baja si agregas cada 5 s?
**OT-I8 (C).** ¿Para qué sirven heartbeat, LWT y *keep-alive*?
**OT-I9 (DEP).** Los datos llegan al broker pero no al dashboard. Da 6 hipótesis y el orden de pruebas.
**OT-I10 (C).** HTTP/REST vs MQTT: cuándo usarías cada uno para telemetría.

## Nivel avanzado
**OT-A1 (DIS).** Diseña la arquitectura completa (sensor → dashboard) para monitorear tractores, bombas y motores de un ingenio: componentes, protocolos, zonas de seguridad, buffer, alertas y qué **no** harías. Dibuja el diagrama (puedes abrir `diagrams/archify/architecture_case.html` **después** de intentarlo).
**OT-A2 (DIS).** Diseña una estrategia de *store & forward* con reintentos, idempotencia, orden y límites de buffer. Define el esquema SQL de idempotencia.
**OT-A3 (DIS).** Un cliente pide "controlar la velocidad de la bomba desde el celular". Responde como ingeniero: riesgos, requisitos previos y cómo lo abordarías por fases.
**OT-A4 (CAL).** Buffer para 24 h por gateway con 5 mensajes/s de 300 B. ¿Espacio? ¿Y si el enlace vuelve y se limita a 50 msg/s: cuánto tarda en vaciarse un buffer de 24 h a 1 msg/s (86 400 msgs)?
**OT-A5 (DEP).** Tras una caída de red aparecen duplicados y algunos timestamps en 1970. Da las causas probables y las correcciones.
**OT-A6 (DIS).** Diseña la seguridad de un gateway en campo: autenticación, cifrado, actualizaciones, acceso remoto, credenciales, y qué harías si roban el equipo.
**OT-A7 (C).** ¿Qué es un diodo de datos, una DMZ y una VPN? ¿Cuándo usar cada uno?
**OT-A8 (DIS).** Amplía el sistema a 50 máquinas sobre un enlace compartido de 64 kbit/s: recalcula el tráfico y decide qué enviar siempre y qué por excepción.

## Discusión para entrevista (respuesta abierta)
1. "Convergencia OT/IT" en 60 segundos.
2. ¿Qué aporta el edge computing a este proyecto?
3. ¿Cómo asegurarías que el dato que ve el gerente es confiable?
4. ¿Qué medirías para saber que **el sistema de monitoreo** funciona bien (monitorear el monitoreo)?
