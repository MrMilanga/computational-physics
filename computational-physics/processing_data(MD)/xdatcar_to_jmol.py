"""
xdatcar_to_jmol.py
Convierte un archivo XDATCAR de VASP a formato XYZ multi-frame
para visualizar como animación en Jmol.

Uso:
    python xdatcar_to_jmol.py [XDATCAR] [salida.xyz] [opciones]

Opciones:
    --step N     Guardar cada N frames (default: 1, todos)
    --start N    Frame inicial (default: primer frame encontrado)
    --end N      Frame final (default: último frame)
"""

import numpy as np
import sys
import argparse
import os


def parse_xdatcar(filepath):
    """
    Lee un archivo XDATCAR y devuelve una lista de frames.
    Cada frame es un dict con:
        - config_num : número de configuración
        - lattice    : array (3x3) de vectores de celda (Angstrom)
        - species    : lista de símbolos atómicos
        - counts     : lista de conteos por especie
        - coords     : array (N, 3) coordenadas directas (fraccionarias)
    """
    frames = []
    current_lattice = None
    current_species = None
    current_counts = None

    with open(filepath, "r") as f:
        lines = f.readlines()

    i = 0
    total = len(lines)

    while i < total:
        line = lines[i].strip()

        # El encabezado VASP XDATCAR tiene exactamente este formato:
        #   línea 0: título
        #   línea 1: factor de escala
        #   línea 2: vector a
        #   línea 3: vector b
        #   línea 4: vector c
        #   línea 5: símbolos de especies
        #   línea 6: conteos por especie
        #   línea 7: "Direct configuration= N"
        # Entre frames el encabezado se repite completo.
        if line.lower().startswith("direct"):
            header_start = i - 7
            if header_start >= 0:
                try:
                    scale = float(lines[header_start + 1].strip())
                    a = np.array([float(x) for x in lines[header_start + 2].split()]) * scale
                    b = np.array([float(x) for x in lines[header_start + 3].split()]) * scale
                    c = np.array([float(x) for x in lines[header_start + 4].split()]) * scale
                    current_lattice = np.array([a, b, c])
                    current_species = lines[header_start + 5].split()
                    current_counts = [int(x) for x in lines[header_start + 6].split()]
                except (ValueError, IndexError):
                    pass  # Mantener lattice del frame anterior si falla

            # Número de configuración
            try:
                config_num = int(line.split("=")[-1].strip())
            except ValueError:
                config_num = len(frames) + 1

            # Leer coordenadas
            n_atoms = sum(current_counts)
            coords = []
            for j in range(1, n_atoms + 1):
                if i + j < total:
                    vals = lines[i + j].strip().split()
                    if len(vals) >= 3:
                        coords.append([float(v) for v in vals[:3]])

            if len(coords) == n_atoms:
                frames.append({
                    "config_num": config_num,
                    "lattice": current_lattice.copy(),
                    "species": list(current_species),
                    "counts": list(current_counts),
                    "coords": np.array(coords),
                })

            i += n_atoms + 1
        else:
            i += 1

    return frames


def direct_to_cartesian(coords_direct, lattice):
    """
    Convierte coordenadas directas (fraccionarias) a cartesianas.
    coords_direct : array (N, 3)
    lattice       : array (3, 3), filas = vectores a, b, c
    Retorna array (N, 3) en Angstrom.
    """
    return coords_direct @ lattice


