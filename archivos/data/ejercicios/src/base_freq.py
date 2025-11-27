#!/usr/bin/env python3
"""Análisis de frecuencias de bases nucleotídicas en archivos FASTA.

Este módulo proporciona funcionalidades para procesar secuencias de ADN desde
archivos en formato FASTA, limpiar caracteres inválidos y calcular la frecuencia
de bases nucleotídicas (A, T, G, C).

Ejemplo de uso:
    $ python base_freq.py data/sequence.fasta

Clases:
    FrequencyResult: Encapsula resultados del análisis de frecuencias.
    CleaningResult: Encapsula resultados de limpieza de secuencia.

Funciones principales:
    main(): Orquesta el flujo completo de procesamiento.
    parse_args(): Procesa argumentos de línea de comandos.
    read_file(): Lee contenido de archivo con validaciones.
    extract_header_and_sequence(): Extrae header y secuencia de FASTA.
    clean_sequence(): Filtra bases inválidas.
    calc_frequencies(): Calcula conteos de bases.
    get_frequency_result(): Crea resultado tipado.
    print_frequencies(): Presenta resultados.

Autor: Mónica Reyes Ramírez
Fecha: 2025-11-26
Versión: 2.0 (Refactored)
"""

import argparse
import os
import sys
from typing import Tuple, Dict
from dataclasses import dataclass

# =============================================================================
# CONSTANTES
# =============================================================================
# Bases nucleotídicas válidas en ADN
NUCLEOTIDE_BASES = {"A", "T", "G", "C"}

# Tamaño máximo de archivo permitido en MB (100 MB)
MAX_FILE_SIZE_MB = 100


# =============================================================================
# DATACLASSES - Estructuras de datos para resultados
# =============================================================================


@dataclass
class FrequencyResult:
    """Encapsula el resultado del análisis de frecuencias de bases.
    
    Atributos:
        header (str): Identificador de la secuencia FASTA.
        sequence_length (int): Longitud de la secuencia limpia.
        frequencies (Dict[str, int]): Conteos de cada base: A, T, G, C.
        invalid_chars_count (int): Total de caracteres inválidos encontrados.
    """

    header: str
    sequence_length: int
    frequencies: Dict[str, int]
    invalid_chars_count: int

    def get_percentage(self, base: str) -> float:
        """Calcula el porcentaje de una base específica.
        
        Args:
            base (str): La base nucleotídica (A, T, G o C).
        
        Returns:
            float: Porcentaje redondeado a 2 decimales. Retorna 0.0 si
                   sequence_length es 0 para evitar división por cero.
        
        Ejemplo:
            >>> result = FrequencyResult("seq1", 4, {"A": 1, "T": 1, "G": 1, "C": 1}, 0)
            >>> result.get_percentage("A")
            25.0
        """
        if self.sequence_length == 0:
            return 0.0
        return round(
            (self.frequencies[base] / self.sequence_length) * 100, 2
        )


@dataclass
class CleaningResult:
    """Encapsula el resultado de limpiar una secuencia.
    
    Atributos:
        cleaned (str): Secuencia con solo bases válidas (A, T, G, C).
        invalid_chars (Dict[str, int]): Conteos de cada carácter inválido.
        invalid_count (int): Total de caracteres inválidos encontrados.
    """

    cleaned: str
    invalid_chars: Dict[str, int]
    invalid_count: int

# =============================================================================
# FUNCIONES - Procesamiento de archivos FASTA
# =============================================================================


def parse_args(argv=None) -> str:
    """Procesa y valida argumentos de línea de comandos.
    
    Parsea los argumentos de la línea de comandos para obtener la ruta del
    archivo FASTA a procesar. Soporta testing pasando argumentos directamente.
    
    Args:
        argv (list, optional): Lista de argumentos (para testing). Si es None,
                              usa sys.argv. Por defecto None.
    
    Returns:
        str: Ruta del archivo FASTA validada y limpia de espacios.
    
    Raises:
        SystemExit: Si no se proporciona archivo o la ruta está vacía.
    
    Ejemplo:
        >>> ruta = parse_args(["data/sequence.fasta"])
        >>> print(ruta)
        data/sequence.fasta
    """
    parser = argparse.ArgumentParser(
        description=(
            "Calcula la frecuencia de A, T, G y C de un archivo FASTA "
            "con UNA sola secuencia."
        )
    )
    parser.add_argument(
        "fasta",
        help="Archivo FASTA que contiene una sola secuencia."
    )
    args = parser.parse_args(argv)

    # Validar que la ruta no sea vacía o contenga solo espacios
    if not args.fasta or not args.fasta.strip():
        print("Error: la ruta del archivo no puede estar vacía.")
        sys.exit(1)

    return args.fasta.strip()


