import numpy as np
import matplotlib.pyplot as plt

# Generar una señal de ejemplo
t = np.linspace(0, 1, 1000)  # Vector de tiempo
f = 5  # Frecuencia de la señal
signal = np.sin(2 * np.pi * f * t) +np.cos(3*np.pi*f*t) #Acaba escribo la señal, esto puede ser un coseno, un seno, la suma,etc
# Calcular la Transformada de Fourier
fourier = np.fft.fft(signal)

# Calcular las frecuencias correspondientes
frequencies = np.fft.fftfreq(len(signal), t[1] - t[0])

# Graficar la señal original y su Transformada de Fourier
fig, axs = plt.subplots(2, 1)

axs[0].plot(t, signal)
axs[0].set_xlabel('Tiempo')
axs[0].set_ylabel('Señal')
axs[0].set_title('Señal original')

axs[1].plot(frequencies, np.abs(fourier))
axs[1].set_xlabel('Frecuencia')
axs[1].set_ylabel('Amplitud')
axs[1].set_title('Transformada de Fourier')

plt.tight_layout()
plt.show()