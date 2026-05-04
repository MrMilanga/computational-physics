import re
import numpy as np
import matplotlib.pyplot as plt

with open("salida.txt", "r") as f:
    lines = f.readlines()

pattern = re.compile(r"^\s*(\d+)\s+T=\s*\d+\.\s*E=\s*([-\.\dE+]+)")

steps = []
E_vals = []

for line in lines:
    match = pattern.search(line)
    if match:
        step = int(match.group(1))
        E = float(match.group(2))
        
        steps.append(step)
        E_vals.append(E)

# Guardar
with open("E_vs_steps.dat", "w") as f:
    for s, E in zip(steps, E_vals):
        f.write(f"{s} {E}\n")

# Graficar
plt.figure(figsize=(8, 5))
plt.plot(steps, E_vals, marker='o', linestyle='-')
plt.xlabel("Paso (MD step)")
plt.ylabel("Energía E")
plt.title("E vs número de pasos")
plt.grid(True)
plt.tight_layout()
plt.savefig("E_vs_steps.png")
plt.show()