def read_file(path: str) -> str:
    """Lee archivo FASTA con validaciones robustas.
    
    Abre y lee un archivo de texto asumiendo encoding UTF-8. Realiza múltiples
    validaciones antes de la lectura: existencia, tipo de archivo, tamaño,
    permisos y validez del encoding.
    
    Args:
        path (str): Ruta absoluta o relativa al archivo a leer.
    
    Returns:
        str: Contenido completo del archivo como string en UTF-8.
    
    Raises:
        FileNotFoundError: Si el archivo no existe en la ruta especificada.
        IsADirectoryError: Si la ruta apunta a un directorio, no a un archivo.
        PermissionError: Si no hay permisos de lectura para el archivo.
        ValueError: Si el archivo excede MAX_FILE_SIZE_MB.
        UnicodeDecodeError: Si el archivo no está en encoding UTF-8 válido.
    
    Nota:
        - Tamaño máximo permitido: 100 MB (configurable con MAX_FILE_SIZE_MB)
        - Encoding asumido: UTF-8
        - No apto para archivos binarios
    
    Ejemplo:
        >>> contenido = read_file("data/sequence.fasta")
        >>> ">seq1" in contenido
        True
    """
    # Validar que el archivo existe
    if not os.path.exists(path):
        raise FileNotFoundError(f"El archivo no existe: {path}")

    # Validar que es un archivo, no directorio
    if not os.path.isfile(path):
        raise IsADirectoryError(
            f"La ruta es un directorio, no un archivo: {path}"
        )

    # Validar tamaño del archivo
    file_size_mb = os.path.getsize(path) / (1024 * 1024)
    if file_size_mb > MAX_FILE_SIZE_MB:
        raise ValueError(
            f"El archivo es demasiado grande ({file_size_mb:.1f} MB). "
            f"Máximo: {MAX_FILE_SIZE_MB} MB"
        )

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
            f"El archivo no está en UTF-8 válido: {e.reason}",
        )


def extract_header_and_sequence(fasta_text: str) -> Tuple[str, str]:
    """Extrae encabezado y secuencia de un archivo FASTA.
    
    Parsea un texto en formato FASTA y extrae el header (línea con ">") y la
    secuencia (líneas siguientes concatenadas). Solo procesa la PRIMERA
    secuencia encontrada. Las líneas se convierten a mayúsculas.
    
    Args:
        fasta_text (str): Contenido del archivo FASTA como string.
    
    Returns:
        Tuple[str, str]: Tupla (header, sequence) donde:
            - header: Identificador de la secuencia sin el símbolo ">".
            - sequence: Secuencia concatenada en mayúsculas.
    
    Raises:
        ValueError: En múltiples casos:
            - FASTAFORMAT_EMPTY: Si el archivo está vacío.
            - FASTAFORMAT_INVALID: Si no contiene ">", o header/secuencia vacíos.
    
    Nota:
        - Si hay múltiples secuencias (más de un ">"), imprime aviso y procesa solo la primera.
        - Los saltos de línea dentro de la secuencia se eliminan (estándar FASTA).
        - El header se extrae sin modificar (excepto strip de espacios).
    
    Ejemplo:
        >>> fasta = ">seq1\\nATG\\nCGT\\nA"
        >>> header, seq = extract_header_and_sequence(fasta)
        >>> print(header, seq)
        seq1 ATGCGTA
    """
    # Validar que el archivo no está vacío
    if not fasta_text or not fasta_text.strip():
        raise ValueError("FASTAFORMAT_EMPTY: El archivo está vacío")

    # Validar que contiene ">"
    if ">" not in fasta_text:
        raise ValueError(
            "FASTAFORMAT_INVALID: El archivo no contiene '>'. No es FASTA válido."
        )

    partes = fasta_text.split(">")
    if len(partes) < 2:
        raise ValueError("FASTAFORMAT_EMPTY")

    bloque = partes[1].strip().split("\n")
    header = bloque[0].strip()

    # Validar que el header no es vacío
    if not header:
        raise ValueError(
            "FASTAFORMAT_INVALID: El header está vacío (línea después de '>')."
        )

    sec = "".join(bloque[1:]).strip().upper()

    # Validar que la secuencia no es vacía
    if not sec:
        raise ValueError("FASTAFORMAT_INVALID: No hay secuencia después del header.")

    # Avisar si hay múltiples secuencias
    if fasta_text.count(">") > 1:
        print(f"Aviso: El archivo FASTA contiene {fasta_text.count('>')} secuencias.")
        print("Procesando solo la primera secuencia.")

    return header, sec


