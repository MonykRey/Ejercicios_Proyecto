#!/usr/bin/env python3
"""
Suite de pruebas unitarias para gene-expression.py

Utiliza pytest para validar todas las funciones del módulo de filtrado de genes.
Prueba casos normales, casos límite y manejo de errores.

Estructura:
    - TestLoadExpressionTable: Pruebas para carga de archivos
    - TestFilterGenes: Pruebas para filtrado de genes
    - TestValidateThreshold: Pruebas para validación de threshold
    - TestBuildParser: Pruebas para parser de argumentos
"""

import pytest
import pandas as pd
from pathlib import Path
import sys
import os

# Agregar src al path para importar el módulo
current_dir = Path(__file__).parent
src_dir = current_dir.parent / "src"
sys.path.insert(0, str(src_dir))

# Cambiar al directorio del proyecto para que las rutas relativas funcionen
os.chdir(str(current_dir.parent))

from gene_expression import (
    load_expression_table,
    filter_genes,
    validate_threshold,
    build_parser,
    print_results,
)

# Ruta a los datos de prueba
TEST_DATA_DIR = Path(__file__).parent / "test_data"


class TestLoadExpressionTable:
    """Pruebas para la función load_expression_table()"""

    def test_load_valid_file(self):
        """Test: cargar archivo válido con datos correctos"""
        df = load_expression_table(str(TEST_DATA_DIR / "valid.tsv"))

        # Verificar que se cargó correctamente
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 5
        assert "gene" in df.columns
        assert "expression" in df.columns

    def test_load_valid_file_has_correct_types(self):
        """Test: verificar que los tipos de datos son correctos"""
        df = load_expression_table(str(TEST_DATA_DIR / "valid.tsv"))

        # Expression debe ser numérico
        assert pd.api.types.is_numeric_dtype(df["expression"])
        assert pd.api.types.is_object_dtype(df["gene"])

    def test_load_valid_file_sorted(self):
        """Test: verificar que los genes están presentes"""
        df = load_expression_table(str(TEST_DATA_DIR / "valid.tsv"))
        genes = df["gene"].tolist()

        assert "g1" in genes
        assert "g2" in genes
        assert "g3" in genes

    def test_file_not_found(self):
        """Test: lanzar excepción cuando archivo no existe"""
        with pytest.raises(FileNotFoundError):
            load_expression_table(str(TEST_DATA_DIR / "nonexistent.tsv"))

    def test_empty_file(self):
        """Test: lanzar excepción para archivo vacío"""
        with pytest.raises(ValueError, match="vacío"):
            load_expression_table(str(TEST_DATA_DIR / "empty.tsv"))

    def test_wrong_columns(self):
        """Test: lanzar excepción si columnas son incorrectas"""
        with pytest.raises(ValueError, match="columnas"):
            load_expression_table(str(TEST_DATA_DIR / "wrong_columns.tsv"))

    def test_invalid_values_cleaned(self, capsys):
        """Test: limpiar valores inválidos y mostrar advertencia"""
        df = load_expression_table(str(TEST_DATA_DIR / "invalid_values.tsv"))

        # Verificar que se eliminaron filas inválidas
        captured = capsys.readouterr()
        assert "Advertencia" in captured.out
        assert df.empty is False  # Al menos algunos datos válidos
        assert len(df) >= 1  # g1 y g3 deberían estar presentes


