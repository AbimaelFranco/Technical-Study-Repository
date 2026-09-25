// arduino_temp_monitor.ino
// Adquiere temperatura de un DS18B20 y la transmite por UART como JSON linea a linea.
//
// REQUIERE (no es C/C++ estandar):
//   - Framework Arduino (Arduino IDE / PlatformIO): setup(), loop(), Serial, millis(), pinMode, ...
//   - Bibliotecas: "OneWire" (Paul Stoffregen) y "DallasTemperature" (Miles Burton), instalables desde el Library Manager.
//   - Placa con logica de 3.3 V o 5 V: verifica el rango de VDD del DS18B20 (3.0-5.5 V).
// Conexion: DQ -> pin 4 con pull-up de 4.7 kOhm a VDD; VDD y GND del sensor a la placa.
//
// Este sketch es DIDACTICO. No se ha ejecutado en hardware dentro de este repositorio.
// Una aplicacion industrial requiere watchdog, validacion adicional y pruebas.

#include <OneWire.h>
#include <DallasTemperature.h>

const uint8_t  ONE_WIRE_PIN   = 4;
const uint32_t SAMPLE_MS      = 1000;   // periodo de muestreo
const float    TEMP_MIN_VALID = -40.0f;
const float    TEMP_MAX_VALID = 150.0f;

OneWire oneWire(ONE_WIRE_PIN);
DallasTemperature sensors(&oneWire);

uint32_t lastSample = 0;
uint32_t seq = 0;                       // numero de secuencia para detectar perdidas/duplicados

void setup() {
  Serial.begin(115200);
  sensors.begin();
  sensors.setResolution(12);            // 12 bits: 0.0625 C, conversion ~750 ms
  sensors.setWaitForConversion(false);  // no bloquear: pedimos y leemos en el siguiente ciclo
  sensors.requestTemperatures();
}

void loop() {
  uint32_t now = millis();
  // Patron sin delay(): se compara con millis(). La resta con uint32_t maneja el desbordamiento (~49 dias).
  if (now - lastSample >= SAMPLE_MS) {
    lastSample = now;

    float t = sensors.getTempCByIndex(0);        // lee la conversion anterior
    sensors.requestTemperatures();               // inicia la siguiente

    bool valid = (t != DEVICE_DISCONNECTED_C) && t >= TEMP_MIN_VALID && t <= TEMP_MAX_VALID;

    // Una linea JSON por muestra: el gateway la parsea con json.loads (ver examples/python).
    Serial.print(F("{\"id\":\"esp-01\",\"seq\":")); Serial.print(seq++);
    Serial.print(F(",\"t_ms\":"));                   Serial.print(now);
    Serial.print(F(",\"temp_c\":"));
    if (valid) Serial.print(t, 2); else Serial.print(F("null"));
    Serial.print(F(",\"quality\":\""));              Serial.print(valid ? F("good") : F("bad"));
    Serial.println(F("\"}"));
  }
}
