/*
 * 03_serial_parser.c
 * Programa 5: parser de mensajes seriales.
 *
 * Formato del mensaje (ASCII, definido para este ejemplo):
 *     $<sensor_id>,<valor>*<CS>\n
 *   ej: $T1,85.25*4C\n
 * CS = XOR de todos los caracteres entre '$' y '*', en hexadecimal (2 digitos).
 *
 * El parser es una maquina de estados que consume UN byte por llamada
 * (asi funciona en una ISR o en un lazo que lee la UART sin bloquear).
 *
 *   gcc -std=c11 -Wall -Wextra -o parser 03_serial_parser.c && ./parser
 */
#include <ctype.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MSG_MAX 32

typedef enum { WAIT_START, IN_BODY, CS_HI, CS_LO } ParseState;

typedef struct {
    ParseState state;
    char body[MSG_MAX]; /* entre '$' y '*' */
    uint8_t len;
    uint8_t checksum;   /* XOR acumulado */
    uint8_t rx_cs;      /* checksum recibido */
} Parser;

typedef struct {
    char id[8];
    float value;
} Message;

static int hexval(char c)
{
    if (c >= '0' && c <= '9') return c - '0';
    if (c >= 'A' && c <= 'F') return c - 'A' + 10;
    if (c >= 'a' && c <= 'f') return c - 'a' + 10;
    return -1;
}

static void parser_reset(Parser *p) { p->state = WAIT_START; p->len = 0; p->checksum = 0; p->rx_cs = 0; }

/* Interpreta "T1,85.25" -> id y valor. Valida todo: nunca confiar en la entrada. */
static bool decode_body(const char *body, Message *m)
{
    const char *comma = strchr(body, ',');
    if (!comma || comma == body || (size_t)(comma - body) >= sizeof m->id) return false;
    memcpy(m->id, body, (size_t)(comma - body));
    m->id[comma - body] = '\0';

    char *end;
    m->value = strtof(comma + 1, &end);           /* convierte y avisa donde se detuvo */
    return end != comma + 1 && *end == '\0';      /* debe consumir todo el texto */
}

/* Devuelve true cuando se completo un mensaje valido y lo escribe en *out. */
static bool parser_feed(Parser *p, char c, Message *out)
{
    switch (p->state) {
    case WAIT_START:
        if (c == '$') { parser_reset(p); p->state = IN_BODY; }
        break;
    case IN_BODY:
        if (c == '*') { p->body[p->len] = '\0'; p->state = CS_HI; }
        else if (c == '$') { parser_reset(p); p->state = IN_BODY; }             /* resincroniza */
        else if (p->len < MSG_MAX - 1) { p->body[p->len++] = c; p->checksum ^= (uint8_t)c; }
        else parser_reset(p);                                                    /* desborde: descarta */
        break;
    case CS_HI: {
        int h = hexval(c);
        if (h < 0) { parser_reset(p); break; }
        p->rx_cs = (uint8_t)(h << 4);
        p->state = CS_LO;
        break;
    }
    case CS_LO: {
        int l = hexval(c);
        bool ok = false;
        if (l >= 0) {
            p->rx_cs |= (uint8_t)l;
            ok = (p->rx_cs == p->checksum) && decode_body(p->body, out);
        }
        parser_reset(p);
        return ok;
    }
    }
    return false;
}

static uint8_t xor_cs(const char *s) { uint8_t x = 0; while (*s) x ^= (uint8_t)*s++; return x; }

int main(void)
{
    /* Se calcula el checksum en tiempo de ejecucion para que el ejemplo sea correcto. */
    char good[40], bad[40];
    snprintf(good, sizeof good, "$T1,85.25*%02X\n", xor_cs("T1,85.25"));
    snprintf(bad, sizeof bad, "junk$T1,85.25*00\n");     /* checksum incorrecto */
    const char *stream_parts[] = {"ruido", good, bad, "$T2,abc*00\n"};

    Parser p; parser_reset(&p);
    Message m;
    for (size_t i = 0; i < sizeof stream_parts / sizeof stream_parts[0]; ++i) {
        for (const char *s = stream_parts[i]; *s; ++s) {
            if (parser_feed(&p, *s, &m)) printf("OK  id=%s valor=%.2f\n", m.id, m.value);
        }
    }
    printf("fin\n");
    return 0;
}

/* Salida esperada: solo el mensaje bueno se acepta.
 * OK  id=T1 valor=85.25
 * fin
 */
