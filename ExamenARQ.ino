#include <Arduino.h>

// Definición de pines
const int ledRojo = 12;
const int ledVerde = 14;
const int ledAmarillo = 27;
const int botonInicio = 33;
const int botonDetener = 32;
const int ledIndicador = 2;

// Variables de estado
bool semaforoActivo = false;
bool detenerSemaforo = false;
unsigned long tiempoAnterior = 0;
int estadoSemaforo = 0;
unsigned long intervalo = 0;

// Variables para el LED indicador
unsigned long tiempoAnteriorIndicador = 0;
bool estadoIndicador = false;
int parpadeosIndicador = 0;

void setup() {
  // Configuración de pines
  pinMode(ledRojo, OUTPUT);
  pinMode(ledVerde, OUTPUT);
  pinMode(ledAmarillo, OUTPUT);
  pinMode(botonInicio, INPUT_PULLUP);
  pinMode(botonDetener, INPUT_PULLUP);
  pinMode(ledIndicador, OUTPUT);

  // Inicialización del monitor serie
  Serial.begin(115200);
}

void loop() {
  // Verificar si se presiona el botón de inicio
  if (digitalRead(botonInicio) == LOW) {
    semaforoActivo = true;
    detenerSemaforo = false;
    tiempoAnterior = millis();
  }

  // Verificar si se presiona el botón de detener
  if (digitalRead(botonDetener) == LOW) {
    detenerSemaforo = true;
  }

  // Secuencia del semáforo usando millis()
  if (semaforoActivo && !detenerSemaforo) {
    unsigned long tiempoActual = millis();
    switch (estadoSemaforo) {
      case 0: // Rojo
        if (tiempoActual - tiempoAnterior >= 12000) {
          digitalWrite(ledRojo, LOW);
          estadoSemaforo = 1;
          tiempoAnterior = tiempoActual;
        } else {
          digitalWrite(ledRojo, HIGH);
          Serial.println("LED Rojo encendido");
        }
        break;
      case 1: // Verde
        if (tiempoActual - tiempoAnterior >= 9000) {
          digitalWrite(ledVerde, LOW);
          estadoSemaforo = 2;
          tiempoAnterior = tiempoActual;
        } else {
          digitalWrite(ledVerde, HIGH);
          Serial.println("LED Verde encendido");
        }
        break;
      case 2: // Amarillo (parpadeo)
        if (tiempoActual - tiempoAnterior >= 3000) {
          digitalWrite(ledAmarillo, LOW);
          estadoSemaforo = 0;
          tiempoAnterior = tiempoActual;
        } else {
          if ((tiempoActual - tiempoAnterior) % 1000 < 500) {
            digitalWrite(ledAmarillo, HIGH);
            Serial.println("LED Amarillo encendido");
          } else {
            digitalWrite(ledAmarillo, LOW);
            Serial.println("LED Amarillo apagado");
          }
        }
        break;
    }
  }

  // Indicador de operación del sistema usando millis()
  unsigned long tiempoActualIndicador = millis();
  if (tiempoActualIndicador - tiempoAnteriorIndicador >= (estadoIndicador ? 600 : 400)) {
    estadoIndicador = !estadoIndicador;
    digitalWrite(ledIndicador, estadoIndicador);
    tiempoAnteriorIndicador = tiempoActualIndicador;
    if (!estadoIndicador) {
      parpadeosIndicador++;
      if (parpadeosIndicador >= 3) {
        tiempoAnteriorIndicador += 2000; // Añadir 2 segundos de espera
        parpadeosIndicador = 0;
      }
    }
  }
}