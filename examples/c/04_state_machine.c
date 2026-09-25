/*
 * 04_state_machine.c
 * Programas 6 y 7: maquina de estados de un sistema de monitoreo y struct de medicion.
 * Corresponde a diagrams/state_machine_firmware.mmd y a diagrams/archify/lifecycle_firmware.html
 *
 * Se simula el tiempo con un ciclo for para poder ejecutarlo en PC:
 *   gcc -std=c11 -Wall -Wextra -o fsm 04_state_machine.c && ./fsm
 */
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>

/* ---- 7) struct que representa una medicion ---- */
typedef enum { Q_GOOD = 0, Q_UNCERTAIN = 1, Q_BAD = 2 } Quality;

typedef struct {
    uint32_t timestamp_s; /* segundos desde el arranque (o epoch) */
    uint8_t  sensor_id;
    float    value;       /* magnitud en unidades SI (aqui grados C) */
    Quality  quality;     /* calidad del dato: nunca enviar un numero sin decir si es confiable */
} Measurement;

typedef enum { ST_INIT, ST_SELF_TEST, ST_SAMPLING, ST_VALIDATE, ST_TRANSMIT, ST_DEGRADED, ST_NO_LINK, ST_FAULT, ST_SAFE } State;

static const char *STATE_NAMES[] = {"INIT", "SELF_TEST", "SAMPLING", "VALIDATE", "TRANSMIT", "DEGRADED", "NO_LINK", "FAULT", "SAFE"};

typedef struct {
    State state;
    Measurement last;
    uint8_t fault_retries;
    uint8_t link_failures;
    uint32_t samples;   /* muestras tomadas */
} Monitor;

/* Simuladores de hardware (en un MCU real serian lecturas de I2C/1-Wire y envio por UART). */
static bool sensor_present(void) { return true; }
static float read_sensor(uint32_t n) { return n == 1 ? 300.0f : 80.0f + (float)n; } /* muestra n=1: lectura absurda */
static bool send_ok(uint32_t t) { return !(t >= 14 && t <= 21); }                    /* t=14..21: gateway no responde */

static void step(Monitor *m, uint32_t t)
{
    State next = m->state;
    switch (m->state) {
    case ST_INIT:      next = ST_SELF_TEST; break;
    case ST_SELF_TEST: next = sensor_present() ? ST_SAMPLING : ST_FAULT; break;
    case ST_SAMPLING:
        m->last = (Measurement){t, 1, read_sensor(m->samples++), Q_GOOD};
        next = ST_VALIDATE;
        break;
    case ST_VALIDATE:
        if (m->last.value < -40.0f || m->last.value > 150.0f) { m->last.quality = Q_BAD; next = ST_DEGRADED; }
        else next = ST_TRANSMIT;
        break;
    case ST_DEGRADED:  next = ST_SAMPLING; break; /* el dato se marca BAD y se sigue muestreando */
    case ST_TRANSMIT:
        if (send_ok(t)) { m->link_failures = 0; next = ST_SAMPLING; }
        else if (++m->link_failures >= 2) next = ST_NO_LINK;  /* 2 fallos seguidos */
        else next = ST_SAMPLING;
        break;
    case ST_NO_LINK:   next = send_ok(t) ? ST_SAMPLING : ST_NO_LINK; break;
    case ST_FAULT:     next = (++m->fault_retries < 3) ? ST_SELF_TEST : ST_SAFE; break;
    case ST_SAFE:      break; /* en un MCU real: esperar al watchdog / reset */
    }
    if (next != m->state) printf("t=%u  %-9s -> %-9s (valor=%.1f q=%d)\n", t, STATE_NAMES[m->state], STATE_NAMES[next], m->last.value, m->last.quality);
    m->state = next;
}

int main(void)
{
    Monitor m = {ST_INIT, {0, 0, 0.0f, Q_BAD}, 0, 0, 0};
    for (uint32_t t = 0; t < 30; ++t) step(&m, t);
    return 0;
}