class TestFilterGenes:
    """Pruebas para la función filter_genes()"""

    @pytest.fixture
    def sample_df(self):
        """Fixture: crear DataFrame de prueba"""
        return pd.DataFrame({
            "gene": ["g1", "g2", "g3", "g4", "g5"],
            "expression": [10.5, 5.2, 20.8, 15.3, 3.1]
        })

    def test_filter_threshold_zero(self, sample_df):
        """Test: con threshold 0, retorna todos los genes"""
        result = filter_genes(sample_df, 0)
        assert len(result) == 5

    def test_filter_threshold_10(self, sample_df):
        """Test: con threshold 10, retorna genes >= 10"""
        result = filter_genes(sample_df, 10)

        # Genes esperados: g1 (10.5), g3 (20.8), g4 (15.3)
        expected_genes = ["g1", "g3", "g4"]
        actual_genes = result["gene"].tolist()

        assert len(result) == 3
        assert set(actual_genes) == set(expected_genes)

    def test_filter_threshold_high(self, sample_df):
        """Test: con threshold alto, retorna pocos genes"""
        result = filter_genes(sample_df, 20)

        # Solo g3 tiene expresión >= 20
        assert len(result) == 1
        assert result["gene"].iloc[0] == "g3"

    def test_filter_returns_sorted(self, sample_df):
        """Test: genes retornados están ordenados alfabéticamente"""
        result = filter_genes(sample_df, 5)
        genes = result["gene"].tolist()

        # Verificar que está ordenado
        assert genes == sorted(genes)

    def test_filter_no_results(self, sample_df):
        """Test: threshold muy alto retorna vacío"""
        result = filter_genes(sample_df, 100)
        assert result.empty

    def test_filter_preserves_expression(self, sample_df):
        """Test: verificar que los valores de expression se preservan"""
        result = filter_genes(sample_df, 10)

        # g1 debe tener expresión 10.5
        g1_row = result[result["gene"] == "g1"]
        assert g1_row["expression"].iloc[0] == 10.5


class TestValidateThreshold:
    """Pruebas para la función validate_threshold()"""

    def test_validate_positive_threshold(self):
        """Test: acepta threshold positivo"""
        result = validate_threshold(10.5)
        assert result == 10.5

    def test_validate_zero_threshold(self):
        """Test: acepta threshold cero"""
        result = validate_threshold(0.0)
        assert result == 0.0

    def test_validate_large_threshold(self):
        """Test: acepta threshold muy grande"""
        result = validate_threshold(1000000.0)
        assert result == 1000000.0

    def test_validate_negative_threshold_raises_error(self):
        """Test: rechaza threshold negativo"""
        with pytest.raises(ValueError, match="negativo"):
            validate_threshold(-5.0)

    def test_validate_small_negative_threshold_raises_error(self):
        """Test: rechaza threshold negativo pequeño"""
        with pytest.raises(ValueError, match="negativo"):
            validate_threshold(-0.1)

    def test_validate_float_threshold(self):
        """Test: acepta threshold con decimales"""
        result = validate_threshold(3.14159)
        assert result == 3.14159


class TestBuildParser:
    """Pruebas para la función build_parser()"""

    def test_parser_created(self):
        """Test: parser se crea correctamente"""
        parser = build_parser()
        assert parser is not None

    def test_parser_has_file_argument(self):
        """Test: parser tiene argumento 'file'"""
        parser = build_parser()
        args = parser.parse_args(["data.tsv"])

        assert hasattr(args, "file")
        assert args.file == "data.tsv"

    def test_parser_has_threshold_argument(self):
        """Test: parser tiene argumento 'threshold'"""
        parser = build_parser()
        args = parser.parse_args(["data.tsv", "-t", "5.5"])

        assert hasattr(args, "threshold")
        assert args.threshold == 5.5

    def test_parser_threshold_default(self):
        """Test: threshold tiene valor por defecto 0.0"""
        parser = build_parser()
        args = parser.parse_args(["data.tsv"])

        assert args.threshold == 0.0

    def test_parser_threshold_long_form(self):
        """Test: argumento threshold funciona con forma larga"""
        parser = build_parser()
        args = parser.parse_args(["data.tsv", "--threshold", "10.0"])

        assert args.threshold == 10.0

    def test_parser_threshold_type_conversion(self):
        """Test: threshold se convierte a float automáticamente"""
        parser = build_parser()
        args = parser.parse_args(["data.tsv", "-t", "15"])

        assert isinstance(args.threshold, float)
        assert args.threshold == 15.0

    def test_parser_invalid_threshold(self):
        """Test: parser rechaza threshold no numérico"""
        parser = build_parser()

        with pytest.raises(SystemExit):
            parser.parse_args(["data.tsv", "-t", "invalid"])


