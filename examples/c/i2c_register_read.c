/*
 * i2c_register_read.c
 * Patron de acceso a registros de un sensor I2C, con un "bus" simulado para poder
 * ejecutarlo en PC. En un MCU real se sustituyen i2c_write/i2c_read por la API de
 * la plataforma (HAL de STM32, Wire de Arduino, i2c_master de ESP-IDF, etc.).
 *
 * Sensor ficticio (NO es un dispositivo real): direccion 0x48,
 *   registro 0x00 = WHO_AM_I (0xA5), registro 0x01..0x02 = temperatura (16 bits, big-endian, 1/128 C).
 *
 *   gcc -std=c11 -Wall -Wextra -o i2c i2c_register_read.c && ./i2c
 */
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>

#define SENSOR_ADDR 0x48
#define REG_WHO_AM_I 0x00
#define REG_TEMP_MSB 0x01

/* ------------- Bus simulado (reemplazar en hardware real) ------------- */
static uint8_t fake_regs[3] = {0xA5, 0x0C, 0x80}; /* 0x0C80 = 3200 -> 25.0 C */
static bool fake_bus_connected = true;

static bool i2c_read_regs(uint8_t addr, uint8_t reg, uint8_t *buf, size_t len)
{
    if (!fake_bus_connected || addr != SENSOR_ADDR) return false;   /* NACK */
    if ((size_t)reg + len > sizeof fake_regs) return false;
    memcpy(buf, &fake_regs[reg], len);
    return true;
}
/* ----------------------------------------------------------------------- */

typedef enum { SENSOR_OK, SENSOR_NO_ACK, SENSOR_WRONG_ID } SensorStatus;

static SensorStatus sensor_read_temperature(float *temp_c)
{
    uint8_t id;
    if (!i2c_read_regs(SENSOR_ADDR, REG_WHO_AM_I, &id, 1)) return SENSOR_NO_ACK;
    if (id != 0xA5) return SENSOR_WRONG_ID;            /* verificar que el chip es el esperado */

    uint8_t raw[2];
    if (!i2c_read_regs(SENSOR_ADDR, REG_TEMP_MSB, raw, 2)) return SENSOR_NO_ACK;

    int16_t v = (int16_t)((uint16_t)raw[0] << 8 | raw[1]);    /* big-endian: MSB primero */
    *temp_c = v / 128.0f;
    return SENSOR_OK;
}

int main(void)
{
    float t;
    SensorStatus s = sensor_read_temperature(&t);
    printf("estado=%d temperatura=%.2f C\n", s, t);

    fake_bus_connected = false;    /* simula cable desconectado */
    s = sensor_read_temperature(&t);
    printf("estado=%d (1 = NACK: revisar cableado, pull-ups, direccion)\n", s);
    return 0;
}

/* Salida esperada:
 * estado=0 temperatura=25.00 C
 * estado=1 (1 = NACK: revisar cableado, pull-ups, direccion)
 */
