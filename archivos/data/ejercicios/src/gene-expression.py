#!/usr/bin/env python3
"""
Filtrador de genes por nivel de expresión.

Este módulo filtra un archivo TSV de datos de expresión génica basándose en
un umbral (threshold) especificado por el usuario. Utiliza pandas para la
manipulación eficiente de datos tabulares.

Funcionalidad:
    - Lee archivos TSV con columnas 'gene' y 'expression'
    - Valida que los datos de expresión sean numéricos
    - Filtra genes cuya expresión sea >= threshold
    - Imprime genes filtrados en orden alfabético

Ejemplo de uso:
    $ python3 gene-expression.py data.tsv -t 10.5
    Genes filtrados:
    BRCA1
    TP53

Requisitos:
    - pandas: Para lectura y manipulación de datos tabulares
    - Python 3.6+

Autor:
    Monica Reyes Ramírez

Versión:
    1.0
"""

import argparse
import pandas as pd

# Constantes de configuración
DEFAULT_THRESHOLD = 0.0
SEPARATOR = "\t"
EMPTY_MESSAGE = "No se encontraron genes con expresión >= {threshold}."
HEADER_MESSAGE = "Genes filtrados (threshold: {threshold}):"
TOTAL_MESSAGE = "Total: {count} genes\n"


def load_expression_table(path):
    """
    Carga un archivo TSV con columnas 'gene' y 'expression'.

    Lee un archivo de valores separados por tabulaciones (TSV) que contiene
    datos de expresión génica. Realiza validaciones y limpieza de datos,
    con advertencias sobre filas eliminadas.

    Args:
        path (str): Ruta al archivo TSV.

    Returns:
        pd.DataFrame: DataFrame con columnas 'gene' y 'expression', sin filas
                      con valores NaN en expression.

    Raises:
        ValueError: Si el archivo no contiene las columnas requeridas,
                    si está vacío, o si no hay datos válidos después de limpieza.
        FileNotFoundError: Si el archivo no existe en la ruta especificada.

    Example:
        >>> df = load_expression_table('data.tsv')
        >>> print(df.head())
            gene  expression
        0  BRCA1         12.0
        1  TP53          8.5
    """
    # Leer archivo TSV con pandas
    df = pd.read_csv(path, sep=SEPARATOR)

    # Validación básica de columnas requeridas
    if "gene" not in df.columns or "expression" not in df.columns:
        raise ValueError("El archivo debe tener columnas 'gene' y 'expression'.")

    # Verificar que el archivo no está vacío
    if df.empty:
        raise ValueError("El archivo TSV está vacío.")

    # Convertir expresión a numérico, valores inválidos se convierten en NaN
    df["expression"] = pd.to_numeric(df["expression"], errors="coerce")

    # Contar filas antes de eliminar NaN
    filas_antes = len(df)
    df = df.dropna(subset=["expression"])
    filas_eliminadas = filas_antes - len(df)

    # Advertencia si se eliminaron filas
    if filas_eliminadas > 0:
        print(f"⚠️  Advertencia: Se eliminaron {filas_eliminadas} filas con valores inválidos.")

    # Verificar que quedan datos válidos después de limpieza
    if df.empty:
        raise ValueError("No hay datos válidos después de la limpieza.")

    return df


def filter_genes(df, threshold):
    """
    Filtra genes con expresión mayor o igual al threshold especificado.

    Selecciona del DataFrame solo aquellos genes cuyo nivel de expresión
    sea mayor o igual al umbral (threshold) proporcionado, y los ordena
    alfabéticamente por nombre de gen.

    Args:
        df (pd.DataFrame): DataFrame con columnas 'gene' y 'expression'.
        threshold (float): Umbral mínimo de expresión para el filtrado.

    Returns:
        pd.DataFrame: Subconjunto del DataFrame original con genes filtrados
                      y ordenados alfabéticamente por nombre de gen.

    Example:
        >>> filtered = filter_genes(df, threshold=5.0)
        >>> print(filtered)
            gene  expression
        1  BRCA1        12.0
        3  EGFR         10.1
    """
    # Filtrar genes con expresión mayor o igual al threshold
    filtered = df[df["expression"] >= threshold]

    # Ordenar alfabéticamente por gene para mejor legibilidad
    filtered = filtered.sort_values("gene")

    return filtered


