/*
 * 06_buggy_code.c
 * Programa 9: codigo defectuoso, explicacion y correccion.
 *
 * La version DEFECTUOSA esta desactivada con BUGGY 0 para que el archivo compile y corra.
 * Cambia a "#define BUGGY 1" para ver el comportamiento incorrecto.
 * Usar -fsanitize=address,undefined (gcc/clang) delata varios de estos errores.
 *
 *   gcc -std=c11 -Wall -Wextra -o buggy 06_buggy_code.c && ./buggy
 */
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>

#define BUGGY 0

#if BUGGY
/* --------------------------- DEFECTUOSO --------------------------- */
float average(int *data, int n)
{
    int sum;                          /* BUG 1: no inicializada -> valor basura */
    for (int i = 0; i <= n; i++)      /* BUG 2: <= lee data[n], fuera de limites */
        sum += data[i];
    return sum / n;                   /* BUG 3: division entera pierde decimales; n==0 -> division por cero */
}

char *make_label(int id)
{
    char buf[8];
    sprintf(buf, "sensor-%d", id);    /* BUG 4: desborda buf con ids grandes (buffer overflow) */
    return buf;                       /* BUG 5: devuelve puntero a memoria local (dangling pointer) */
}

#else
/* ---------------------------- CORREGIDO ---------------------------- */
/* Devuelve 0 si hay error (n <= 0 o puntero nulo); el promedio via out. */
static int average(const int *data, size_t n, float *out)
{
    if (data == NULL || out == NULL || n == 0) return 0;  /* validar entradas */
    long sum = 0;                                         /* inicializada y con margen contra overflow */
    for (size_t i = 0; i < n; i++) sum += data[i];        /* < n: limites correctos */
    *out = (float)sum / (float)n;                         /* division en punto flotante */
    return 1;
}

/* El llamador aporta el buffer; snprintf limita la escritura al tamano. */
static int make_label(char *buf, size_t size, int id)
{
    int written = snprintf(buf, size, "sensor-%d", id);
    return (written >= 0 && (size_t)written < size);      /* 0 si se trunco */
}
#endif

int main(void)
{
#if !BUGGY
    int data[] = {10, 20, 35};
    float avg;
    if (average(data, 3, &avg)) printf("promedio=%.2f\n", avg);   /* 21.67 (con int seria 21) */

    char label[16];
    printf("etiqueta ok=%d -> %s\n", make_label(label, sizeof label, 7), label);
    char small[8];
    printf("etiqueta ok=%d (truncada) -> %s\n", make_label(small, sizeof small, 123456), small);
    (void)strlen; /* evita advertencia si se ajustan includes */
#endif
    return 0;
}

/* Salida esperada (version corregida):
 * promedio=21.67
 * etiqueta ok=1 -> sensor-7
 * etiqueta ok=0 (truncada) -> sensor-
 */