def clean_sequence(raw_seq: str, header: str) -> CleaningResult:
    """Filtra bases inválidas de una secuencia.
    
    Procesa una secuencia de ADN y retorna solo las bases nucleotídicas
    válidas (A, T, G, C). Cuenta y reporta caracteres inválidos encontrados.
    
    Args:
        raw_seq (str): Secuencia raw a limpiar (en mayúsculas, típicamente).
        header (str): Identificador de la secuencia (para reportes de error).
    
    Returns:
        CleaningResult: Objeto con:
            - cleaned: Secuencia filtrada (solo A, T, G, C).
            - invalid_chars: Dict con conteos de cada carácter inválido.
            - invalid_count: Total de caracteres inválidos.
    
    Nota:
        - Esta función NO imprime, retorna información para que main() decida.
        - Caracteres inválidos pueden ser: espacios, guiones, N, X, etc.
        - La secuencia se asume ya en mayúsculas.
    
    Ejemplo:
        >>> result = clean_sequence("ATGCNNN---GC", "seq1")
        >>> print(result.cleaned)
        ATGCGC
        >>> print(result.invalid_count)
        6
    """
    seq_limpia_chars = []
    invalid_chars: Dict[str, int] = {}
    invalid_count = 0

    for base in raw_seq:
        if base in NUCLEOTIDE_BASES:
            seq_limpia_chars.append(base)
        else:
            invalid_count += 1
            # Contar ocurrencias de cada carácter inválido
            invalid_chars[base] = invalid_chars.get(base, 0) + 1

    return CleaningResult(
        cleaned="".join(seq_limpia_chars),
        invalid_chars=invalid_chars,
        invalid_count=invalid_count,
    )


def print_cleaning_warnings(header: str, result: CleaningResult) -> None:
    """Imprime advertencias sobre caracteres inválidos encontrados.
    
    Presenta un resumen consolidado de los caracteres inválidos encontrados
    durante la limpieza de la secuencia. Los caracteres especiales se
    describen explícitamente (espacio, tabulador, etc.).
    
    Args:
        header (str): Identificador de la secuencia (para el mensaje).
        result (CleaningResult): Resultado de la limpieza con invalid_chars.
    
    Retorna:
        None: Solo imprime en stdout.
    
    Nota:
        - Solo imprime si result.invalid_count > 0.
        - Los caracteres se ordenan alfabéticamente.
        - Caracteres especiales tienen descripción: espacio, tabulador, etc.
    
    Ejemplo:
        >>> result = CleaningResult("ATGC", {'N': 3, '-': 2}, 5)
        >>> print_cleaning_warnings("seq1", result)
        Aviso: Se encontraron 5 caracteres inválidos en 'seq1':
          - '-': 2 ocurrencia(s)
          - 'N': 3 ocurrencia(s)
    """
    if result.invalid_count > 0:
        print(
            f"Aviso: Se encontraron {result.invalid_count} "
            f"caracteres inválidos en '{header}':"
        )
        for char, count in sorted(result.invalid_chars.items()):
            if char == " ":
                print(f"  - espacio: {count} ocurrencia(s)")
            elif char == "\t":
                print(f"  - tabulador: {count} ocurrencia(s)")
            elif char == "\n":
                print(f"  - salto de línea: {count} ocurrencia(s)")
            else:
                print(f"  - '{char}': {count} ocurrencia(s)")


def calc_frequencies(seq_limpia: str) -> Dict[str, int]:
    """Calcula el conteo de bases nucleotídicas.
    
    Cuenta la cantidad de cada base nucleotídica (A, T, G, C) en la secuencia.
    Esta función contabiliza, no valida - asume input válido.
    
    Args:
        seq_limpia (str): Secuencia limpia (solo A, T, G, C).
    
    Returns:
        Dict[str, int]: Diccionario con conteos:
            {"A": int, "T": int, "G": int, "C": int}
    
    Raises:
        ValueError: Si la secuencia está vacía.
    
    Ejemplo:
        >>> freqs = calc_frequencies("ATGCGTA")
        >>> print(freqs)
        {'A': 2, 'T': 2, 'G': 2, 'C': 1}
    """
    if len(seq_limpia) == 0:
        raise ValueError(
            "CALCULATION_ERROR: La secuencia limpia está vacía. "
            "No se puede calcular frecuencias."
        )

    return {
        "A": seq_limpia.count("A"),
        "T": seq_limpia.count("T"),
        "G": seq_limpia.count("G"),
        "C": seq_limpia.count("C"),
    }