def validate_threshold(threshold):
    """
    Valida que el threshold sea un número válido y no negativo.

    Args:
        threshold (float): Valor del threshold a validar.

    Returns:
        float: El threshold validado.

    Raises:
        ValueError: Si el threshold es negativo.

    Example:
        >>> validate_threshold(5.0)
        5.0
        >>> validate_threshold(-1.0)
        Traceback (most recent call last):
        ...
        ValueError: El threshold no puede ser negativo.
    """
    if threshold < 0:
        raise ValueError("El threshold no puede ser negativo.")
    return threshold


def build_parser():
    """
    Construye y configura el parser de argumentos de línea de comandos.

    Define los argumentos esperados por el programa:
    - archivo TSV: posicional, requerido
    - threshold: opcional, con valor por defecto 0.0

    Returns:
        argparse.ArgumentParser: Parser configurado y listo para usar.

    Example:
        >>> parser = build_parser()
        >>> args = parser.parse_args(['data.tsv', '-t', '5.0'])
        >>> print(args.threshold)
        5.0
    """
    parser = argparse.ArgumentParser(
        description="Filtra genes por expresión usando un archivo TSV y pandas.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Ejemplo:\n  python3 gene-expression.py data.tsv -t 10.5"
    )

    parser.add_argument(
        "file",
        help="Archivo TSV con columnas 'gene' y 'expression'."
    )

    # Argumento threshold como número flotante para operaciones matemáticas
    parser.add_argument(
        "-t",
        "--threshold",
        type=float,
        default=0.0,
        help="Umbral mínimo de expresión. Por defecto: 0.0 (ej. 10.5)."
    )

    return parser


def print_results(filtered, threshold):
    """
    Imprime los genes filtrados de forma clara y ordenada.

    Muestra un encabezado con el threshold usado y el total de genes encontrados,
    seguido por la lista de genes en orden alfabético. Si no hay resultados,
    muestra un mensaje informativo.

    Args:
        filtered (pd.DataFrame): DataFrame con genes filtrados.
        threshold (float): Valor del threshold utilizado en el filtrado.

    Example:
        >>> print_results(filtered_df, 5.0)
        Genes filtrados (threshold: 5.0):
        Total: 3 genes

          - BRCA1
          - TP53
          - MYC
    """
    if filtered.empty:
        print(EMPTY_MESSAGE.format(threshold=threshold))
        return

    print(HEADER_MESSAGE.format(threshold=threshold))
    print(TOTAL_MESSAGE.format(count=len(filtered)))
    for gene in filtered["gene"].tolist():
        print(f"  - {gene}")


def main():
    """
    Función principal que orquesta el flujo del programa.

    Secuencia de operaciones:
        1. Parsea los argumentos de línea de comandos
        2. Carga el archivo TSV de expresión génica
        3. Valida el threshold proporcionado
        4. Filtra los genes según el threshold
        5. Imprime los resultados ordenados alfabéticamente

    Manejo de errores:
        - FileNotFoundError: Archivo no encontrado
        - ValueError: Columnas inválidas, datos vacíos o threshold negativo
        - Exception: Errores inesperados
    """
    parser = build_parser()
    args = parser.parse_args()

    try:
        # Cargar datos del archivo TSV
        print(f"Cargando archivo: {args.file}")
        df = load_expression_table(args.file)
        print(f"✓ Archivo cargado correctamente ({len(df)} genes).\n")

        # Validar y obtener threshold
        threshold = validate_threshold(args.threshold)

        # Filtrar genes con expresión >= threshold
        filtered = filter_genes(df, threshold)

        # Mostrar resultados
        print_results(filtered, threshold)

    except FileNotFoundError as e:
        print(f" Error: El archivo '{args.file}' no existe.")
        print(f"   Detalle: {e}")
        exit(1)

    except ValueError as e:
        print(f" Error de validación: {e}")
        exit(1)

    except Exception as e:
        print(f"Error inesperado: {e}")
        exit(1)


if __name__ == "__main__":
    main()
