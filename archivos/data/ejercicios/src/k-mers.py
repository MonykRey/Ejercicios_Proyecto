#!/usr/bin/env python3
"""Contador de k-mers para secuencias de ADN.

Este módulo implementa un programa que cuenta la frecuencia de cada k-mer
(fragmento de longitud k) en una secuencia de ADN dada.

Requerimientos:
- Validar que la secuencia solo contenga nucleótidos válidos (A, T, C, G).
- Leer la secuencia desde un argumento posicional.
- Leer k desde la opción -k / --kmer_size.
- Contar todos los k-mers contiguos de longitud k.
- Imprimir resultados en formato: kmer<TAB>conteo.

Ejemplo de uso:
    python3 k-mers.py ATCGATCG -k 2
    python3 k-mers.py ATCGATCG --kmer_size 3
"""
import argparse
import sys


def validate_sequence(seq):
    """Validar que la secuencia contenga solo nucleótidos válidos.

    Verifica que la secuencia de ADN solo contenga los nucleótidos A, T, C, G.
    Convierte la secuencia a mayúsculas para normalizar la entrada.

    Args:
        seq (str): Secuencia de ADN a validar.

    Returns:
        str: Secuencia normalizada (mayúsculas).

    Raises:
        ValueError: Si la secuencia contiene caracteres inválidos o está vacía.
        TypeError: Si el argumento no es una cadena de texto.
    """
    # Validar tipo de dato
    if not isinstance(seq, str):
        raise TypeError(
            f"La secuencia debe ser una cadena de texto, "
            f"se recibió: {type(seq).__name__}"
        )

    # Validar que no esté vacía
    if not seq:
        raise ValueError("La secuencia no puede estar vacía.")

    # Normalizar a mayúsculas
    seq_upper = seq.upper()

    # Validar caracteres válidos
    valid_nucleotides = set("ATCG")
    invalid_chars = set(seq_upper) - valid_nucleotides

    if invalid_chars:
        invalid_str = ", ".join(sorted(invalid_chars))
        raise ValueError(
            f"La secuencia contiene nucleótidos inválidos: {invalid_str}. "
            f"Solo se permiten: A, T, C, G."
        )

    return seq_upper


def count_kmers(seq, k):
    """Contar la frecuencia de cada k-mer en una secuencia.

    Extrae todos los k-mers contiguos de longitud k de la secuencia
    y cuenta cuántas veces aparece cada uno.

    Args:
        seq (str): Secuencia de ADN (debe estar validada).
        k (int): Longitud del k-mer.

    Returns:
        dict: Diccionario con k-mers como claves y sus frecuencias como valores.
              La secuencia de inserción se mantiene.

    Raises:
        ValueError: Si k es inválido (no positivo o mayor que la secuencia).
        TypeError: Si k no es un entero.
    """
    # Validar tipo de dato de k
    if not isinstance(k, int):
        raise TypeError(
            f"k debe ser un entero, se recibió: {type(k).__name__}"
        )

    # Validar que k sea positivo
    if k <= 0:
        raise ValueError(
            f"El tamaño de k debe ser mayor a 0, se recibió: {k}"
        )

    # Validar que k no sea mayor que la secuencia
    if k > len(seq):
        raise ValueError(
            f"El tamaño de k ({k}) no puede ser mayor que "
            f"la longitud de la secuencia ({len(seq)})."
        )

    # Contar k-mers usando ventana deslizante
    kmer_counts = {}

    # Iterar sobre todos los k-mers posibles
    # Número de k-mers = len(seq) - k + 1
    for i in range(len(seq) - k + 1):
        kmer = seq[i:i + k]

        # Incrementar el contador (usar get para inicializar si no existe)
        kmer_counts[kmer] = kmer_counts.get(kmer, 0) + 1

    return kmer_counts


def main():
    """Función principal que orquesta el programa.

    Realiza las siguientes tareas:
    1. Parsea los argumentos de línea de comandos.
    2. Valida la secuencia de entrada.
    3. Valida el tamaño de k.
    4. Cuenta los k-mers.
    5. Imprime los resultados en formato tabulado.

    Maneja excepciones y proporciona mensajes de error descriptivos.
    """
    # Crear el parser de argumentos
    parser = argparse.ArgumentParser(
        description=(
            "Contador de k-mers: cuenta la frecuencia de cada k-mer en una "
            "secuencia de ADN."
        ),
        epilog=(
            "Ejemplo: python3 k-mers.py ATCGATCG -k 2"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    # Argumento posicional: secuencia
    parser.add_argument(
        "sequence",
        type=str,
        help="Secuencia de ADN (solo A, T, C, G).",
    )

    # Argumento opcional: tamaño de k
    parser.add_argument(
        "-k",
        "--kmer_size",
        type=int,
        required=True,
        help="Tamaño del k-mer (debe ser un entero positivo).",
    )

    # Parsear argumentos
    try:
        args = parser.parse_args()
    except SystemExit:
        # argparse ya imprime el mensaje de error
        sys.exit(1)

    # Validar la secuencia
    try:
        seq_validated = validate_sequence(args.sequence)
    except (ValueError, TypeError) as e:
        print(f"Error en la secuencia: {e}", file=sys.stderr)
        sys.exit(1)

    # Contar los k-mers
    try:
        kmer_counts = count_kmers(seq_validated, args.kmer_size)
    except (ValueError, TypeError) as e:
        print(f"Error al contar k-mers: {e}", file=sys.stderr)
        sys.exit(1)

    # Verificar que se encontraron k-mers
    if not kmer_counts:
        print(
            "No se encontraron k-mers (esto no debería ocurrir).",
            file=sys.stderr,
        )
        sys.exit(1)

    # Imprimir resultados en formato: kmer<TAB>conteo
    # Ordenar por orden de aparición (mantiene el diccionario)
    print("# kmer\tconteo")
    for kmer, count in kmer_counts.items():
        print(f"{kmer}\t{count}")


if __name__ == "__main__":
    main()
