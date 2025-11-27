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
    python3 k-mers.py ATCGATCG -k 2 --sort frequency
"""
import argparse
import sys
from collections import Counter


# Constantes globales para validación de nucleótidos
VALID_NUCLEOTIDES = {"A", "T", "C", "G"}
VALID_NUCLEOTIDES_STR = "A, T, C, G"

# Opciones de ordenamiento disponibles
SORT_OPTIONS = ["appearance", "frequency", "kmer"]


def validate_sequence(seq):
    """Validar que la secuencia contenga solo nucleótidos válidos.

    Verifica que la secuencia de ADN solo contenga los nucleótidos A, T, C, G.
    Convierte la secuencia a mayúsculas para normalizar la entrada.

    Parameters
    ----------
    seq : str
        Secuencia de ADN a validar.

    Returns
    -------
    str
        Secuencia normalizada (mayúsculas).

    Raises
    ------
    TypeError
        Si el argumento no es una cadena de texto.
    ValueError
        Si la secuencia está vacía o contiene nucleótidos inválidos.

    Examples
    --------
    >>> validate_sequence("ATCG")
    'ATCG'

    >>> validate_sequence("atcg")
    'ATCG'

    >>> validate_sequence("ATCGX")
    Traceback (most recent call last):
        ...
    ValueError: La secuencia contiene nucleótidos inválidos: X...

    Notes
    -----
    La función acepta minúsculas y las convierte a mayúsculas.
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
    invalid_chars = set(seq_upper) - VALID_NUCLEOTIDES

    if invalid_chars:
        invalid_str = ", ".join(sorted(invalid_chars))
        raise ValueError(
            f"La secuencia contiene nucleótidos inválidos: {invalid_str}. "
            f"Solo se permiten: {VALID_NUCLEOTIDES_STR}."
        )

    return seq_upper


def count_kmers(seq, k):
    """Contar la frecuencia de cada k-mer en una secuencia.

    Extrae todos los k-mers contiguos de longitud k de la secuencia
    y cuenta cuántas veces aparece cada uno usando un algoritmo de
    ventana deslizante.

    Parameters
    ----------
    seq : str
        Secuencia de ADN validada (solo A, T, C, G).
    k : int
        Longitud del k-mer (1 <= k <= len(seq)).

    Returns
    -------
    Counter
        Objeto Counter con k-mers como claves y sus frecuencias como valores.

    Raises
    ------
    TypeError
        Si k no es un entero o si es un booleano.
    ValueError
        Si k <= 0 o si k > len(seq).

    Examples
    --------
    >>> count_kmers("ATCGATCG", 2)
    Counter({'AT': 2, 'TC': 2, 'CG': 2, 'GA': 1})

    >>> count_kmers("ATCGATCG", 3)
    Counter({'ATC': 2, 'TCG': 2, 'CGA': 1, 'GAT': 1})

    Time Complexity
    ---------------
    O(n * k) donde n es la longitud de la secuencia.
    Nota: El slicing de Python es O(k).

    Space Complexity
    ----------------
    O(unique_kmers * k) para almacenar el Counter.
    En el peor caso, O(n * k) si todos los k-mers son únicos.

    Notes
    -----
    - El parámetro k no puede ser un booleano (bool es subclase de int).
    - La secuencia debe estar validada antes de llamar a esta función.
    - Los k-mers se extraen con solapamiento (overlapping).
    """
    # Validar tipo de dato (evitar que bool sea aceptado como int)
    if isinstance(k, bool) or not isinstance(k, int):
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

    # Generar k-mers usando una lista comprehension
    kmers = [seq[i:i + k] for i in range(len(seq) - k + 1)]

    # Contar k-mers usando Counter (mucho más eficiente y limpio)
    return Counter(kmers)


def format_output(kmer_counts, sort_by="appearance"):
    """Formatear los resultados para impresión.

    Parameters
    ----------
    kmer_counts : Counter
        Counter con los k-mers y sus frecuencias.
    sort_by : str, optional
        Criterio de ordenamiento: "appearance", "frequency", o "kmer".
        Por defecto "appearance" (orden de inserción).

    Returns
    -------
    str
        Cadena formateada lista para imprimir.

    Raises
    ------
    ValueError
        Si sort_by no es una opción válida.

    Examples
    --------
    >>> from collections import Counter
    >>> kmers = Counter({'AT': 2, 'TC': 2, 'CG': 2, 'GA': 1})
    >>> print(format_output(kmers, "frequency"))
    # kmer\tfrequency
    AT\t2
    TC\t2
    CG\t2
    GA\t1
    """
    if sort_by not in SORT_OPTIONS:
        raise ValueError(
            f"sort_by debe ser una de: {', '.join(SORT_OPTIONS)}. "
            f"Se recibió: {sort_by}"
        )

    # Ordenar según criterio
    if sort_by == "frequency":
        sorted_items = kmer_counts.most_common()
    elif sort_by == "kmer":
        sorted_items = sorted(kmer_counts.items())
    else:  # appearance (orden natural del Counter)
        sorted_items = kmer_counts.items()

    # Construir salida formateada
    lines = ["# kmer\tfrequency"]
    for kmer, count in sorted_items:
        lines.append(f"{kmer}\t{count}")

    return "\n".join(lines)