def get_frequency_result(header: str, seq_limpia: str) -> FrequencyResult:
    """Crea un objeto FrequencyResult con datos de análisis.
    
    Actúa como factory function que calcula frecuencias y empaqueta los
    resultados en un objeto FrequencyResult tipado y reutilizable.
    
    Args:
        header (str): Identificador de la secuencia FASTA.
        seq_limpia (str): Secuencia limpia (solo A, T, G, C).
    
    Returns:
        FrequencyResult: Objeto con header, length, frequencies y metadata.
    
    Raises:
        ValueError: Si la secuencia está vacía (propagado de calc_frequencies).
    
    Ejemplo:
        >>> result = get_frequency_result("seq1", "ATGCGTA")
        >>> result.header
        'seq1'
        >>> result.get_percentage("A")
        28.57
    """
    frequencies = calc_frequencies(seq_limpia)
    return FrequencyResult(
        header=header,
        sequence_length=len(seq_limpia),
        frequencies=frequencies,
        invalid_chars_count=0,
    )


def print_frequencies(result: FrequencyResult) -> None:
    """Imprime el análisis de frecuencias en formato legible.
    
    Presenta los datos de análisis de frecuencias en un formato de fácil
    lectura para el usuario. Incluye header, longitud y conteos con
    porcentajes para cada base.
    
    Args:
        result (FrequencyResult): Objeto con datos de análisis.
    
    Retorna:
        None: Solo imprime en stdout.
    
    Nota:
        - Los porcentajes se muestran redondeados a 2 decimales.
        - El orden de bases es siempre: A, T, G, C.
        - Usa el método get_percentage() del resultado.
    
    Ejemplo:
        >>> result = FrequencyResult("seq1", 7, {"A": 2, "T": 2, "G": 2, "C": 1}, 0)
        >>> print_frequencies(result)
        Encabezado: seq1
        Longitud secuencia válida: 7
        Frecuencias:
        A: 2 (28.57%)
        T: 2 (28.57%)
        G: 2 (28.57%)
        C: 1 (14.29%)
    """
    print("Encabezado:", result.header)
    print("Longitud secuencia válida:", result.sequence_length)
    print("Frecuencias:")

    for base in ["A", "T", "G", "C"]:
        count = result.frequencies[base]
        percentage = result.get_percentage(base)
        print(f"{base}: {count} ({percentage}%)")


def main(argv=None) -> None:
    """Orquesta el flujo completo de procesamiento FASTA.
    
    Función principal que coordina todo el proceso:
    1. Parsea argumentos de línea de comandos
    2. Lee y valida archivo FASTA
    3. Extrae header y secuencia
    4. Limpia secuencia de bases inválidas
    5. Calcula frecuencias
    6. Presenta resultados
    
    Todo con manejo robusto de errores específicos para cada etapa.
    
    Args:
        argv (list, optional): Argumentos de línea de comandos (para testing).
                              Si es None, usa sys.argv. Por defecto None.
    
    Retorna:
        None: Imprime resultados en stdout o errores en stderr, luego exit.
    
    Exit codes:
        0: Ejecución exitosa
        1: Error en cualquier etapa (archivo, validación, cálculo, etc.)
    
    Ejemplo:
        >>> main(["data/sequence.fasta"])  # Procesa archivo y imprime
        >>> # O desde línea de comandos:
        >>> # python base_freq.py data/sequence.fasta
    """
    try:
        ruta = parse_args(argv)
    except SystemExit as e:
        sys.exit(e.code)

    # ===== LECTURA Y VALIDACIÓN DE ARCHIVO =====
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

    # ===== EXTRACCIÓN DE HEADER Y SECUENCIA =====
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

    # ===== LIMPIEZA DE SECUENCIA =====
    try:
        cleaning_result = clean_sequence(sec, header)
        seq_limpia = cleaning_result.cleaned
        print_cleaning_warnings(header, cleaning_result)
    except Exception as e:
        print(f"Error al limpiar la secuencia: {e}")
        sys.exit(1)

    # Validar que la secuencia limpia no está vacía
    if len(seq_limpia) == 0:
        print("Error: la secuencia no contiene bases válidas (A,T,G,C).")
        sys.exit(1)

    # ===== CÁLCULO Y PRESENTACIÓN DE RESULTADOS =====
    try:
        result = get_frequency_result(header, seq_limpia)
        print_frequencies(result)
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
    """Punto de entrada del programa.
    
    Solo se ejecuta si el script se llama directamente, no si se importa
    como módulo en otro código.
    """
    main()
