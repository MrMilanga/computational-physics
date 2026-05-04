import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import PillowWriter
from matplotlib import _cm
import numba
from numba import jit

#Defino Condiciones de borde
edge = np.linspace (-1,1,100) #va desde -1 a 1 y hay 100 numeros entre los enteros
xv,yv= np.meshgrid(edge,edge) #esto es las dimensiones de mi grilla
upper_y=9
upper_x=10
lower_x=5
lower_y=5


#hago el potencial
@numba.jit("f8[:,:](f8[:,:], i8)", nopython=True, nogil=True)#nopython no gil es que se ejecute sin usar al interprete para mejorar el rendimiento
def compute_potential(potencial, n_iter):
    length = len(potencial[0])
    for n in range(n_iter):
        for i in range(1, length-1):
            for j in range(1, length-1):
                potencial[j][i] = 1/4 * (potencial[j+1][i] + potencial[j-1][i] + potencial[j][i+1] + potencial[j][i-1])
    return potencial


#defino un bloque

def potential_block(x, y):
    return np.select([(x>-0.25)*(x<0.25)*(y>-0.25)*(y<0.25),
                      (x<=-0.25)+(x>=0.25)+(y<=-0.25)+(y>=0.25)],
                     [1.,
                      0])
#esto dice que si estoy en esos contornos, el potencial es 1 y si no estoy ahi es 0

fixed = potential_block(xv,yv)
fixed_bool = fixed!=0
# le digo que mi bloque es constante (o sea me queda todo false y en el bloque true)
plt.contourf(fixed)

@numba.jit("f8[:,:](f8[:,:], b1[:,:], i8)", nopython=True, nogil=True)
def compute_potential(potencial, fixed_bool, n_iter):
    length = len(potencial[0])
    for n in range(n_iter):
        for i in range(1, length-1):
            for j in range(1, length-1):
                if not(fixed_bool[j][i]):# le digo que si no es el fix, que haga la funcion,sino no
                    potencial[j][i] = 1/4 * (potencial[j+1][i] + potencial[j-1][i] + potencial[j][i+1] + potencial[j][i-1])
    return potencial

#Ubico mis condiciones de borde
potencial = np.zeros((100,100))
potencial[:,-1]=lower_y
potencial[:, 0]=upper_y
potencial[0,:]=upper_x
potencial[-1,:]=lower_x
potencial[fixed_bool] = 0
potencial = compute_potential(potencial, fixed_bool, n_iter=2000)

#grafico en 2D
fig, ax = plt.subplots(1, 1, figsize=(8,6))
clr_plot = ax.contourf(xv, yv, potencial,30)
ax.set_xlabel('x')
ax.set_ylabel('y')
fig.colorbar(clr_plot, label='V')
plt.show() 

#grafico en 3D
fig=plt.figure()
ax=plt.subplot(111,projection="3d")
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("V")
ax.plot_wireframe(xv,yv,potencial)
plt.show()
