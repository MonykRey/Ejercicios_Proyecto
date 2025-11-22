#!/usr/bin/env python3
# archivo: src/base_freq.py

import argparse
import os
import sys
from typing import Tuple

# ---------------------------
# ARGPARSE (mezclado en el código)
# ---------------------------
def parse_args(argv=None) -> str:
    """
    Parse command-line arguments and return the FASTA file path.

    Accepts an optional argv for easier testing.
    """
    parser = argparse.ArgumentParser(
        description="Calcula la frecuencia de A, T, G y C de un archivo FASTA con UNA sola secuencia."
    )
    parser.add_argument("fasta", help="Archivo FASTA que contiene una sola secuencia.")
    args = parser.parse_args(argv)
    return args.fasta


def read_file(path: str) -> str:
    """
    Leer y devolver el contenido del archivo usando UTF-8.

    Lanza la excepción original al llamador para que gestione el mensaje y el exit.
    """
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


def extract_header_and_sequence(fasta_text: str) -> Tuple[str, str]:
    """
    Extrae el encabezado y la secuencia raw (concatenada, en mayúsculas) de la
    primera entrada FASTA encontrada en el texto.
    """
    partes = fasta_text.split(">")
    if len(partes) < 2:
        raise ValueError("FASTAFORMAT_EMPTY")
    bloque = partes[1].strip().split("\n")
    header = bloque[0]
    sec = "".join(bloque[1:]).strip().upper()
    return header, sec


def clean_sequence(raw_seq: str, header: str) -> str:
    """
    Filtra y devuelve solo las bases válidas A/T/G/C en mayúsculas.
    Imprime avisos por cada carácter inválido (manteniendo el comportamiento original).
    """
    bases_validas = {"A", "T", "G", "C"}
    seq_limpia_chars = []
    for base in raw_seq:
        if base in bases_validas:
            seq_limpia_chars.append(base)
        else:
            # Mantener exactamente el mensaje original por carácter inválido
            print(f"Aviso: caracter inválido '{base}' ignorado en la secuencia '{header}'")
    return "".join(seq_limpia_chars)


def calc_and_print_frequencies(header: str, seq_limpia: str) -> None:
    """
    Calcula los conteos y porcentajes y los imprime en el mismo formato que el programa original.
    """
    total = len(seq_limpia)
    a = seq_limpia.count("A")
    t = seq_limpia.count("T")
    g = seq_limpia.count("G")
    c = seq_limpia.count("C")

    print("Encabezado:", header)
    print("Longitud secuencia válida:", total)
    print("Frecuencias:")
    # Mantener redondeo y formato exactamente igual
    print("A:", a, f"({round((a/total)*100,2)}%)")
    print("T:", t, f"({round((t/total)*100,2)}%)")
    print("G:", g, f"({round((g/total)*100,2)}%)")
    print("C:", c, f"({round((c/total)*100,2)}%)")


def main(argv=None) -> None:
    """
    Orquesta la ejecución: parseo, validaciones, lectura, procesamiento y salida.
    Conserva los mensajes y sys.exit como en el original.
    """
    ruta = parse_args(argv)

    if not os.path.exists(ruta):
        print("Error: el archivo no existe:", ruta)
        sys.exit(1)

    try:
        contenido = read_file(ruta)
    except Exception as e:
        print("Error al leer el archivo:", e)
        sys.exit(1)

    if ">" not in contenido:
        print("Error: El archivo no parece estar en formato FASTA.")
        sys.exit(1)

    try:
        header, sec = extract_header_and_sequence(contenido)
    except ValueError:
        print("Error: FASTA vacío o sin secuencia válida.")
        sys.exit(1)

    if len(sec) == 0:
        print("Error: la secuencia está vacía.")
        sys.exit(1)

    seq_limpia = clean_sequence(sec, header)

    if len(seq_limpia) == 0:
        print("Error: la secuencia no contiene bases válidas (A,T,G,C).")
        sys.exit(1)

    calc_and_print_frequencies(header, seq_limpia)


if __name__ == "__main__":
    main()
