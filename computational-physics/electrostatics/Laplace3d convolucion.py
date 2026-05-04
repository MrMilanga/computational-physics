import numpy as np
import matplotlib.pyplot as plt
plt.style.use(['classic'])
from scipy.ndimage import convolve, generate_binary_structure
from matplotlib import _cm

#Hago como una grilla en 3D de 100x100x100
N=100
grid = np.zeros((N,N,N))+0.5

grid[30:70,30:70,20] = 1
grid[30:70,30:70,80] = 0
grid[:,:,0]=0
grid[:,:,99]=1
grid[:,0,:]=0
grid[:,99,:]=0
mask_pos = grid==1
mask_neg = grid==0
yv, xv, zv = np.meshgrid(np.arange(N),np.arange(N),np.arange(N))

kern = generate_binary_structure(3,1).astype(float)/6
kern[1,1,1] = 0


#con esta funcion lo que hago es actualizar la grilla
iters = 1000
for i in range(iters):
    grid_updated = convolve(grid,kern, mode='constant')

    # Condiciones de borde
    grid_updated[mask_pos] = 1
    grid_updated[mask_neg] = 0
    # error de la grilla actualizada
    grid = grid_updated

slc = 40
#grafico en 2D visto desde el eje X

plt.figure(figsize=(8,6))
CS = plt.contour(np.arange(100)/100, np.arange(100)/100, grid[slc],50)
plt.clabel(CS, CS.levels, inline=True, fontsize=6)
plt.xlabel('z')
plt.ylabel('y')
plt.axvline(0.2, ymin=0.3, ymax=0.7, color='r')
plt.axvline(0.8, ymin=0.3, ymax=0.7, color='b')
plt.colorbar(CS, label='V/Vo')
plt.show()
