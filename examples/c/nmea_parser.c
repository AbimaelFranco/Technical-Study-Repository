/*
 * nmea_parser.c
 * Parsea una frase NMEA-0183 $GPGGA que llega por UART desde un modulo GPS.
 * Valida el checksum (XOR entre '$' y '*') y extrae hora, latitud y longitud.
 *
 * NMEA: latitud "ddmm.mmmm", longitud "dddmm.mmmm"; grados decimales = dd + mm.mmmm/60.
 *
 *   gcc -std=c11 -Wall -Wextra -o nmea nmea_parser.c && ./nmea
 *
 * En un MCU, la linea se arma byte a byte desde la UART (ver docs/02, seccion UART).
 */
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static bool nmea_checksum_ok(const char *s)
{
    if (*s != '$') return false;
    uint8_t x = 0;
    const char *p = s + 1;
    while (*p && *p != '*') x ^= (uint8_t)*p++;
    if (*p != '*') return false;
    unsigned rx;
    if (sscanf(p + 1, "%2x", &rx) != 1) return false;
    return rx == x;
}

/* "4807.038" y 'N' -> 48.1173 */
static double nmea_to_degrees(const char *field, char hemi)
{
    double v = atof(field);
    int deg = (int)(v / 100);
    double minutes = v - deg * 100;
    double d = deg + minutes / 60.0;
    return (hemi == 'S' || hemi == 'W') ? -d : d;
}

int main(void)
{
    const char *line = "$GPGGA,123519,4807.038,N,01131.000,E,1,08,0.9,545.4,M,46.9,M,,*47";

    if (!nmea_checksum_ok(line)) { puts("checksum invalido"); return 1; }

    /* strtok modifica la cadena: se trabaja sobre una copia local. */
    char buf[96];
    strncpy(buf, line, sizeof buf - 1);
    buf[sizeof buf - 1] = '\0';

    /* Campos separados por coma. strtok salta campos vacios, pero los de interes no lo estan. */
    char *f[8] = {0};
    int n = 0;
    for (char *t = strtok(buf, ",*"); t && n < 8; t = strtok(NULL, ",*")) f[n++] = t;
    /* f[0]="$GPGGA" f[1]=hora f[2]=lat f[3]=N/S f[4]=lon f[5]=E/W f[6]=calidad f[7]=satelites */
    if (n < 8) { puts("frase incompleta"); return 1; }

    if (atoi(f[6]) == 0) { puts("sin fix GPS"); return 1; }

    printf("hora UTC: %.2s:%.2s:%.2s\n", f[1], f[1] + 2, f[1] + 4);
    printf("lat=%.5f lon=%.5f sats=%s\n", nmea_to_degrees(f[2], f[3][0]), nmea_to_degrees(f[4], f[5][0]), f[7]);
    return 0;
}

/* Salida esperada:
 * hora UTC: 12:35:19
 * lat=48.11730 lon=11.51667 sats=08
 */
