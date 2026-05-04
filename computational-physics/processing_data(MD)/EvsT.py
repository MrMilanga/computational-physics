import re
import numpy as np
import matplotlib.pyplot as plt

# Abrir archivo y leer líneas
with open("salida.txt", "r") as f:
    lines = f.readlines()

# Regex para encontrar líneas con T y E
#Defino una expresion regular para tener las lineas con el formato que quiero
#Es decir t=un real y E= otro real
pattern = re.compile(r"T=\s*(\d+)\.\s*E=\s*([-\.\dE+]+)")

#T=\s*: Busca el texto T= seguido de cualquier cantidad de espacios.
#(\d+): Captura un número entero (la temperatura).
#\.: El punto decimal que separa entero y decimales (lo descarta del número de temperatura).
#\s*E=\s*: Busca el texto E= rodeado de espacios.
#([-\.\dE+]+): Captura la energía en notación científica, por ejemplo -.75813413E+03


# Listas vacias para guardar T y E
T_vals = []
E_vals = []

# Extraer datos (Recorro las lienas y busco si tengo el patron que defini)
for line in lines:
    match = pattern.search(line)
    if match:
        T = float(match.group(1)) #Extraigo los valores que quiero
        E = float(match.group(2))
        T_vals.append(T) #Lo guardo
        E_vals.append(E)

# Guardar en archivo
with open("E_vs_T.dat", "w") as f:
    for T, E in zip(T_vals, E_vals):
        f.write(f"{T} {E}\n")

# Graficar
plt.figure(figsize=(8, 5))
plt.plot(T_vals, E_vals, marker='o', linestyle='-')
plt.xlabel("Temperatura T")
plt.ylabel("Energía total E")
plt.title("Gráfico de E vs T")
plt.grid(True)
plt.tight_layout()
plt.savefig("E_vs_T.png")
plt.show()
