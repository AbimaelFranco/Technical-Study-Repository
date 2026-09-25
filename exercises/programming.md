# Ejercicios · Programación (C/C++, Python, Git)

> Soluciones en [`answer_key.md`](answer_key.md) (sección **Programación**). Teoría: [`docs/03`](../docs/03_c_cpp.md), [`docs/04`](../docs/04_python.md), [`docs/06`](../docs/06_sistemas_embebidos.md), [`docs/09`](../docs/09_git_y_control_versiones.md).
> **Consejo:** para los ejercicios de escribir código, hazlo primero en papel/editor sin ayuda (como en la prueba) y luego ejecútalo.

## A. C / C++

### Nivel básico
**PG-B1 (LEC).** ¿Qué imprime?
```c
#include <stdio.h>
#include <stdint.h>
int main(void) {
    uint8_t a = 200, b = 100;
    uint8_t s = a + b;
    int t = a + b;
    printf("%u %d\n", s, t);
    return 0;
}
```
**PG-B2 (LEC).** ¿Qué imprime? `int x = 7; int y = 2; printf("%d %f", x / y, (float)x / y);`

**PG-B3 (CAL).** Escribe las expresiones en C para: (a) poner en 1 el bit 3 de `reg`; (b) poner en 0 el bit 5; (c) invertir el bit 0; (d) leer el bit 7 (0 o 1); (e) comprobar si el bit 2 está en 0.

**PG-B4 (MC).** `volatile` garantiza:
a) Atomicidad b) Que el compilador no optimice/cachee los accesos c) Seguridad entre hilos d) Que la variable esté en Flash

**PG-B5 (C).** ¿Qué diferencia hay entre `const int *p`, `int *const p` y `const int *const p`?

**PG-B6 (C).** ¿Qué es un *puntero nulo* y por qué se valida antes de desreferenciar?

### Nivel intermedio
**PG-I1 (DEP).** Encuentra y corrige los errores:
```c
float average(int *data, int n) {
    int sum;
    for (int i = 0; i <= n; i++) sum += data[i];
    return sum / n;
}
```
**PG-I2 (DEP).** ¿Qué falla?
```c
char *name_of(int id) {
    char buf[8];
    sprintf(buf, "sensor-%d", id);
    return buf;
}
```
**PG-I3 (CAL).** Dado el registro `CTRL` de 8 bits: bit7 = ENABLE, bits6..4 = PRESC, bits3..1 = MODE, bit0 = IRQ. Escribe código para: configurar PRESC = 5 y MODE = 2 **sin alterar** los demás bits; ¿cuál es el valor final si `CTRL` inicial = 0x81?

**PG-I4 (LEC).** ¿Qué imprime?
```c
uint16_t v = 0x1234;
uint8_t lo = v & 0xFF, hi = v >> 8;
printf("%02X %02X\n", lo, hi);
```
**PG-I5 (C).** ¿Por qué el siguiente bucle es infinito? `for (uint8_t i = 0; i < 256; i++) {}`

**PG-I6 (DIS).** Escribe en C una función `bool parse_temp(const char *s, float *out)` que convierta `"85.25"` a `float` validando que **toda** la cadena sea numérica y que el resultado esté en [−40, 150].

**PG-I7 (DIS).** Implementa un buffer circular de `int16_t` con capacidad 8, con `push` (sobrescribe el más antiguo si está lleno) y `pop`. ¿Qué problemas hay si `push` corre en una ISR y `pop` en el lazo principal?

**PG-I8 (C).** Compara `malloc` en un MCU vs en Linux. ¿Cuándo lo evitarías?

**PG-I9 (C++).** ¿Qué son las referencias y por qué `void f(const std::string& s)` es preferible a `void f(std::string s)` para cadenas largas?

**PG-I10 (C).** ¿Qué imprime `sizeof` de un `uint8_t arr[10]` dentro de `main`, y dentro de una función que recibe `uint8_t *arr`?

### Nivel avanzado
**PG-A1 (DIS).** Diseña una máquina de estados para un nodo: INIT → SELF_TEST → SAMPLING → VALIDATE → TRANSMIT, con DEGRADED, NO_LINK y FAULT. Define tabla de transiciones, condiciones y qué se hace en cada estado. ¿Dónde se alimenta el watchdog?

**PG-A2 (DIS).** Escribe un parser de tramas `$id,valor*CS\n` (CS = XOR de los caracteres entre `$` y `*`) que procese **un byte por llamada**. ¿Cómo resincronizas tras un byte perdido?

**PG-A3 (DEP).** Una ISR incrementa `uint32_t pulses`; el lazo principal lo lee cada segundo y lo pone a 0. A veces `pulses` da valores absurdos. ¿Por qué? Propón dos soluciones.

**PG-A4 (C).** ¿Cómo evitas `delay()` bloqueante para muestrear cada 1 s en Arduino? ¿Por qué `now - last >= period` funciona aunque `millis()` desborde?

**PG-A5 (DIS).** ¿Qué harías para que un firmware sea robusto ante un sensor que deja de responder? Enumera 8 medidas.

