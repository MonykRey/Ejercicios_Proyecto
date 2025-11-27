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

Autores:
    Proyecto Bioinformática

Versión:
    1.0
"""

import argparse
import pandas as pd


def load_expression_table(path):
    """
    Carga un archivo TSV con columnas 'gene' y 'expression'.

    Lee un archivo de valores separados por tabulaciones (TSV) que contiene
    datos de expresión génica. Realiza validaciones y limpieza de datos.

    Args:
        path (str): Ruta al archivo TSV.

    Returns:
        pd.DataFrame: DataFrame con columnas 'gene' y 'expression', sin filas
                      con valores NaN en expression.

    Raises:
        ValueError: Si el archivo no contiene las columnas 'gene' y 'expression'.
        FileNotFoundError: Si el archivo no existe en la ruta especificada.

    Example:
        >>> df = load_expression_table('data.tsv')
        >>> print(df.head())
            gene  expression
        0  BRCA1         12.0
        1  TP53          8.5
    """
    # Leer archivo TSV con pandas
    df = pd.read_csv(path, sep="\t") 

    # Validación básica de columnas requeridas
    if "gene" not in df.columns or "expression" not in df.columns:
        raise ValueError("El archivo debe tener columnas 'gene' y 'expression'.")

    # Convertir expresión a numérico, valores inválidos se convierten en NaN
    df["expression"] = pd.to_numeric(df["expression"], errors="coerce")

    # Eliminar filas con NaN en expression (datos incompletos)
    df = df.dropna(subset=["expression"])

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


def main():
    """
    Función principal que orquesta el flujo del programa.

    1. Parsea los argumentos de línea de comandos
    2. Carga el archivo TSV de expresión génica
    3. Filtra los genes según el threshold
    4. Imprime los resultados ordenados alfabéticamente

    Si no hay genes que cumplan el criterio, imprime un mensaje informativo.
    """
    # Construir parser y parsear argumentos
    parser = build_parser()
    args = parser.parse_args()

    # Cargar datos del archivo TSV
    df = load_expression_table(args.file)

    # Obtener threshold desde argumentos
    threshold = args.threshold

    # Filtrar genes con expresión >= threshold
    filtered = filter_genes(df, threshold)

    # Mostrar resultados o mensaje de vacío
    if filtered.empty:
        print("No se encontraron genes por encima del threshold.")
        return

    print("Genes filtrados:")
    for gene in filtered["gene"].tolist():
        print(gene)


if __name__ == "__main__":
    main()
