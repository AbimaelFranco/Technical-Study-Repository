# Ejercicios · Fundamentos de electrónica y sensores

> Soluciones en [`answer_key.md`](answer_key.md) (sección **Fundamentos**). Intenta resolver **sin mirar**, con calculadora. Tipo: **C** conceptual · **MC** opción múltiple · **CAL** cálculo · **LEC** lectura de esquema/código · **DEP** depuración · **DIS** diseño.
> Teoría: [`docs/01`](../docs/01_fundamentos_electronica.md), [`docs/05`](../docs/05_sensores_y_adquisicion.md), [`docs/10`](../docs/10_esquematicos_y_diseno_3d.md).

## Nivel básico

**F-B1 (CAL).** Una resistencia de 470 Ω se conecta a 12 V. Calcula la corriente, la potencia disipada y elige la potencia nominal comercial mínima razonable (1/4 W, 1/2 W, 1 W).

**F-B2 (CAL).** Un LED (Vf ≈ 2.0 V) debe conducir ≈ 8 mA desde 3.3 V. Calcula R y elige un valor comercial cercano; ¿qué corriente circula realmente?

**F-B3 (CAL).** Un ADC de 12 bits con Vref = 3.3 V entrega 1000 cuentas. ¿Qué voltaje hay en la entrada? ¿Cuál es el LSB?

**F-B4 (MC).** ¿Cuál es la función de una resistencia *pull-up* en un pin de entrada?
a) Limitar la corriente a un LED b) Definir un nivel alto cuando nada maneja la línea c) Filtrar ruido de alta frecuencia d) Aumentar la velocidad del reloj

**F-B5 (MC).** ¿Cuál afirmación es correcta sobre el GPIO de una Raspberry Pi?
a) Tolera 5 V b) Opera a 3.3 V y no tolera 5 V c) Puede entregar 500 mA por pin d) Tiene ADC integrado de 10 bits

**F-B6 (CAL).** Un transmisor de presión da 4–20 mA (0–10 bar). Lee 12 mA. ¿Presión? ¿Qué voltaje se obtiene sobre una resistencia de 250 Ω?

**F-B7 (C).** Diferencia entre resolución, exactitud y precisión (repetibilidad) con un ejemplo de sensor de temperatura.

**F-B8 (C).** ¿Por qué el valor 4 mA (y no 0 mA) representa el mínimo de un lazo 4–20 mA?

## Nivel intermedio

**F-I1 (CAL).** Una NTC de 10 kΩ a 25 °C con β = 3950 K mide 20 kΩ. Calcula la temperatura con la ecuación Beta: `1/T = 1/T0 + (1/β)·ln(R/R0)`.

**F-I2 (CAL).** Una señal de 700 Hz se muestrea a 1 kHz. ¿Qué frecuencia aparente verás? ¿Qué se debió hacer?

**F-I3 (CAL).** Filtro RC paso bajo con R = 10 kΩ y C = 100 nF. Calcula fc. ¿Qué pasa con una señal de 1.6 kHz?

**F-I4 (CAL).** Bus I2C a 3.3 V, 400 kHz (t_r,máx = 300 ns), capacitancia de bus 150 pF. Calcula el rango de valores de pull-up (usa I_OL = 3 mA, V_OL = 0.4 V).

**F-I5 (CAL).** Un sensor de 12 V consume 150 mA y está a 20 m del tablero (cable de cobre 0.5 mm², ρ ≈ 0.0175 Ω·mm²/m). Calcula la caída de tensión ida y vuelta.

**F-I6 (MC).** Se promedian 16 muestras independientes con ruido gaussiano. El ruido (σ) disminuye aproximadamente en un factor de:
a) 2 b) 4 c) 8 d) 16

**F-I7 (DEP).** Un sensor analógico 0–5 V conectado a un ADC de 3.3 V "satura" a partir de 3.3 V. ¿Qué haces? Calcula un divisor 10 kΩ / R2 para que 5 V → ≤ 3.0 V.

**F-I8 (CAL).** Un divisor lee la batería de 12 V (puede llegar a 15 V) con R1 = 10 kΩ y R2 = 3.3 kΩ hacia un ADC de 3.3 V. ¿Es correcto? Justifica con números y propón R2.

**F-I9 (C).** Explica qué es un lazo de tierra y cómo se mitiga en un sensor analógico de cable largo.

**F-I10 (MC).** ¿Qué valor devolverá con seguridad un DS18B20 al que se lee sin haber terminado la conversión (valor de reset)? a) 0 °C b) 25 °C c) 85 °C d) −127 °C

## Nivel avanzado

**F-A1 (DIS/CAL).** Un sensor de presión ratiométrico 0.5–4.5 V (0–10 bar) alimentado a 5 V debe leerse con un ADC de 12 bits a 3.3 V. Diseña un divisor (usa R1 = 4.7 kΩ), calcula el rango de cuentas y la resolución en mbar/LSB. Comenta las limitaciones (impedancia de la fuente, ratiometría con la alimentación).

**F-A2 (CAL).** Un regulador lineal baja 12 V a 3.3 V con carga de 200 mA. ¿Cuánta potencia disipa? ¿Qué alternativa propones?

**F-A3 (LEC).** Lee este esquema en texto y lista al menos **5 problemas**:
```
J1: +12V ---- U1 (regulador lineal 7805) ---- +5V
+5V ---- MCU (ESP32, Vdd = 3.3 V)  y  sensor I2C (3.3 V)
SDA, SCL: MCU <-> sensor, pull-ups de 10 k a +5V
1-Wire DS18B20: DQ al GPIO4 del ESP32, sin resistencia, VDD y GND del sensor unidos a GND (modo parásito)
Cable de 15 m del sensor de temperatura, cable de 2 hilos sin trenzar, paralelo a cables de potencia del motor
CAN: MCU CAN_TX/CAN_RX ---- CANH/CANL directo (sin transceptor), 120 ohm en cada nodo (3 nodos)
Sin fusible ni protección contra polaridad inversa en J1
```

**F-A4 (DIS).** Diseña la adquisición de temperatura de un motor con 3 puntos de medición, cable de 12 m en un entorno ruidoso. Elige sensor(es), interfaz, protecciones, muestreo, validación y qué enviarías al gateway. Justifica.

**F-A5 (CAL).** Un acelerómetro se muestrea a 10 kHz. ¿Cuál es la frecuencia máxima observable sin aliasing? Una componente real de 7 kHz, ¿en qué frecuencia aparece? ¿Cómo lo evitarías?

**F-A6 (CAL).** Convierte los datos crudos de un DS18B20: `0x0191`, `0xFF5E`, `0x07D0`, `0xFC90` (16 bits, complemento a 2, 1/16 °C).

**F-A7 (C).** Un cliente pregunta "¿un ADC de 16 bits es más exacto que uno de 12 bits?". Responde de forma completa.
