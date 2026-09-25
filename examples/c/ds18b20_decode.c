/*
 * ds18b20_decode.c
 * Decodifica el scratchpad de 9 bytes de un DS18B20 y verifica el CRC-8 Maxim.
 * Sirve para entender el formato; el acceso real al bus 1-Wire depende de la plataforma
 * (driver w1-therm en Linux, libreria OneWire en Arduino, RMT/UART en ESP32, etc.).
 *
 * Scratchpad (segun el datasheet del DS18B20):
 *   byte 0: temperatura LSB     byte 1: temperatura MSB
 *   byte 2: TH (alarma alta)    byte 3: TL (alarma baja)
 *   byte 4: configuracion (resolucion)   bytes 5..7: reservados   byte 8: CRC
 * CRC-8: polinomio x^8 + x^5 + x^4 + 1 (0x31; forma reflejada 0x8C), inicial 0.
 *
 *   gcc -std=c11 -Wall -Wextra -o ds ds18b20_decode.c && ./ds
 */
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>

/* CRC-8 Dallas/Maxim procesando bit a bit (LSB primero). */
static uint8_t crc8_maxim(const uint8_t *data, unsigned len)
{
    uint8_t crc = 0;
    for (unsigned i = 0; i < len; ++i) {
        uint8_t byte = data[i];
        for (int b = 0; b < 8; ++b) {
            uint8_t mix = (crc ^ byte) & 0x01;
            crc >>= 1;
            if (mix) crc ^= 0x8C;   /* polinomio reflejado */
            byte >>= 1;
        }
    }
    return crc;
}

typedef enum { DS_OK, DS_BAD_CRC, DS_NOT_CONVERTED, DS_DISCONNECTED } DsStatus;

static DsStatus ds18b20_decode(const uint8_t sp[9], float *temp_c)
{
    /* Un bus en alto constante (sin dispositivo) devuelve todo 0xFF. */
    bool all_ff = true;
    for (int i = 0; i < 9; ++i) if (sp[i] != 0xFF) all_ff = false;
    if (all_ff) return DS_DISCONNECTED;

    if (crc8_maxim(sp, 8) != sp[8]) return DS_BAD_CRC;   /* corrupto por ruido/timing */

    int16_t raw = (int16_t)((uint16_t)sp[1] << 8 | sp[0]);   /* complemento a 2, unidades de 1/16 C */

    /* Resolucion segun bits R1:R0 del byte de configuracion (bits 6:5). En 9..11 bits los bits bajos son indefinidos. */
    switch ((sp[4] >> 5) & 0x3) {
    case 0: raw &= ~0x7; break;  /*  9 bits */
    case 1: raw &= ~0x3; break;  /* 10 bits */
    case 2: raw &= ~0x1; break;  /* 11 bits */
    default: break;              /* 12 bits */
    }

    /* Valor de reset 85.0 C (raw = 0x0550): si aparece con TH/TL por defecto es probable que no haya conversion. */
    if (raw == 0x0550 && sp[2] == 0x4B && sp[3] == 0x46) return DS_NOT_CONVERTED;

    *temp_c = (float)raw / 16.0f;
    return DS_OK;
}

int main(void)
{
    /* Ejemplo del datasheet: 25.0625 C = 0x0191 */
    uint8_t good[9] = {0x91, 0x01, 0x4B, 0x46, 0x7F, 0xFF, 0x0F, 0x10, 0x00};
    good[8] = crc8_maxim(good, 8);        /* se calcula el CRC para que el ejemplo sea consistente */

    uint8_t neg[9]  = {0x5E, 0xFF, 0x4B, 0x46, 0x7F, 0xFF, 0x02, 0x10, 0x00};  /* -10.125 C */
    neg[8] = crc8_maxim(neg, 8);

    uint8_t reset[9] = {0x50, 0x05, 0x4B, 0x46, 0x7F, 0xFF, 0x0C, 0x10, 0x00};  /* 85 C sin convertir */
    reset[8] = crc8_maxim(reset, 8);

    uint8_t noise[9] = {0x91, 0x01, 0x4B, 0x46, 0x7F, 0xFF, 0x0F, 0x10, 0x55};  /* CRC malo */
    uint8_t none[9]  = {0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF};

    const uint8_t *cases[] = {good, neg, reset, noise, none};
    const char *names[] = {"normal", "negativa", "reset 85C", "ruido", "desconectado"};
    for (int i = 0; i < 5; ++i) {
        float t = 0;
        DsStatus s = ds18b20_decode(cases[i], &t);
        if (s == DS_OK) printf("%-13s -> %.4f C\n", names[i], t);
        else printf("%-13s -> error %d\n", names[i], s);
    }
    return 0;
}

/* Salida esperada:
 * normal        -> 25.0625 C
 * negativa      -> -10.1250 C
 * reset 85C     -> error 2
 * ruido         -> error 1
 * desconectado  -> error 3
 */