def write_xyz(frames, output_path, step=1, start=None, end=None):
    """
    Escribe un archivo XYZ multi-frame.
    En el comentario de cada frame incluye la celda para que Jmol
    pueda leerla con: load "archivo.xyz" {1 1 1}
    """
    selected = frames[::step]

    # Filtrar por rango de configuración si se especifica
    if start is not None:
        selected = [f for f in selected if f["config_num"] >= start]
    if end is not None:
        selected = [f for f in selected if f["config_num"] <= end]

    if not selected:
        print(" No se encontraron frames con los filtros especificados.")
        return 0

    with open(output_path, "w") as out:
        for frame in selected:
            lattice = frame["lattice"]
            coords_cart = direct_to_cartesian(frame["coords"], lattice)

            # Construir lista de símbolos por átomo
            atom_symbols = []
            for symbol, count in zip(frame["species"], frame["counts"]):
                atom_symbols.extend([symbol] * count)

            n_atoms = len(atom_symbols)

            # Línea 1: número de átomos
            out.write(f"{n_atoms}\n")

            # Línea 2: comentario con información de celda (formato Jmol/OVITO)
            a, b, c = lattice[0], lattice[1], lattice[2]
            comment = (
                f'config={frame["config_num"]} '
                f'Lattice="{a[0]:.6f} {a[1]:.6f} {a[2]:.6f} '
                f'{b[0]:.6f} {b[1]:.6f} {b[2]:.6f} '
                f'{c[0]:.6f} {c[1]:.6f} {c[2]:.6f}" '
                f'Properties=species:S:1:pos:R:3'
            )
            out.write(comment + "\n")

            # Coordenadas
            for sym, pos in zip(atom_symbols, coords_cart):
                out.write(f"{sym:4s}  {pos[0]:14.8f}  {pos[1]:14.8f}  {pos[2]:14.8f}\n")

    return len(selected)


def print_summary(frames):
    if not frames:
        print("No se encontraron frames.")
        return
    configs = [f["config_num"] for f in frames]
    print(f"  Frames encontrados : {len(frames)}")
    print(f"  Configuraciones    : {min(configs)} → {max(configs)}")
    print(f"  Átomos por frame   : {sum(frames[0]['counts'])}")
    print(f"  Especies           : {', '.join(frames[0]['species'])} "
          f"({', '.join(str(c) for c in frames[0]['counts'])})")
    a, b, c = frames[0]["lattice"]
    print(f"  Celda (frame 1)    :")
    print(f"    a = [{a[0]:8.4f}  {a[1]:8.4f}  {a[2]:8.4f}]  |a| = {np.linalg.norm(a):.4f} Å")
    print(f"    b = [{b[0]:8.4f}  {b[1]:8.4f}  {b[2]:8.4f}]  |b| = {np.linalg.norm(b):.4f} Å")
    print(f"    c = [{c[0]:8.4f}  {c[1]:8.4f}  {c[2]:8.4f}]  |c| = {np.linalg.norm(c):.4f} Å")


def main():
    parser = argparse.ArgumentParser(
        description="Convierte XDATCAR de VASP a XYZ multi-frame para Jmol."
    )
    parser.add_argument(
        "input", nargs="?", default="XDATCAR",
        help="Archivo XDATCAR de entrada (default: XDATCAR)"
    )
    parser.add_argument(
        "output", nargs="?", default=None,
        help="Archivo XYZ de salida (default: <nombre_entrada>.xyz)"
    )
    parser.add_argument(
        "--step", type=int, default=1,
        help="Guardar 1 de cada N frames (default: 1)"
    )
    parser.add_argument(
        "--start", type=int, default=None,
        help="Número de configuración inicial"
    )
    parser.add_argument(
        "--end", type=int, default=None,
        help="Número de configuración final"
    )

    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"Archivo no encontrado: {args.input}")
        sys.exit(1)

    if args.output is None:
        base = os.path.splitext(os.path.basename(args.input))[0]
        args.output = base + ".xyz"

    print(f"\n Leyendo: {args.input}")
    frames = parse_xdatcar(args.input)

    print("\nResumen del archivo:")
    print_summary(frames)

    print(f"\nEscribiendo: {args.output}")
    print(f"   Paso entre frames : {args.step}")
    if args.start:
        print(f"   Desde config      : {args.start}")
    if args.end:
        print(f"   Hasta config      : {args.end}")

    n_written = write_xyz(frames, args.output, step=args.step,
                          start=args.start, end=args.end)

    print(f"\n Listo. Se escribieron {n_written} frames → {args.output}")
    print("\n─────────────────────────────────────────────")
    print("💡 Para abrir en Jmol, usá estos comandos:")
    print(f'   load "{args.output}"')
    print( '   animation mode loop')
    print( '   animation fps 10')
    print( '   animation on')
    print("─────────────────────────────────────────────\n")


if __name__ == "__main__":
    main()
