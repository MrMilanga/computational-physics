import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib.animation import PillowWriter

from scipy.linalg import eigh_tridiagonal

plt.style.use("dark_background")
#fdtd
Nx = 301
Nt = 100000
dx = 1/(Nx-1)
dt= 1e-7
x = np.linspace(0, 1, Nx)
psi0 = np.sqrt(2)*np.sin(np.pi*x)

V = -10000*np.exp(-(10*x-5)**2)

plt.figure(figsize=(8,3))
plt.plot(x,V)
plt.title("$1000exp(-(10x-5)^2)$")
plt.xlabel("x",fontsize=20)
plt.ylabel("v",fontsize=20)
plt.grid()
plt.show()


psi = np.zeros([Nt,Nx])
psi[0] = psi0
def compute_psi(psi):
    for t in range(0, Nt-1):
        dtau = 1j * dt
        for i in range(1, Nx-1):
            a = (1 - (dtau / 2) * V[i]) / (1 + (dtau / 2) * V[i])
            b = 1 / (1 + (dtau / 2) * V[i])
            d = dtau / (2 * (dx) ** 2)
            psi[t + 1][i] = a * psi[t][i] + b * d * (psi[t][i + 1] - 2 * psi[t][i] + psi[t][i - 1])
        
        normal = np.sum(np.absolute(psi[t+1])**2)*dx
        #print(normal)
        for i in range(1, Nx-1):
            psi[t+1][i] = psi[t+1][i]/normal
        
    return psi

psi_m1 = compute_psi(psi.astype(complex))

#Matriz
Nx = 301
dx = 1/(Nx-1)
x = np.linspace(0, 1, Nx)
psi0 = np.sqrt(2)*np.sin(np.pi*x)

def V(x):
    return -10000*np.exp(-(10*x-5)**2)
d = 1/dx**2 + V(x)[1:-1] 
e = -1/(2*dx**2) * np.ones(len(d)-1)
w, v = eigh_tridiagonal(d, e)
E_js = w[0:70]
psi_js = np.pad(v.T[0:70], [(0, 0), (1, 1)], mode="constant")
cs = np.dot(psi_js, psi0)
def psi_m2(t):
    return psi_js.T@(cs*np.exp(-1j*E_js*t))

print(np.arange(0, 70, 1), w[0:70])
#plt.scatter(np.arange(0, 70, 1), w[0:70])

def animate(i):
    ln1.set_data(x, np.absolute(psi_m1[100*i])**2)
    ln2.set_data(x, np.absolute(psi_m2(100*i*dt))**2)

fig, ax = plt.subplots(1,1, figsize=(8,4))
#ax.grid()
ln1, = plt.plot([], [], "r-", lw=2, markersize=8, label="Metodo fdtd")
ln2, = plt.plot([], [], "b--", lw=3, markersize=8, label="Metodo de las matrices")
ax.set_ylim(-1,20)
ax.set_xlim(0,1)
ax.set_ylabel("$|\psi(x)|^2$", fontsize=20)
ax.set_xlabel("$x$", fontsize=20)
ax.legend(loc="upper left")
ax.set_title("$Densidad  de  Probabilidades$",fontsize=20)
plt.tight_layout()
ani = animation.FuncAnimation(fig, animate, frames=1000, interval=50)
ani.save("animacion.gif",writer="pillow",fps=50,dpi=100)

