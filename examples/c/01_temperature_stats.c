/*
 * 01_temperature_stats.c
 * Programas 1, 2 y 3 del modulo 03:
 *   1) Leer y clasificar temperaturas.
 *   2) Calcular promedio, maximo y minimo.
 *   3) Detectar valores invalidos (NaN, fuera de rango, sensor desconectado).
 *
 * C estandar (C11), sin hardware. Compilar y ejecutar en PC:
 *   gcc -std=c11 -Wall -Wextra -o temp_stats 01_temperature_stats.c -lm && ./temp_stats
 */
#include <math.h>    /* isnan */
#include <stdbool.h> /* bool */
#include <stddef.h>  /* size_t */
#include <stdio.h>

/* Limites fisicamente plausibles para un motor (ejemplo didactico). */
#define TEMP_MIN_VALID (-40.0f)
#define TEMP_MAX_VALID (150.0f)
#define DS18B20_DISCONNECTED (-127.0f) /* valor tipico de driver cuando el bus lee 0xFF */
#define DS18B20_POWER_ON (85.0f)       /* valor de reset del DS18B20 */

typedef enum { TEMP_NORMAL, TEMP_WARNING, TEMP_CRITICAL, TEMP_INVALID } TempClass;

/* ---- 3) Validacion: devuelve true si la lectura es utilizable ---- */
static bool temp_is_valid(float t)
{
    if (isnan(t)) return false;                        /* no es un numero */
    if (t == DS18B20_DISCONNECTED) return false;       /* sensor desconectado */
    if (t < TEMP_MIN_VALID || t > TEMP_MAX_VALID) return false; /* fuera de rango fisico */
    return true;
}

/* ---- 1) Clasificacion por umbrales (los umbrales dependen de la maquina) ---- */
static TempClass temp_classify(float t)
{
    if (!temp_is_valid(t)) return TEMP_INVALID;
    if (t >= 105.0f) return TEMP_CRITICAL; /* ejemplo: critico */
    if (t >= 95.0f) return TEMP_WARNING;   /* ejemplo: advertencia */
    return TEMP_NORMAL;
}

static const char *temp_class_name(TempClass c)
{
    switch (c) {
    case TEMP_NORMAL:   return "NORMAL";
    case TEMP_WARNING:  return "WARNING";
    case TEMP_CRITICAL: return "CRITICAL";
    default:            return "INVALID";
    }
}

/* ---- 2) Estadisticas: ignora invalidos. Devuelve el numero de muestras validas ---- */
typedef struct {
    float mean, min, max;
    size_t valid, invalid;
} TempStats;

/* Entrada: arreglo y su tamano (un arreglo pierde su tamano al pasarlo a una funcion).
 * Salida: struct con resultados. Complejidad: O(n) tiempo, O(1) memoria. */
static TempStats temp_stats(const float *data, size_t n)
{
    TempStats s = {0.0f, 0.0f, 0.0f, 0, 0};
    double sum = 0.0; /* double para reducir error de acumulacion */
    for (size_t i = 0; i < n; ++i) {
        if (!temp_is_valid(data[i])) { s.invalid++; continue; }
        if (s.valid == 0 || data[i] < s.min) s.min = data[i];
        if (s.valid == 0 || data[i] > s.max) s.max = data[i];
        sum += data[i];
        s.valid++;
    }
    if (s.valid > 0) s.mean = (float)(sum / (double)s.valid); /* evita dividir entre 0 */
    return s;
}

int main(void)
{
    const float samples[] = {78.5f, 80.1f, 96.3f, -127.0f, 85.0f, 110.2f, NAN, 79.9f, 200.0f};
    const size_t n = sizeof samples / sizeof samples[0];

    for (size_t i = 0; i < n; ++i)
        printf("muestra %zu: %7.2f -> %s\n", i, samples[i], temp_class_name(temp_classify(samples[i])));

    TempStats s = temp_stats(samples, n);
    printf("\nvalidas=%zu invalidas=%zu promedio=%.2f min=%.2f max=%.2f\n", s.valid, s.invalid, s.mean, s.min, s.max);
    /* Nota: 85.0 pasa como valida (podria ser el valor de reset del DS18B20).
     * Un sistema real debe distinguirlo por CRC/estado de conversion, no solo por valor. */
    return 0;
}

/* Salida esperada:
 * muestra 0:   78.50 -> NORMAL
 * muestra 1:   80.10 -> NORMAL
 * muestra 2:   96.30 -> WARNING
 * muestra 3: -127.00 -> INVALID
 * muestra 4:   85.00 -> NORMAL
 * muestra 5:  110.20 -> CRITICAL
 * muestra 6:     nan -> INVALID
 * muestra 7:   79.90 -> NORMAL
 * muestra 8:  200.00 -> INVALID
 *
 * validas=6 invalidas=3 promedio=88.33 min=78.50 max=110.20
 */
