
//ARDUINO TIERRA
#include <SoftwareSerial.h>

SoftwareSerial mySerial(10, 11); 
const int led2 = 12; // LED que parpadea al recibir datos
const int led3 = 13; // LED de alerta (Fallo o sin comunicación)

// Variable para controlar el timeout
unsigned long ultimoMensaje = 0;
const unsigned long timeout = 5000; // 5 segundos

void setup() {
  pinMode(led2, OUTPUT);
  pinMode(led3, OUTPUT);
  Serial.begin(9600);
  mySerial.begin(9600);
  mySerial.println("Empezamos");
  ultimoMensaje = millis(); // inicia el contador
}

void loop() {
  // Si llegan datos desde el satélite
  if (mySerial.available()) {
    String data = mySerial.readStringUntil('\n');
    data.trim(); // elimina espacios y saltos de línea
    Serial.println(data);

    // Actualiza el tiempo del último mensaje recibido
    ultimoMensaje = millis();

    // 🔹 LED indicador de recepción
    digitalWrite(led2, HIGH);
    delay(200);
    digitalWrite(led2, LOW);

    // 🔸 Si se recibe "Fallo", activar la alerta
    if (data == "Fallo") {
      digitalWrite(led3, HIGH);
      Serial.println("Error de la lectura de temperatura y humedad");
    } else {
      // Si el mensaje es válido, apaga alerta (si estaba encendida)
      digitalWrite(led3, LOW);
    }
  }

  // 🕒 Comprobación del timeout (falta de comunicación)
  if (millis() - ultimoMensaje > timeout) {
    digitalWrite(led3, HIGH); // enciende luz de alerta
    Serial.println("⚠️  Sin comunicación con el satélite");
  }

  // Si se mandan datos desde el monitor serie
  if (Serial.available()) {
    String data = Serial.readStringUntil('\n');
    mySerial.println(data);
  }
}

