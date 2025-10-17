import serial
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import *

device = 'COM4'
mySerial = serial.Serial(device, 9600, timeout=1)

temperaturas = []
humedades = []
eje_x = []
i = 0
lectura_activa = False

window = Tk()
window.title("Ground Station - Doble gráfica")
window.geometry("900x600")

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6, 6))
fig.tight_layout(pad=4)

line_temp, = ax1.plot([], [], '-o', color='red', label="Temperatura (°C)")
ax1.set_xlabel("Muestras")
ax1.set_ylabel("Temperatura (°C)")
ax1.set_title("Evolución de la Temperatura")
ax1.grid(True)
ax1.legend()

line_hum, = ax2.plot([], [], '-s', color='blue', label="Humedad (%)")
ax2.set_xlabel("Muestras")
ax2.set_ylabel("Humedad (%)")
ax2.set_title("Evolución de la Humedad")
ax2.grid(True)
ax2.legend()

canvas = FigureCanvasTkAgg(fig, master=window)
canvas.draw()
canvas.get_tk_widget().grid(row=0, column=0, rowspan=4, padx=10, pady=10)

def actualizar_graficas():
    """Actualiza las dos gráficas con los nuevos datos."""
    line_temp.set_data(eje_x, temperaturas)
    line_hum.set_data(eje_x, humedades)

    ax1.relim()
    ax1.autoscale_view()
    ax2.relim()
    ax2.autoscale_view()

    canvas.draw_idle() 


def leer_serial():
    """Lee una línea del puerto serie."""
    global i
    if mySerial.in_waiting > 0:
        line = mySerial.readline().decode('utf-8').rstrip()
        print(line)
        trozos = line.split(':')

        
        if len(trozos) >= 4 and trozos[0] == 'T' and trozos[2] == 'H':
            try:
                temperatura = float(trozos[1])
                humedad = float(trozos[3])
            except ValueError:
                return

            eje_x.append(i)
            temperaturas.append(temperatura)
            humedades.append(humedad)
            i += 1
            actualizar_graficas()
        else:
            print("Formato no válido:", line)


def ciclo_lectura():
    """Se ejecuta periódicamente mientras la lectura está activa."""
    if lectura_activa:
        leer_serial()
        window.after(500, ciclo_lectura)  


def IniciarClick():
    """Botón para iniciar la recepción."""
    global lectura_activa
    lectura_activa = True
    mySerial.write(b'Iniciar')
    print("Transmisión iniciada.")
    ciclo_lectura()


def PararClick():
    """Botón para detener la recepción."""
    global lectura_activa
    lectura_activa = False
    mySerial.write(b'Parar')
    print("Transmisión detenida.")


def ReanudarClick():
    """Botón para reanudar la recepción."""
    global lectura_activa
    lectura_activa = True
    mySerial.write(b'Iniciar')
    print("Transmisión reanudada.")
    ciclo_lectura()



tituloLabel = Label(window, text="Ground Station", font=("Courier", 25, "italic"))
tituloLabel.grid(row=0, column=1, padx=10, pady=10, sticky=N)

IniciarButton = Button(window, text="Iniciar", bg='green', fg="white", command=IniciarClick, width=15, height=2)
IniciarButton.grid(row=1, column=1, padx=10, pady=10)

PararButton = Button(window, text="Parar", bg='red', fg="white", command=PararClick, width=15, height=2)
PararButton.grid(row=2, column=1, padx=10, pady=10)

ReanudarButton = Button(window, text="Reanudar", bg='yellow', fg="black", command=ReanudarClick, width=15, height=2)
ReanudarButton.grid(row=3, column=1, padx=10, pady=10)


def on_close():
    global lectura_activa
    lectura_activa = False
    mySerial.close()
    print("Puerto serie cerrado.")
    window.destroy()

window.protocol("WM_DELETE_WINDOW", on_close)


window.mainloop()


