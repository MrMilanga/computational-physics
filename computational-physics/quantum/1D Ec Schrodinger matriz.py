import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import eigh_tridiagonal
plt.style.use("dark_background")
N = 101
dx = 1/N
x = np.linspace(0, 1, N)

def V(x):
    return -(25 / np.cosh(5*x))

d = 1/dx**2 + V(x)[1:-1]
e = -1/(2*dx**2) * np.ones(len(d)-1)
w, v = eigh_tridiagonal(d, e)

plt.figure(figsize=(10,5))
plt.plot(x, V(x), lw=5,color="b")
plt.title("Potencial", fontsize=20)
plt.ylabel("$V$", fontsize=15)
plt.xlabel("$x$", fontsize=15)
plt.grid()

plt.figure(figsize=(10,5))
plt.plot(x[1:-1], v.T[0],lw=5,label= "Estado fundamental",color="b")
plt.plot(x[1:-1], v.T[1],lw=5, label= "Estado excitado 1",color="orange")
plt.plot(x[1:-1], v.T[2],lw=5,label= "Estado excitado 2",color="green")
plt.plot(x[1:-1], v.T[3],lw=5,label= "Estado excitado 3",color="red")
plt.legend(loc='upper left')
plt.title("Autoestados", fontsize=20)
plt.ylabel("$\psi$", fontsize=15)
plt.xlabel("$x$", fontsize=15)
plt.grid()


plt.figure(figsize=(10,5))
plt.plot(x[1:-1], v.T[0]**2,lw=3,label= "Estado fundamental",color="b")
plt.plot(x[1:-1], v.T[1]**2,lw=3,label= "Estado excitado 1",color="orange")
plt.plot(x[1:-1], v.T[2]**2,lw=3,label= "Estado excitado 2",color="g")
plt.plot(x[1:-1], v.T[3]**2,lw=3,label= "Estado excitado 3",color="r")
plt.title("Densidad de Probabilidad", fontsize=20)
plt.legend(loc='upper left')
plt.ylabel("$|\psi(x)|^2$", fontsize=15)
plt.xlabel("$x$", fontsize=15)
plt.grid()
plt.show()



plt.scatter(np.arange(0, 10, 1), w[0:10],color="r")
plt.ylabel("Autovalores")
plt.xlabel("N")
plt.show()