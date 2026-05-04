[README_computational_physics.md](https://github.com/user-attachments/files/27326575/README_computational_physics.md)
# Computational Physics

A collection of numerical methods and simulations developed during my Physics degree at [Universidad Nacional del Sur](https://www.uns.edu.ar/), Bahía Blanca, Argentina.

Each script tackles a different area of physics using Python, covering quantum mechanics, electrostatics, signal processing, and ab initio molecular dynamics post-processing.

---

## Repository Structure

```
computational-physics/
│
├── quantum/
│   ├── 1D_Ec_Schrodinger_matriz.py              # 1D Schrödinger equation via matrix diagonalization
│   ├── Comparacion_Fdtd_y_matriz.py             # FDTD vs matrix method comparison (animated)
│   └── el_tunelamiento_mas_tunelamiento_que_nunca.py  # Quantum tunneling — Gaussian wave packet
│
├── electrostatics/
│   ├── Laplace3d_convolucion.py                 # 3D Laplace equation via convolution
│   ├── laplace2D.py                             # 2D Laplace with Numba JIT + conductor block + 3D plot
│   └── Metodo_de_relajación_con_conductor.ipynb # 2D relaxation method with conductor boundary
│
├── signal_processing/
│   ├── transformada_de_fourier_.py              # Discrete Fourier Transform basics
│   └── transformada_de_fourier_ondas_aleatorias.py   # FFT of superposed random waves
│
└── processing_data(MD)/
    └── EvsN.py                                  # Energy vs MD steps parser (VASP output)
```

---

##  Scripts Overview

---

###Quantum Mechanics

#### `1D_Ec_Schrodinger_matriz.py`
Solves the **time-independent 1D Schrödinger equation** using matrix diagonalization.

- Builds the Hamiltonian as a tridiagonal matrix using finite differences
- Diagonalizes it with `scipy.linalg.eigh_tridiagonal` to obtain eigenvalues and eigenvectors
- Plots the potential, wavefunctions ψ, and probability densities |ψ|²
- Default potential: Pöschl-Teller well `V(x) = -25/cosh(5x)`

```python
python 1D_Ec_Schrodinger_matriz.py
```

**Output:**

| Plot | Description |
|---|---|
| Potential V(x) | Shape of the quantum well |
| Eigenstates ψ | Ground state + first 3 excited states |
| Probability densities \|ψ\|² | Where the particle is most likely found |
| Eigenvalue spectrum | Energy levels vs quantum number N |

---

#### `Comparacion_Fdtd_y_matriz.py`
Compares two independent numerical methods for the **time-dependent Schrödinger equation** and animates both simultaneously.

| Method | Description |
|---|---|
| **FDTD** (Finite Difference Time Domain) | Explicit time evolution with imaginary time step |
| **Matrix decomposition** | Expansion in energy eigenstates, exact time evolution |

The animation (`animacion.gif`) shows both probability densities evolving — agreement between methods validates the numerical accuracy.

```python
python Comparacion_Fdtd_y_matriz.py
# Output: animacion.gif
```

---

#### `el_tunelamiento_mas_tunelamiento_que_nunca.py`
Simulates a **Gaussian wave packet** tunneling through a Pöschl-Teller potential barrier.

- Full matrix Hamiltonian (kinetic + potential) via `numpy.linalg.eigh`
- Time evolution by expansion in energy eigenstates
- Tracks real part, imaginary part, and probability density
- Monitors norm conservation over time (numerical stability check)
- Generates animated GIF of the tunneling event

```python
python el_tunelamiento_mas_tunelamiento_que_nunca.py
# Output: animacion.gif, densidad de probabilidad.gif
```

---

### Electrostatics

#### `Laplace3d_convolucion.py`
Solves the **3D Laplace equation** using a convolution-based relaxation method.

- Discretizes a 100×100×100 grid
- Uses `scipy.ndimage.convolve` with a 3D 6-neighbor kernel (equivalent to the discrete Laplacian)
- Applies Dirichlet boundary conditions (conductor plates at fixed potentials)
- Runs 1000 relaxation iterations
- Visualizes a 2D equipotential cross-section with contour lines

```python
python Laplace3d_convolucion.py
```

**Physical setup:** Two parallel conductor plates inside a box — models a capacitor-like geometry.

---

#### `laplace2D.py`
Solves the **2D Laplace equation** with a conductor block obstacle, accelerated with **Numba JIT compilation**.

- Defines a square conductor region using boolean masks and `numpy.select`
- Applies **Dirichlet boundary conditions** on all four edges (different voltage on each side)
- Uses `@numba.jit` with `nopython=True, nogil=True` for near-C performance on the inner loop
- Runs 2000 relaxation iterations on a 100×100 grid
- Produces both a **2D filled contour plot** and a **3D wireframe surface** of the potential

```python
pip install numba
python laplace2D.py
```

**Physical setup:** A grounded conductor block embedded in a region with asymmetric boundary voltages — the potential field adapts around the obstacle.

| Output | Description |
|---|---|
| 2D contour plot | Equipotential lines around the conductor |
| 3D wireframe | Full surface V(x, y) |

> **Why Numba?** The relaxation algorithm requires iterating over every grid point at every step — a pure Python loop over a 100×100 grid for 2000 iterations is slow. `@numba.jit` compiles the function to native machine code, giving 100–200× speedup with no change to the algorithm.

---

#### `Metodo_de_relajación_con_conductor.ipynb`
Jupyter notebook solving the **2D Laplace equation** with a conductor obstacle using iterative relaxation.

- Implements a custom `calculate_potential()` function with convergence criterion `ε = 1e-6`
- Supports arbitrary conductor geometries via boolean masks
- Enforces boundary conditions at each iteration
- Best viewed directly on GitHub (renders automatically)

```bash
jupyter notebook Metodo_de_relajación_con_conductor.ipynb
```

---

### Signal Processing

#### `transformada_de_fourier_.py`
Clean introduction to the **Discrete Fourier Transform** applied to a known signal.

- Constructs a signal: `sin(2πft) + cos(3πft)`
- Computes DFT with `numpy.fft.fft`
- Plots original signal and frequency spectrum side by side
- Useful as a minimal reference implementation

```python
python transformada_de_fourier_.py
```

---

#### `transformada_de_fourier_ondas_aleatorias.py`
Generates a **random superposition of waves** and recovers their frequency content via FFT.

- Creates N random waves with random amplitude, phase, and frequency
- Sums them into a composite signal
- Applies FFT and plots the power spectrum |F(ω)|²
- Visualizes each individual component alongside the total signal

```python
python transformada_de_fourier_ondas_aleatorias.py
```

---

###  Ab Initio / VASP Post-processing

#### `EvsN.py`
Parser and plotter for **VASP molecular dynamics output**.

- Reads `OUTCAR`-style output (`salida.txt`) using regex
- Extracts energy E and MD step number at each ionic step
- Saves parsed data to `E_vs_steps.dat`
- Plots energy convergence curve — used to monitor MD equilibration

```python
# Requires: salida.txt (VASP OUTCAR or equivalent output)
python EvsN.py
# Output: E_vs_steps.png, E_vs_steps.dat
```

This script was used in research on NiTi shape memory alloys and FeRh magnetic alloys using the **VASP** package (Vienna Ab initio Simulation Package).

---

##Installation

```bash
pip install numpy scipy matplotlib jupyter numba
```

No additional dependencies required beyond the standard scientific Python stack. `numba` is only needed for `laplace2D.py`.

---

##  Author

**Francisco Nahuel Quintanilla**
Physics undergraduate — Universidad Nacional del Sur, Bahía Blanca, Argentina
[LinkedIn](https://www.linkedin.com/in/francisco-quintanilla-b40367386/)
