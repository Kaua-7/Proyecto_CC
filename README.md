# 🚀 Proyecto Grupo 9

Repositorio con los códigos y recursos del **Proyecto del Grupo 9**, formado por **Jan Fernández**, **Kaua Vieira** e **Ingrid Rojano**. El proyecto simula y monitoriza un satélite con sensores, comunicación inalámbrica, estación de tierra e interfaz gráfica con visualización avanzada.

---

## 📌 Estado del proyecto

* **Última versión publicada:** v3
* **Funciones descritas a continuación:** v4 (en desarrollo / próxima publicación)

---

##  Índice

1. [Arquitectura general](#-arquitectura-general)
2. [Funciones – Versión 4](#-funciones--versión-4)

   * [Arduino satélite](#arduino-satélite)
   * [Estación de tierra](#estación-de-tierra)
   * [Interfaz gráfica](#interfaz-gráfica)
3. [Registro y trazabilidad](#-registro-y-trazabilidad)
4. [Simulación orbital](#-simulación-orbital)
5. [Vídeos del proyecto](#-vídeos-del-proyecto)

---

##  Arquitectura general

El sistema está dividido en **tres bloques principales**:

* **Satélite (Arduino):** Captura datos ambientales y de distancia, los procesa y los envía inalámbricamente.
* **Estación de tierra:** Recibe los datos, valida la comunicación y actúa como puente hacia la interfaz gráfica.
* **Interfaz gráfica (Python):** Visualiza los datos, permite la interacción del usuario y gestiona alarmas y registros.

---

##  Funciones – Versión 4

###  Arduino satélite

1.  **Adquisición de datos**

   * Temperatura y humedad mediante sensor **DHT**.
   * Medición de distancia con **sensor de ultrasonidos**, montado sobre un **servomotor** en movimiento.

2.  **Integridad de datos**

   * Implementación de un **checksum**, que permite detectar y descartar mensajes corruptos durante la transmisión.

3.  **Comunicación inalámbrica**

   * Enlace estable entre el satélite y la estación de tierra.

---

###  Estación de tierra

1.  **Indicadores LED**

   * **LED verde:** Parpadea cada vez que se reciben datos correctamente.
   * **LED rojo:** Se activa en caso de fallo de comunicación, deshabilitando el LED verde.
   * **LED blanco:** Se activa en caso de fallo en el DHT.
   * **LED verde:** Se activa en caso de fallo en el sensor de ultrasonido.

2.  **Gestión de recepción**

   * Validación de mensajes recibidos antes de enviarlos a la interfaz gráfica.

3.  **Alarma de distancia**

   * LCD1602 en el cual aparece el mensaje de amenaza cuando el sensor de ultrasonidos detecta un objeto a menos de 50 cm.
     

---

###  Interfaz gráfica

1.  **Visualización de datos**

   * Recepción de datos desde la estación de tierra.
   * Representación gráfica en tiempo real.

2.  **Gráficas incluidas**

   * Evolución de la **temperatura**.
   * **Media de temperatura**.
   * Evolución de la **humedad**.

3.  **Control por parte del usuario**
   El usuario puede configurar:

   * Intervalo de envío de datos.
   * Número de valores usados para la media de temperatura.
   * Cálculo de la media en **Arduino** o en **Python**.
   * Umbral máximo de temperatura.

     **Sistema de alarma:**

   * Si las **tres últimas medias** superan el valor máximo configurado, se activa una alarma en pantalla.

4.  **Control del servomotor**

   * Barrido continuo.
   * Posicionamiento en un ángulo específico definido por el usuario.

---

##  Registro y trazabilidad

El sistema incluye un **fichero de registro (log)** que almacena:

* Datos recibidos.
* Errores de comunicación.
* Cambios realizados por el usuario.
* Observaciones manuales.

Cada evento queda registrado junto con su **fecha y hora**, garantizando trazabilidad completa del sistema.

---

##  Simulación orbital

* Simulación **3D** del período orbital del satélite alrededor de la Tierra.
* Visualización del satélite desplazándose sobre un mapa mundi en 2D, siguiendo un movimiento sinusoidal que simula su paso orbital sobre la superficie terrestre.

---

##  Vídeos del proyecto

* ▶️ **Versión 1**
* ▶️ **Versión 2**
* ▶️ **Versión 3**
* ▶️ **Versión 4**

---


