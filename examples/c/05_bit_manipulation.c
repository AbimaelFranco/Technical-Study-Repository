/*
 * 05_bit_manipulation.c
 * Programa 8: manipulacion de bits y mascaras (como se trabaja con registros).
 *
 *   gcc -std=c11 -Wall -Wextra -o bits 05_bit_manipulation.c && ./bits
 */
#include <stdint.h>
#include <stdio.h>

#define BIT(n)           (1u << (n))
#define SET_BIT(reg, n)  ((reg) |= BIT(n))     /* pone el bit n en 1 */
#define CLR_BIT(reg, n)  ((reg) &= ~BIT(n))    /* pone el bit n en 0 */
#define TGL_BIT(reg, n)  ((reg) ^= BIT(n))     /* invierte el bit n */
#define TST_BIT(reg, n)  (((reg) >> (n)) & 1u) /* lee el bit n */

/* Registro de configuracion imaginario de 8 bits (didactico):
 *   bit 7: ENABLE   bits 6..4: PRESCALER   bits 3..1: MODO   bit 0: IRQ_EN */
#define ENABLE_MASK   BIT(7)
#define PRESC_SHIFT   4
#define PRESC_MASK    (0x7u << PRESC_SHIFT)
#define MODE_SHIFT    1
#define MODE_MASK     (0x7u << MODE_SHIFT)

static void print_bin(const char *label, uint8_t v)
{
    printf("%-22s 0x%02X = ", label, v);
    for (int i = 7; i >= 0; --i) putchar((v >> i) & 1u ? '1' : '0');
    putchar('\n');
}

int main(void)
{
    uint8_t reg = 0;
    SET_BIT(reg, 7);                                  print_bin("ENABLE=1", reg);
    /* Modificar un CAMPO: primero limpiar con la mascara, despues escribir el valor desplazado. */
    reg = (uint8_t)((reg & ~PRESC_MASK) | (5u << PRESC_SHIFT)); print_bin("PRESCALER=5", reg);
    reg = (uint8_t)((reg & ~MODE_MASK) | (2u << MODE_SHIFT));   print_bin("MODO=2", reg);
    TGL_BIT(reg, 0);                                  print_bin("toggle bit0", reg);
    CLR_BIT(reg, 7);                                  print_bin("ENABLE=0", reg);
    printf("bit0=%u prescaler=%u\n", TST_BIT(reg, 0), (reg & PRESC_MASK) >> PRESC_SHIFT);

    /* Empaquetar y desempaquetar: temperatura DS18B20 (16 bits con signo, 1/16 C). */
    uint8_t lsb = 0x91, msb = 0x01;
    int16_t raw = (int16_t)((uint16_t)msb << 8 | lsb);  /* 0x0191 = 401 */
    printf("raw=%d -> %.4f C\n", raw, raw / 16.0f);

    /* Bytes de una trama CAN de 16 bits en big-endian y little-endian */
    uint16_t rpm = 1850;
    uint8_t le[2] = {(uint8_t)(rpm & 0xFF), (uint8_t)(rpm >> 8)};   /* little-endian: bajo primero */
    uint8_t be[2] = {(uint8_t)(rpm >> 8), (uint8_t)(rpm & 0xFF)};   /* big-endian: alto primero */
    printf("rpm=%u LE=%02X %02X BE=%02X %02X\n", rpm, le[0], le[1], be[0], be[1]);
    return 0;
}

/* Salida esperada:
 * ENABLE=1               0x80 = 10000000
 * PRESCALER=5            0xD0 = 11010000
 * MODO=2                 0xD4 = 11010100
 * toggle bit0            0xD5 = 11010101
 * ENABLE=0               0x55 = 01010101
 * bit0=1 prescaler=5
 * raw=401 -> 25.0625 C
 * rpm=1850 LE=3A 07 BE=07 3A
 */
