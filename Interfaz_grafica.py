import serial
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import *

# =========================
# CONFIGURACIÓN DEL PUERTO SERIE
# =========================
device = 'COM4'  # Puerto serie donde está conectado el Arduino
mySerial = serial.Serial(device, 9600, timeout=1)  # Inicializa la comunicación serial

# =========================
# VARIABLES PARA ALMACENAR DATOS
# =========================
temperaturas = []  # Lista para guardar los valores de temperatura
humedades = []     # Lista para guardar los valores de humedad
eje_x = []         # Eje X (número de muestras)
i = 0              # Contador de muestras
lectura_activa = False  # Bandera que indica si la lectura está activa

# =========================
# CONFIGURACIÓN DE LA INTERFAZ GRÁFICA
# =========================
window = Tk()  # Crear la ventana principal
window.title("Ground Station - Doble gráfica")
window.geometry("900x600")  # Tamaño de la ventana

# Crear una figura con 2 subgráficas (una para temperatura y otra para humedad)
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6, 6))
fig.tight_layout(pad=4)  # Ajusta los espacios entre las gráficas

# --- Gráfica de temperatura ---
line_temp, = ax1.plot([], [], '-o', color='red', label="Temperatura (°C)")
ax1.set_xlabel("Muestras")
ax1.set_ylabel("Temperatura (°C)")
ax1.set_title("Evolución de la Temperatura")
ax1.grid(True)
ax1.legend()

# --- Gráfica de humedad ---
line_hum, = ax2.plot([], [], '-s', color='blue', label="Humedad (%)")
ax2.set_xlabel("Muestras")
ax2.set_ylabel("Humedad (%)")
ax2.set_title("Evolución de la Humedad")
ax2.grid(True)
ax2.legend()

# Embebe la figura de Matplotlib dentro de la ventana Tkinter
canvas = FigureCanvasTkAgg(fig, master=window)
canvas.draw()
canvas.get_tk_widget().grid(row=0, column=0, rowspan=4, padx=10, pady=10)

# =========================
# FUNCIONES DE ACTUALIZACIÓN DE GRÁFICAS
# =========================
def actualizar_graficas():
    """Actualiza las dos gráficas con los datos más recientes."""
    line_temp.set_data(eje_x, temperaturas)  # Actualiza línea de temperatura
    line_hum.set_data(eje_x, humedades)      # Actualiza línea de humedad

    # Ajusta automáticamente los límites de los ejes según los datos
    ax1.relim()
    ax1.autoscale_view()
    ax2.relim()
    ax2.autoscale_view()

    canvas.draw_idle()  # Refresca el canvas incrustado en la interfaz

# =========================
# FUNCIONES DE LECTURA SERIAL
# =========================
def leer_serial():
    """Lee una línea del puerto serie y procesa los datos."""
    global i
    if mySerial.in_waiting > 0:  # Si hay datos disponibles
        line = mySerial.readline().decode('utf-8').rstrip()  # Leer y limpiar la línea
        print(line)  # Mostrar en consola
        trozos = line.split(':')  # Separar datos por los ':' enviados desde Arduino

        # Comprueba que el formato sea correcto: T:valor:H:valor
        if len(trozos) >= 4 and trozos[0] == 'T' and trozos[2] == 'H':
            try:
                temperatura = float(trozos[1])
                humedad = float(trozos[3])
            except ValueError:
                return  # Si no se puede convertir a float, ignorar la línea

            # Guardar datos en las listas
            eje_x.append(i)
            temperaturas.append(temperatura)
            humedades.append(humedad)
            i += 1

            actualizar_graficas()  # Actualizar la gráfica con los nuevos datos
        else:
            print("Formato no válido:", line)

# =========================
# CICLO PERIÓDICO DE LECTURA
# =========================
def ciclo_lectura():
    """Se ejecuta periódicamente mientras lectura_activa sea True."""
    if lectura_activa:
        leer_serial()  # Llamar a la función de lectura
        window.after(500, ciclo_lectura)  # Repetir cada 500 ms

# =========================
# FUNCIONES DE BOTONES
# =========================
def IniciarClick():
    """Botón para iniciar la recepción de datos."""
    global lectura_activa
    lectura_activa = True
    mySerial.write(b'Iniciar')  # Enviar comando al Arduino
    print("Transmisión iniciada.")
    ciclo_lectura()  # Inicia el ciclo de lectura

def PararClick():
    """Botón para detener la recepción de datos."""
    global lectura_activa
    lectura_activa = False
    mySerial.write(b'Parar')
    print("Transmisión detenida.")

def ReanudarClick():
    """Botón para reanudar la recepción de datos."""
    global lectura_activa
    lectura_activa = True
    mySerial.write(b'Iniciar')
    print("Transmisión reanudada.")
    ciclo_lectura()

# =========================
# ELEMENTOS DE INTERFAZ (BOTONES Y TÍTULO)
# =========================
tituloLabel = Label(window, text="Ground Station", font=("Courier", 25, "italic"))
tituloLabel.grid(row=0, column=1, padx=10, pady=10, sticky=N)

IniciarButton = Button(window, text="Iniciar", bg='green', fg="white", command=IniciarClick, width=15, height=2)
IniciarButton.grid(row=1, column=1, padx=10, pady=10)

PararButton = Button(window, text="Parar", bg='red', fg="white", command=PararClick, width=15, height=2)
PararButton.grid(row=2, column=1, padx=10, pady=10)

ReanudarButton = Button(window, text="Reanudar", bg='yellow', fg="black", command=ReanudarClick, width=15, height=2)
ReanudarButton.grid(row=3, column=1, padx=10, pady=10)

# =========================
# FUNCIONES DE CIERRE
# =========================
def on_close():
    """Se ejecuta al cerrar la ventana: detiene la lectura y cierra el puerto serie."""
    global lectura_activa
    lectura_activa = False
    mySerial.close()
    print("Puerto serie cerrado.")
    window.destroy()

window.protocol("WM_DELETE_WINDOW", on_close)  # Vincula el cierre de ventana a la función

# =========================
# INICIA LA INTERFAZ
# =========================
window.mainloop()  # Ejecuta el bucle principal de Tkinter
