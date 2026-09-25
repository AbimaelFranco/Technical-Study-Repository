// 01_sensor_classes.cpp
// Diferencias practicas entre C y C++ aplicadas a sensores:
//   - clases con constructor y encapsulamiento
//   - referencias (const T&) en lugar de punteros
//   - std::optional para "lectura no disponible" (C++17) en vez de valores magicos como -127
//   - plantilla RingBuffer<T, N> con memoria estatica (sin heap) y std::array
//   - RAII: el destructor libera recursos automaticamente
//
// Compilar y ejecutar en PC (C++17):
//   g++ -std=c++17 -Wall -Wextra -o sensors 01_sensor_classes.cpp && ./sensors
//
// Nota embebida: en firmware muchos proyectos desactivan excepciones y RTTI
// (-fno-exceptions -fno-rtti) y evitan std::vector/new en el lazo principal (fragmentacion del heap).
#include <array>
#include <cstddef>
#include <cstdint>
#include <iostream>
#include <optional>
#include <string>
#include <utility>

// ---- Plantilla de buffer circular con memoria fija (equivalente C++ de 02_circular_buffer.c) ----
template <typename T, std::size_t N>
class RingBuffer {
public:
    void push(const T& v) {           // const T&: evita copiar objetos grandes
        data_[head_] = v;
        head_ = (head_ + 1) % N;
        if (count_ == N) tail_ = (tail_ + 1) % N; else ++count_;
    }
    std::optional<T> pop() {          // optional: vacio = no hay dato (sin "valores magicos")
        if (count_ == 0) return std::nullopt;
        T v = data_[tail_];
        tail_ = (tail_ + 1) % N;
        --count_;
        return v;
    }
    std::size_t size() const { return count_; }   // const: no modifica el objeto
private:
    std::array<T, N> data_{};         // almacenamiento estatico
    std::size_t head_ = 0, tail_ = 0, count_ = 0;
};

// ---- Clase base de sensor con validacion ----
class TemperatureSensor {
public:
    TemperatureSensor(std::string name, float min_valid, float max_valid)
        : name_(std::move(name)), min_(min_valid), max_(max_valid) {}

    // Valida el crudo y devuelve un valor solo si es plausible.
    std::optional<float> accept(float raw) const {
        if (raw != raw) return std::nullopt;                  // NaN != NaN
        if (raw < min_ || raw > max_) return std::nullopt;    // fuera de rango
        return raw;
    }
    const std::string& name() const { return name_; }         // devuelve referencia const: sin copia
private:
    std::string name_;
    float min_, max_;
};

// ---- RAII: guarda un "recurso" (aqui solo imprime; en la vida real seria un fd/puerto serial) ----
class PortGuard {
public:
    explicit PortGuard(const char* n) : name_(n) { std::cout << "abre " << name_ << "\n"; }
    ~PortGuard() { std::cout << "cierra " << name_ << "\n"; }   // se ejecuta aunque haya return temprano o excepcion
    PortGuard(const PortGuard&) = delete;                       // evita copiar el recurso
    PortGuard& operator=(const PortGuard&) = delete;
private:
    const char* name_;
};

// ---- Paso por valor vs referencia ----
void by_value(int x)     { x = 99; (void)x; }   // modifica una copia (el original no cambia)
void by_ref(int& x)      { x = 99; }   // modifica el original
void by_ptr(int* x)      { if (x) *x = 99; }  // puntero: puede ser nullptr, validar

int main() {
    PortGuard port("/dev/ttyUSB0");

    TemperatureSensor motor("motor", -40.0f, 150.0f);
    RingBuffer<float, 3> history;

    for (float raw : {78.0f, -127.0f, 91.5f, 400.0f, 93.0f, 95.0f}) {
        if (auto v = motor.accept(raw)) history.push(*v);
        else std::cout << motor.name() << ": descartada " << raw << "\n";
    }
    std::cout << "en historial: " << history.size() << " (capacidad 3)\n";
    while (auto v = history.pop()) std::cout << "  " << *v << "\n";

    int a = 1, b = 1, c = 1;
    by_value(a); by_ref(b); by_ptr(&c);
    std::cout << "a=" << a << " b=" << b << " c=" << c << "\n";   // a=1 b=99 c=99
    return 0;
}

/* Salida esperada:
 * abre /dev/ttyUSB0
 * motor: descartada -127
 * motor: descartada 400
 * en historial: 3 (capacidad 3)
 *   91.5
 *   93
 *   95
 * a=1 b=99 c=99
 * cierra /dev/ttyUSB0
 */
