import numpy as np 
import matplotlib.pyplot as plt 
from matplotlib.animation import FuncAnimation 
from IPython.display import HTML 

plt.style.use("dark_background") #https://matplotlib.org/stable/gallery/style_sheets/style_sheets_reference.html

h_bar = 1.0545718e-34
m=1
b=3

class Onda_Gaussiana:
    def __init__(self, N_grid, L, a, x0, k0, sigma,t):
        self.t = t
        self.L = L
        self.N_grid = N_grid
        self.x = np.linspace(0, self.L, self.N_grid + 1)
        self.dx = self.x[1] - self.x[0]

        def integral(f, axis=0):
            return np.sum(f * self.dx, axis=axis)

        self.Psi0 = 2*np.exp(-1/2 * (self.x[1:-1] - x0)**2 / sigma**2) * np.exp(1j * k0 * self.x[1:-1])
        norma = integral(np.abs(self.Psi0)**2)
        self.Psi0 = self.Psi0 / np.sqrt(norma)

        self.T = -1/2 * 1/self.dx**2 * (np.diag(-2 * np.ones(self.N_grid - 1)) + np.diag(np.ones(self.N_grid - 2), 1) + np.diag(np.ones(self.N_grid - 2), -1))

        def potencial(x):
            return -(b * h_bar**2 / (2 * m)) * (1 / np.cosh(b * x))**2
        
        self.V = np.diag(potencial(self.x[1:-1]))

        self.H = self.T + self.V

    def animacion(self):
        E, psi = np.linalg.eigh(self.H)
        psi = psi.T
        norma = self.integral(np.abs(psi)**2)
        psi = psi / np.sqrt(norma)

        c_n = np.zeros_like(psi[0], dtype=complex)
        for j in range(0, self.N_grid - 1):
            c_n[j] = self.integral(np.conj(psi[j]) * self.Psi0)

        def Psi(t):
            return psi.T @ (c_n * np.exp(-1j * E * t))
        
        def animate(t):
            y1 = np.real(Psi(t))
            y2 = np.imag(Psi(t))
            line1.set_data(self.x[1:-1], y1)
            line2.set_data(self.x[1:-1], y2)
            return (line1, line2)
        
        def init():
            line1.set_data([], [])
            line2.set_data([], [])
            return (line1, line2)
        
        fig = plt.figure(figsize=(20, 12))
        ax = plt.axes(xlim=(0, self.L), ylim=(-0.25, 0.25))
        line, = ax.plot([], [], lw=2)
        ax.plot(self.x[1:-1], self.V, label="Potencial",color="green")
        ax.set_title("Paquete de onda Gaussiano", fontsize=20)
        line1, = ax.plot(self.x[1:-1], np.zeros(self.N_grid - 1), lw=2, color="red", label="Parte Real")
        line2, = ax.plot(self.x[1:-1], np.zeros(self.N_grid - 1), lw=2, color="blue", label="Parte Imaginaria")
        ax.legend(fontsize=15)
        ax.set_xlabel("X", fontsize=15)

        ani = FuncAnimation(fig, animate, frames=len(self.t), init_func=init, interval=20, blit=False)

        ani.save("animacion.gif", writer="pillow")
        return HTML(ani.to_jshtml())

    def integral(self, f, axis=0):
        return np.sum(f * self.dx, axis=axis)

    def densidad_probabilidad(self, t):
        E, psi = np.linalg.eigh(self.H)
        psi = psi.T
        norma = self.integral(np.abs(psi)**2)
        psi = psi / np.sqrt(norma)

        c_n = np.zeros_like(psi[0], dtype=complex)
        for j in range(0, self.N_grid - 1):
            c_n[j] = self.integral(np.conj(psi[j]) * self.Psi0)

        prob_densidad = np.abs(psi.T @ (c_n * np.exp(-1j * E * t)))**2
        return prob_densidad

    def calcular_norma(self):
        E, psi = np.linalg.eigh(self.H)
        psi = psi.T
        norma = self.integral(np.abs(psi)**2)
        psi = psi / np.sqrt(norma)

        c_n = np.zeros_like(psi[0], dtype=complex)
        for j in range(0, self.N_grid - 1):
            c_n[j] = self.integral(np.conj(psi[j]) * self.Psi0)

        norma_list = []
        for t in self.t:
            psi_t = psi.T @ (c_n * np.exp(-1j * E * t))
            norma_t = self.integral(np.abs(psi_t)**2)
            norma_list.append(norma_t)
        
        return np.array(norma_list)

# Crear una instancia de la clase Gaussian_Wave con dos potenciales
paquetedeonda = Onda_Gaussiana(1000, 1000, 450, 100, 0.5, 15, np.linspace(0., 3000, 1000))
# Crea una instancia de la clase gausiana con los siguientes parámetros:
# N_grid: 1000 - Número de puntos en la discretización del espacio
# L: 1000 - Longitud del espacio en el que se está simulando
# a: 450 - Posición de la pared del potencial 1
# V0: 0.1 - Altura del potencial 1
# w: 20 - Ancho de la pared del potencial 1
# x0: 100 - Posición inicial del paquete de onda 
# k0: 0.5 - Número de onda inicial
# sigma: 15 - Parámetro que controla la dispersión del paquete de onda gaussiano
#a2 : 700 posicion de la pared del potencial 2
#V0_2: 0.2 Altura del potencial 2
#w2: 20 Anchura del potencial 2
# np.linspace(0., 7100, 1500) - Un arreglo de valores de tiempo desde 0 hasta 7100 divididos en 1500 paso


# Generar y mostrar la animación de la función de onda
Psi = paquetedeonda.animacion()

# Generar un gráfico de la densidad de probabilidad en función del tiempo
fig = plt.figure(figsize=(12, 6))
ax = plt.axes(xlim=(0, paquetedeonda.L), ylim=(0, 0.07))
line, = ax.plot(paquetedeonda.x[1:-1], paquetedeonda.densidad_probabilidad(paquetedeonda.t[0]), lw=2)
ax.set_title("Densidad de Probabilidad en función del tiempo", fontsize=15)
ax.set_xlabel("X", fontsize=12)
ax.set_ylabel("Densidad de Probabilidad", fontsize=12)

def animate(t):
    prob_densidad = paquetedeonda.densidad_probabilidad(t)
    line.set_data(paquetedeonda.x[1:-1], prob_densidad)
    return line

def inic():
    line.set_data([], [])
    return line

ani = FuncAnimation(fig, animate, frames=len(paquetedeonda.t), init_func=inic, interval=20, blit=False)

ani.save("densidad de probabilidad.gif", writer="pillow")

# Generar un gráfico de la norma en función del tiempo
Valor_norma = paquetedeonda.calcular_norma()
fig_norma = plt.figure(figsize=(12, 6))
ax_norma = plt.axes(xlim=(0, max(paquetedeonda.t)), ylim=(min(Valor_norma) - 0.005, max(Valor_norma) + 0.005))
line_norma, = ax_norma.plot(paquetedeonda.t, Valor_norma, lw=2)
ax_norma.set_title("Norma en función del tiempo", fontsize=15)
ax_norma.set_xlabel('Tiempo', fontsize=12)
ax_norma.set_ylabel('Norma', fontsize=12)
#ax_norma = plt.axes(xlim=(0, max(paquetedeonda.t)), ylim=(min(Valor_norma), max(Valor_norma)))
plt.show()