class TestIntegration:
    """Pruebas de integración end-to-end"""

    def test_full_workflow(self):
        """Test: flujo completo de carga, filtrado y validación"""
        # Cargar archivo
        df = load_expression_table(str(TEST_DATA_DIR / "valid.tsv"))

        # Validar threshold
        threshold = validate_threshold(10.0)

        # Filtrar genes
        filtered = filter_genes(df, threshold)

        # Verificar resultados
        assert len(filtered) > 0
        assert all(filtered["expression"] >= threshold)
        assert filtered["gene"].tolist() == sorted(filtered["gene"].tolist())

    def test_workflow_with_zero_threshold(self):
        """Test: flujo completo con threshold 0"""
        df = load_expression_table(str(TEST_DATA_DIR / "valid.tsv"))
        threshold = validate_threshold(0.0)
        filtered = filter_genes(df, threshold)

        # Con threshold 0, retorna todos
        assert len(filtered) == len(df)

    def test_workflow_with_no_results(self):
        """Test: flujo cuando no hay genes que cumplen criterio"""
        df = load_expression_table(str(TEST_DATA_DIR / "valid.tsv"))
        threshold = validate_threshold(1000.0)
        filtered = filter_genes(df, threshold)

        # Sin resultados
        assert filtered.empty

    def test_parser_workflow(self):
        """Test: parsing de argumentos funciona correctamente"""
        parser = build_parser()
        args = parser.parse_args([
            str(TEST_DATA_DIR / "valid.tsv"),
            "-t", "10.0"
        ])

        # Verificar que se parseó correctamente
        assert args.file == str(TEST_DATA_DIR / "valid.tsv")
        assert args.threshold == 10.0


class TestEdgeCases:
    """Pruebas para casos límite y especiales"""

    def test_single_gene(self):
        """Test: archivo con un solo gen"""
        df = pd.DataFrame({
            "gene": ["g1"],
            "expression": [10.0]
        })

        filtered = filter_genes(df, 5.0)
        assert len(filtered) == 1
        assert filtered["gene"].iloc[0] == "g1"

    def test_duplicate_genes(self):
        """Test: manejo de genes duplicados"""
        df = pd.DataFrame({
            "gene": ["g1", "g1", "g2"],
            "expression": [10.0, 15.0, 5.0]
        })

        filtered = filter_genes(df, 8.0)
        # Ambas instancias de g1 deberían incluirse
        assert len(filtered) == 2

    def test_genes_with_special_characters(self):
        """Test: genes con caracteres especiales"""
        df = pd.DataFrame({
            "gene": ["TP53", "BRCA-1", "HER2/neu"],
            "expression": [10.0, 15.0, 20.0]
        })

        filtered = filter_genes(df, 5.0)
        assert len(filtered) == 3

    def test_very_small_expression_values(self):
        """Test: valores de expresión muy pequeños"""
        df = pd.DataFrame({
            "gene": ["g1", "g2", "g3"],
            "expression": [0.00001, 0.00002, 0.00003]
        })

        filtered = filter_genes(df, 0.000015)
        assert len(filtered) == 2  # g2 y g3

    def test_very_large_expression_values(self):
        """Test: valores de expresión muy grandes"""
        df = pd.DataFrame({
            "gene": ["g1", "g2"],
            "expression": [1e10, 1e11]
        })

        filtered = filter_genes(df, 5e10)
        assert len(filtered) == 1
        assert filtered["gene"].iloc[0] == "g2"


if __name__ == "__main__":
    # Ejecutar pruebas con pytest si se corre directamente
    pytest.main([__file__, "-v", "--tb=short"])