**PG-A6 (C).** Explica *endianness* y cómo afecta al empaquetar un `uint16_t` de RPM en una trama CAN.

## B. Python

### Nivel básico
**PY-B1 (LEC).** ¿Qué imprime?
```python
def add(x, acc=[]):
    acc.append(x)
    return acc
print(add(1), add(2))
```
**PY-B2 (LEC).** ¿Resultado? `[t for t in [70, 95.5, -127, 101] if -40 <= t <= 100]`

**PY-B3 (C).** Diferencias entre lista, tupla, diccionario y set con un ejemplo de sensores.

**PY-B4 (C).** ¿Por qué `with open(...)` es preferible a `open()` + `close()`?

**PY-B5 (MC).** `time.monotonic()` se usa para:
a) Obtener la fecha b) Medir intervalos sin que le afecten cambios del reloj c) Dormir el programa d) Sincronizar con NTP

### Nivel intermedio
**PY-I1 (DIS).** Escribe `stats(values)` que devuelva mín, máx, promedio y mediana, ignore `None`/`NaN`, y devuelva `None` si no hay datos válidos.

**PY-I2 (DIS).** Lee un CSV `timestamp,device_id,sensor,value,unit`; descarta filas con valor no numérico (reportando el número de línea) y calcula el promedio por `(device_id, sensor)`.

**PY-I3 (DIS).** Escribe un parser de mensajes JSON de telemetría que valide campos requeridos, tipos y que `ts` sea ISO-8601 UTC; lanza una excepción propia si es inválido.

**PY-I4 (DEP).** ¿Qué falla?
```python
r = requests.post(URL, json=data)
print(r.json()["ok"])
```
**PY-I5 (DIS).** Implementa `post_with_retry(payload)` con timeout, 5 reintentos con backoff exponencial y jitter, sin reintentar errores 4xx. ¿Qué hace falta en el servidor para que los reintentos no dupliquen?

**PY-I6 (C).** Explica las diferencias entre un **script** y un **servicio de larga duración** (al menos 6 aspectos).

**PY-I7 (DIS).** Implementa un detector de pérdida de comunicación: cada dispositivo debe hablar cada ≤ 5 s; emite `OFFLINE`/`ONLINE`. ¿Por qué usar `time.monotonic()` y un reloj inyectable?

**PY-I8 (C).** ¿Cuándo usarías `logging` en vez de `print`? Da 4 razones y muestra una configuración con archivo rotativo.

### Nivel avanzado
**PY-A1 (DIS).** Diseña un servicio Python que lee JSON por serial, valida, guarda en una cola SQLite y envía por HTTP con reintentos. Indica hilos/colas, manejo de SIGTERM, y cómo garantizas orden y no duplicados.

**PY-A2 (DEP).** El servicio anterior consume 100 % de CPU cuando se desconecta el USB-serie. Encuentra la causa probable y corrígela.

**PY-A3 (DIS).** Implementa alertas con umbral, confirmación de 3 muestras e histéresis. Escribe casos de prueba (incluye oscilación alrededor del umbral).

**PY-A4 (C).** ¿Por qué guardar timestamps en UTC? ¿Qué problemas trae usar la hora local con horario de verano? (Guatemala no lo aplica actualmente; ¿por qué debes diseñar igual sin suponerlo?)

**PY-A5 (DIS).** Calcula RMS y factor de cresta de una ventana de 1000 muestras; ¿cómo detectarías un cambio respecto a una línea base sin falsos positivos por cambios de carga?

## C. Git

**GIT-1 (C).** Diferencia entre Git y GitHub; entre `fetch` y `pull`; entre `merge` y `rebase`.
**GIT-2 (DIS).** Describe los comandos para: crear una rama, hacer dos commits, subirla, abrir PR, y luego actualizar `main` local.
**GIT-3 (DEP).** Al hacer `git pull` aparece un conflicto en `config.py`. Describe cómo lo resuelves.
**GIT-4 (DIS).** Subiste por error una contraseña a un commit ya publicado. ¿Qué haces? (piensa más allá de borrar la línea)
**GIT-5 (C).** ¿Cómo recuperas la versión de un archivo de hace tres commits sin perder tu trabajo actual? ¿Y cómo deshaces un commit ya publicado sin reescribir historia?
**GIT-6 (C).** ¿Qué debe ir en `.gitignore` en un proyecto de firmware + gateway Python?

## D. Sistemas embebidos

**EMB-1 (C).** Polling vs interrupciones: da un caso para cada uno y el patrón híbrido ISR-bandera.
**EMB-2 (C).** ¿Qué hace un watchdog? ¿Dónde lo alimentas y por qué no en una ISR?
**EMB-3 (C).** Compara Arduino, ESP32 y Raspberry Pi para: (a) nodo de sensor; (b) gateway; (c) control con tiempos estrictos.
**EMB-4 (DIS).** El MCU se reinicia cada pocos segundos al activar el Wi-Fi. Lista las causas probables y las pruebas.
**EMB-5 (CAL).** PWM a 1 kHz con duty 35 % a 3.3 V. ¿Voltaje promedio? ¿Cómo lo convertirías en analógico y qué pasa si la frecuencia del PWM es demasiado baja?
