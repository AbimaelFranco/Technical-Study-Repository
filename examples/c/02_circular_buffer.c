/*
 * 02_circular_buffer.c
 * Programa 4: buffer circular (ring buffer) para almacenar muestras.
 *
 * Por que: memoria fija (sin malloc), O(1) para push/pop, tipico entre una ISR
 * (productor) y el lazo principal (consumidor).
 *
 *   gcc -std=c11 -Wall -Wextra -o ring 02_circular_buffer.c && ./ring
 *
 * Aviso: esta version NO es segura entre ISR y main en un MCU real sin
 * secciones criticas o variables atomicas; solo con un productor y un consumidor
 * y un acceso a indices atomico se puede hacer lock-free. Ver docs/03 y docs/06.
 */
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>

#define RB_CAPACITY 4 /* pocos elementos para ver el comportamiento */

typedef struct {
    int16_t data[RB_CAPACITY]; /* almacenamiento estatico */
    uint8_t head;              /* proxima posicion de escritura */
    uint8_t tail;              /* proxima posicion de lectura */
    uint8_t count;             /* elementos almacenados (evita la ambiguedad lleno/vacio) */
    uint16_t overwritten;      /* muestras perdidas por desbordamiento */
} RingBuffer;

static void rb_init(RingBuffer *rb)
{
    rb->head = rb->tail = rb->count = 0;
    rb->overwritten = 0;
}

/* Politica: si esta lleno, SOBRESCRIBE la muestra mas antigua (util en telemetria: lo nuevo importa). */
static void rb_push(RingBuffer *rb, int16_t v)
{
    rb->data[rb->head] = v;
    rb->head = (uint8_t)((rb->head + 1) % RB_CAPACITY); /* el modulo da la vuelta */
    if (rb->count == RB_CAPACITY) {
        rb->tail = (uint8_t)((rb->tail + 1) % RB_CAPACITY); /* descarta la mas antigua */
        rb->overwritten++;
    } else {
        rb->count++;
    }
}

/* Devuelve false si esta vacio (el llamador decide que hacer). */
static bool rb_pop(RingBuffer *rb, int16_t *out)
{
    if (rb->count == 0) return false;
    *out = rb->data[rb->tail];
    rb->tail = (uint8_t)((rb->tail + 1) % RB_CAPACITY);
    rb->count--;
    return true;
}

int main(void)
{
    RingBuffer rb;
    rb_init(&rb);

    for (int16_t v = 1; v <= 6; ++v) rb_push(&rb, (int16_t)(v * 10)); /* 6 pushes en un buffer de 4 */

    int16_t x;
    printf("sobrescritas=%u, elementos=%u\n", rb.overwritten, rb.count);
    while (rb_pop(&rb, &x)) printf("pop: %d\n", x);
    return 0;
}

/* Salida esperada:
 * sobrescritas=2, elementos=4
 * pop: 30
 * pop: 40
 * pop: 50
 * pop: 60
 */
