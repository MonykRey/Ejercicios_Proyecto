#!/usr/bin/env python3
# archivo: src/base_freq.py

import argparse
import os
import sys
from typing import Tuple

# ---------------------------
# CONSTANTES
# ---------------------------
VALID_BASES = {"A", "T", "G", "C"}
MAX_FILE_SIZE_MB = 100

# ---------------------------
# ARGPARSE
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
    
    # Validar que la ruta no sea vacía
    if not args.fasta or not args.fasta.strip():
        print("Error: la ruta del archivo no puede estar vacía.")
        sys.exit(1)
    
    return args.fasta.strip()


def read_file(path: str) -> str:
    """
    Leer y devolver el contenido del archivo usando UTF-8.

    Validaciones:
    - Archivo existe
    - Es un archivo (no directorio)
    - No excede tamaño máximo
    - Se puede leer (permisos)
    - Encoding UTF-8 válido
    """
    # Validar que el archivo existe
    if not os.path.exists(path):
        raise FileNotFoundError(f"El archivo no existe: {path}")
    
    # Validar que es un archivo, no directorio
    if not os.path.isfile(path):
        raise IsADirectoryError(f"La ruta es un directorio, no un archivo: {path}")
    
    # Validar tamaño del archivo
    file_size_mb = os.path.getsize(path) / (1024 * 1024)
    if file_size_mb > MAX_FILE_SIZE_MB:
        raise ValueError(f"El archivo es demasiado grande ({file_size_mb:.1f} MB). Máximo: {MAX_FILE_SIZE_MB} MB")
    
    # Validar que tenemos permisos de lectura
    if not os.access(path, os.R_OK):
        raise PermissionError(f"No hay permisos de lectura para: {path}")
    
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return fh.read()
    except UnicodeDecodeError as e:
        raise UnicodeDecodeError(
            e.encoding,
            e.object,
            e.start,
            e.end,
            f"El archivo no está en UTF-8 válido: {e.reason}"
        )


def extract_header_and_sequence(fasta_text: str) -> Tuple[str, str]:
    """
    Extrae el encabezado y la secuencia raw (concatenada, en mayúsculas) de la
    primera entrada FASTA encontrada en el texto.
    
    Validaciones:
    - Archivo FASTA no vacío
    - Contiene al menos un ">"
    - Header no vacío
    - Secuencia no vacía
    """
    # Validar que el archivo no está vacío
    if not fasta_text or not fasta_text.strip():
        raise ValueError("FASTAFORMAT_EMPTY: El archivo está vacío")
    
    # Validar que contiene ">"
    if ">" not in fasta_text:
        raise ValueError("FASTAFORMAT_INVALID: El archivo no contiene '>'. No es FASTA válido.")
    
    partes = fasta_text.split(">")
    if len(partes) < 2:
        raise ValueError("FASTAFORMAT_EMPTY")
    
    bloque = partes[1].strip().split("\n")
    header = bloque[0].strip()
    
    # Validar que el header no es vacío
    if not header:
        raise ValueError("FASTAFORMAT_INVALID: El header está vacío (línea después de '>').")
    
    sec = "".join(bloque[1:]).strip().upper()
    
    # Validar que la secuencia no es vacía
    if not sec:
        raise ValueError("FASTAFORMAT_INVALID: No hay secuencia después del header.")
    
    # Avisar si hay múltiples secuencias
    if fasta_text.count(">") > 1:
        print(f"Aviso: El archivo FASTA contiene {fasta_text.count('>')} secuencias.")
        print("Procesando solo la primera secuencia.")
    
    return header, sec


def clean_sequence(raw_seq: str, header: str) -> str:
    """
    Filtra y devuelve solo las bases válidas A/T/G/C en mayúsculas.
    
    Manejo mejorado de caracteres inválidos:
    - Cuenta caracteres inválidos en lugar de printear cada uno
    - Proporciona resumen al final
    - Diferencia entre distintos tipos de caracteres inválidos
    """
    seq_limpia_chars = []
    invalid_chars = {}
    invalid_count = 0
    
    for base in raw_seq:
        if base in VALID_BASES:
            seq_limpia_chars.append(base)
        else:
            invalid_count += 1
            # Contar ocurrencias de cada carácter inválido
            invalid_chars[base] = invalid_chars.get(base, 0) + 1
    
    # Mostrar resumen una sola vez
    if invalid_count > 0:
        print(f"Aviso: Se encontraron {invalid_count} caracteres inválidos en '{header}':")
        for char, count in sorted(invalid_chars.items()):
            if char == ' ':
                print(f"  - espacio: {count} ocurrencia(s)")
            elif char == '\t':
                print(f"  - tabulador: {count} ocurrencia(s)")
            elif char == '\n':
                print(f"  - salto de línea: {count} ocurrencia(s)")
            else:
                print(f"  - '{char}': {count} ocurrencia(s)")
    
    return "".join(seq_limpia_chars)


def calc_and_print_frequencies(header: str, seq_limpia: str) -> None:
    """
    Calcula los conteos y porcentajes y los imprime en el mismo formato que el programa original.
    
    Validación: Protege contra división por cero si seq_limpia está vacía.
    """
    total = len(seq_limpia)
    
    # Proteger contra división por cero
    if total == 0:
        raise ValueError("CALCULATION_ERROR: La secuencia limpia está vacía. No se puede calcular frecuencias.")
    
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
    
    Manejo robusto de errores con excepciones específicas para cada tipo de error.
    """
    try:
        ruta = parse_args(argv)
    except SystemExit as e:
        sys.exit(e.code)

    # Manejo específico de diferentes tipos de errores de archivo
    try:
        contenido = read_file(ruta)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except IsADirectoryError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except PermissionError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except UnicodeDecodeError as e:
        print(f"Error: Encoding inválido - {e.reason}")
        sys.exit(1)
    except Exception as e:
        print(f"Error inesperado al leer el archivo: {e}")
        sys.exit(1)

    # Validar que el contenido no está vacío
    if not contenido or not contenido.strip():
        print("Error: El archivo está vacío.")
        sys.exit(1)

    # Manejo específico de errores de parseo FASTA
    try:
        header, sec = extract_header_and_sequence(contenido)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error inesperado al parsear FASTA: {e}")
        sys.exit(1)

    # Validar que la secuencia no está vacía
    if len(sec) == 0:
        print("Error: la secuencia está vacía.")
        sys.exit(1)

    # Limpiar secuencia
    try:
        seq_limpia = clean_sequence(sec, header)
    except Exception as e:
        print(f"Error al limpiar la secuencia: {e}")
        sys.exit(1)

    # Validar que la secuencia limpia no está vacía
    if len(seq_limpia) == 0:
        print("Error: la secuencia no contiene bases válidas (A,T,G,C).")
        sys.exit(1)

    # Manejo de errores en cálculo de frecuencias
    try:
        calc_and_print_frequencies(header, seq_limpia)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except ZeroDivisionError:
        print("Error: División por cero al calcular porcentajes.")
        sys.exit(1)
    except Exception as e:
        print(f"Error inesperado al calcular frecuencias: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