def process_kmer_analysis(seq, k):
    """Realizar el análisis de k-mers sin I/O.

    Función auxiliar que encapsula la lógica de negocio.

    Parameters
    ----------
    seq : str
        Secuencia de ADN (sin validar aún).
    k : int
        Longitud del k-mer.

    Returns
    -------
    Counter
        Resultados del conteo de k-mers.

    Raises
    ------
    ValueError, TypeError
        Si la secuencia o k son inválidos.

    Notes
    -----
    Esta función es útil para reutilizar la lógica en otros contextos
    (tests, APIs, etc.) sin mezclar con I/O.
    """
    seq_validated = validate_sequence(seq)
    kmer_counts = count_kmers(seq_validated, k)
    return kmer_counts


def main():
    """Función principal que orquesta el programa.

    Realiza las siguientes tareas:
    1. Parsea los argumentos de línea de comandos.
    2. Realiza el análisis de k-mers.
    3. Formatea y imprime los resultados.

    Maneja excepciones y proporciona mensajes de error descriptivos.

    Exit Codes
    ----------
    0 : Ejecución exitosa.
    1 : Error en la validación o procesamiento.
    """
    # Crear el parser de argumentos
    parser = argparse.ArgumentParser(
        description=(
            "Contador de k-mers: cuenta la frecuencia de cada k-mer en una "
            "secuencia de ADN."
        ),
        epilog=(
            "Ejemplos:\n"
            "  python3 k-mers.py ATCGATCG -k 2\n"
            "  python3 k-mers.py ATCGATCG -k 3 --sort frequency\n"
            "  python3 k-mers.py atcgatcg -k 2 --sort kmer"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    # Argumento posicional: secuencia
    parser.add_argument(
        "sequence",
        type=str,
        metavar="SEQUENCE",
        help="Secuencia de ADN (solo A, T, C, G). Acepta minúsculas.",
    )

    # Argumento opcional: tamaño de k
    parser.add_argument(
        "-k",
        "--kmer_size",
        type=int,
        required=True,
        metavar="INT",
        help="Tamaño del k-mer (entero positivo, <= longitud de secuencia).",
    )

    # Argumento opcional: ordenamiento de salida
    parser.add_argument(
        "--sort",
        choices=SORT_OPTIONS,
        default="appearance",
        metavar="ORDER",
        help=(
            "Criterio de ordenamiento: 'appearance' (predeterminado), "
            "'frequency' (descendente), o 'kmer' (alfabético)."
        ),
    )

    # Argumento opcional: modo verbose
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Mostrar información detallada de procesamiento.",
    )

    # Parsear argumentos
    try:
        args = parser.parse_args()
    except SystemExit:
        # argparse ya imprime el mensaje de error
        sys.exit(1)

    # Información en modo verbose
    if args.verbose:
        print(f"Secuencia: {args.sequence}", file=sys.stderr)
        print(f"Longitud: {len(args.sequence)}", file=sys.stderr)
        print(f"k: {args.kmer_size}", file=sys.stderr)

    # Realizar análisis de k-mers
    try:
        kmer_counts = process_kmer_analysis(args.sequence, args.kmer_size)
    except (ValueError, TypeError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    # Verificar que se encontraron k-mers (validación de seguridad)
    if not kmer_counts:
        print(
            "Error: No se encontraron k-mers (esto no debería ocurrir).",
            file=sys.stderr,
        )
        sys.exit(1)

    # Imprimir estadísticas en modo verbose
    if args.verbose:
        total_kmers = sum(kmer_counts.values())
        unique_kmers = len(kmer_counts)
        max_kmer = max(kmer_counts, key=kmer_counts.get)
        max_count = kmer_counts[max_kmer]
        print(f"Total de k-mers: {total_kmers}", file=sys.stderr)
        print(f"k-mers únicos: {unique_kmers}", file=sys.stderr)
        print(f"k-mer más frecuente: {max_kmer} ({max_count}x)", 
              file=sys.stderr)
        print(file=sys.stderr)  # Línea en blanco

    # Formatear y imprimir resultados
    try:
        output = format_output(kmer_counts, args.sort)
        print(output)
    except ValueError as e:
        print(f"Error en formateo: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
