#!/usr/bin/env python3
"""
i2c_multisensor.py
Varios sensores I2C en un bus compartido (Raspberry Pi + smbus2).

Instalacion:  pip install smbus2      | habilitar I2C:  sudo raspi-config -> Interface Options -> I2C
Verificar:    i2cdetect -y 1          (paquete i2c-tools)

Sensores del ejemplo (DIRECCIONES TIPICAS; comprueba con i2cdetect y el datasheet de TU modulo):
  0x48  ADS1115 (ADC 16 bit)   registro de conversion 0x00, big-endian
  0x68  MPU-6050 (IMU)         registro 0x75 = WHO_AM_I (0x68)  [datasheet/registro del MPU-6050]
  0x76  BME280 (T/P/H)         registro 0xD0 = chip id (0x60)   [datasheet Bosch]

Sin hardware: python i2c_multisensor.py --demo   (bus simulado).
Notas de diseno: un unico objeto de bus compartido, cada dispositivo aislado en su propia funcion,
errores por dispositivo (OSError) sin tumbar el resto del bus, y tiempos de espera segun datasheet.
"""
import argparse


class FakeBus:
    """Simula lo minimo de SMBus para la demo. addr -> {registro: bytes}"""
    def __init__(self, missing=()):
        self.mem = {0x48: {0x00: bytes([0x3F, 0xFF])}, 0x68: {0x75: bytes([0x68])}, 0x76: {0xD0: bytes([0x60])}}
        for a in missing:
            self.mem.pop(a, None)

    def read_i2c_block_data(self, addr, reg, length):
        if addr not in self.mem:
            raise OSError(121, "Remote I/O error (NACK)")
        return list(self.mem[addr][reg][:length])

    def __enter__(self): return self
    def __exit__(self, *a): return False


def read_ads1115_raw(bus, addr=0x48):
    hi, lo = bus.read_i2c_block_data(addr, 0x00, 2)
    value = (hi << 8) | lo
    return value - 65536 if value & 0x8000 else value      # complemento a 2 (16 bits con signo)


def read_chip_id(bus, addr, reg):
    return bus.read_i2c_block_data(addr, reg, 1)[0]


DEVICES = [
    ("ADS1115", 0x48, lambda b: read_ads1115_raw(b, 0x48)),
    ("MPU-6050 WHO_AM_I", 0x68, lambda b: hex(read_chip_id(b, 0x68, 0x75))),
    ("BME280 chip id", 0x76, lambda b: hex(read_chip_id(b, 0x76, 0xD0))),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--demo", action="store_true")
    ap.add_argument("--demo-missing", type=lambda s: int(s, 0), default=None, help="direccion a 'desconectar' en la demo")
    args = ap.parse_args()

    if args.demo or args.demo_missing is not None:
        bus_ctx = FakeBus(missing=[args.demo_missing] if args.demo_missing else [])
    else:
        from smbus2 import SMBus                          # solo se importa en hardware real
        bus_ctx = SMBus(1)                                # bus 1 = GPIO2 (SDA), GPIO3 (SCL) en Raspberry Pi

    with bus_ctx as bus:
        for name, addr, reader in DEVICES:
            try:
                print(f"0x{addr:02X} {name}: {reader(bus)}")
            except OSError as e:                          # NACK / bus error: un sensor caido no detiene los demas
                print(f"0x{addr:02X} {name}: ERROR {e}")


if __name__ == "__main__":
    main()

# Salida esperada con --demo:
# 0x48 ADS1115: 16383
# 0x68 MPU-6050 WHO_AM_I: 0x68
# 0x76 BME280 chip id: 0x60
# Con --demo-missing 0x68 la segunda linea muestra ERROR (NACK) y las otras siguen funcionando.
