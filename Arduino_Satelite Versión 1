
//ARDUINO SATELITE
#include <SoftwareSerial.h>
#include <DHT.h>

#define DHTPIN 2
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

const int led1 = 13;

SoftwareSerial mySerial(10, 11);

bool transmitiendo = false;
unsigned long lastMillis = 0;
const unsigned long intervalo = 3000; // 3 segundos entre lecturas

// Variables de control del fallo del sensor
bool esperandoTimeout = false;
unsigned long nextTimeoutHT = 0;

// Para control del intervalo de envío
unsigned long nextHT = 0;

void setup() {
  pinMode(led1, OUTPUT);
  dht.begin();
  Serial.begin(9600);
  mySerial.begin(9600);
}

void loop() {
  // Escucha los comandos del puerto serie
  if (mySerial.available()) {
    String data = mySerial.readStringUntil('\n');
    data.trim();
    if (data == "Iniciar") transmitiendo = true;
    if (data == "Parar") transmitiendo = false;
  }

  // Si estamos transmitiendo y ha pasado el tiempo de intervalo
  if (transmitiendo && millis() >= nextHT) {
    nextHT = millis() + intervalo;

    float h = dht.readHumidity();
    float t = dht.readTemperature();

    // Si hay error en la lectura del DHT
    if (isnan(h) || isnan(t)) {
      if (!esperandoTimeout) {  // Comienza a contar tiempo de fallo
        esperandoTimeout = true;
        nextTimeoutHT = millis() + 5000; // 5 segundos de espera
      }

      // Si pasan 5 segundos y sigue fallando
      if (esperandoTimeout && (millis() >= nextTimeoutHT)) {
        mySerial.println("Fallo");
        esperandoTimeout = false; // Resetea el estado
      }
    }
    else {
      // Lectura válida: envía datos y resetea el control de fallo
      esperandoTimeout = false;

      mySerial.print("T:");
      mySerial.print(t);
      mySerial.print(":H:");
      mySerial.println(h);

      // Enciende LED para indicar envío
      digitalWrite(led1, HIGH);
      delay(200);
      digitalWrite(led1, LOW);
    }
  }
}
