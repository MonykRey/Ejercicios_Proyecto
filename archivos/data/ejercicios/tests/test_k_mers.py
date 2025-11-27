#!/usr/bin/env python3
"""Suite de pruebas unitarias para el contador de k-mers.

Este módulo contiene pruebas exhaustivas para validar la funcionalidad
del programa de conteo de k-mers, incluyendo:
- Validación de secuencias
- Conteo de k-mers
- Formateo de salida
- Manejo de errores

Ejecutar con: pytest test_k_mers.py -v
"""
import pytest
from collections import Counter
import sys
import os

# Agregar el directorio src al path para importar el módulo
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import importlib.util
spec = importlib.util.spec_from_file_location(
    "k_mers",
    os.path.join(os.path.dirname(__file__), '..', 'src', 'k-mers.py')
)
k_mers = importlib.util.module_from_spec(spec)
spec.loader.exec_module(k_mers)


# ============================================================================
# PRUEBAS PARA validate_sequence()
# ============================================================================

class TestValidateSequence:
    """Pruebas para la función validate_sequence()."""

    def test_valid_sequence_uppercase(self):
        """Verificar que acepta secuencias válidas en mayúsculas."""
        result = k_mers.validate_sequence("ATCG")
        assert result == "ATCG"

    def test_valid_sequence_lowercase(self):
        """Verificar que acepta secuencias en minúsculas y las convierte."""
        result = k_mers.validate_sequence("atcg")
        assert result == "ATCG"

    def test_valid_sequence_mixed_case(self):
        """Verificar que normaliza secuencias con mayúsculas y minúsculas."""
        result = k_mers.validate_sequence("AtCg")
        assert result == "ATCG"

    def test_valid_sequence_long(self):
        """Verificar que acepta secuencias largas."""
        long_seq = "ATCGATCGATCGATCGATCG" * 100
        result = k_mers.validate_sequence(long_seq)
        assert result == long_seq

    def test_invalid_sequence_contains_x(self):
        """Verificar que rechaza secuencias con X."""
        with pytest.raises(ValueError) as exc_info:
            k_mers.validate_sequence("ATCGX")
        assert "X" in str(exc_info.value)

    def test_invalid_sequence_contains_n(self):
        """Verificar que rechaza secuencias con N."""
        with pytest.raises(ValueError) as exc_info:
            k_mers.validate_sequence("ATCGN")
        assert "N" in str(exc_info.value)

    def test_invalid_sequence_multiple_invalid_chars(self):
        """Verificar que reporta múltiples caracteres inválidos."""
        with pytest.raises(ValueError) as exc_info:
            k_mers.validate_sequence("ATCGXNZ")
        error_msg = str(exc_info.value)
        assert "X" in error_msg or "N" in error_msg or "Z" in error_msg

    def test_invalid_sequence_empty(self):
        """Verificar que rechaza secuencias vacías."""
        with pytest.raises(ValueError) as exc_info:
            k_mers.validate_sequence("")
        assert "vacía" in str(exc_info.value).lower()

    def test_invalid_sequence_whitespace_only(self):
        """Verificar que rechaza secuencias solo de espacios."""
        with pytest.raises(ValueError):
            k_mers.validate_sequence("   ")

    def test_invalid_type_not_string(self):
        """Verificar que rechaza inputs que no son strings."""
        with pytest.raises(TypeError):
            k_mers.validate_sequence(123)

    def test_invalid_type_none(self):
        """Verificar que rechaza None."""
        with pytest.raises(TypeError):
            k_mers.validate_sequence(None)

    def test_invalid_type_list(self):
        """Verificar que rechaza listas."""
        with pytest.raises(TypeError):
            k_mers.validate_sequence(["A", "T", "C", "G"])

    def test_invalid_sequence_numbers(self):
        """Verificar que rechaza secuencias con números."""
        with pytest.raises(ValueError):
            k_mers.validate_sequence("ATC1G2")

    def test_invalid_sequence_special_chars(self):
        """Verificar que rechaza caracteres especiales."""
        with pytest.raises(ValueError):
            k_mers.validate_sequence("ATC@G")

    def test_all_valid_nucleotides(self):
        """Verificar que acepta todos los nucleótidos válidos."""
        result = k_mers.validate_sequence("AAATTTTCCCCGGGG")
        assert result == "AAATTTTCCCCGGGG"


# ============================================================================
# PRUEBAS PARA count_kmers()
# ============================================================================

class TestCountKmers:
    """Pruebas para la función count_kmers()."""

    def test_basic_count_k2(self):
        """Verificar conteo básico con k=2."""
        result = k_mers.count_kmers("ATCGATCG", 2)
        expected = Counter({'AT': 2, 'TC': 2, 'CG': 2, 'GA': 1})
        assert result == expected

    def test_basic_count_k3(self):
        """Verificar conteo básico con k=3."""
        result = k_mers.count_kmers("ATCGATCG", 3)
        expected = Counter({'ATC': 2, 'TCG': 2, 'CGA': 1, 'GAT': 1})
        assert result == expected

    def test_k_equals_1(self):
        """Verificar conteo de monomeros (k=1)."""
        result = k_mers.count_kmers("ATCGATCG", 1)
        expected = Counter({'A': 2, 'T': 2, 'C': 2, 'G': 2})
        assert result == expected

    def test_k_equals_sequence_length(self):
        """Verificar conteo cuando k = len(seq)."""
        seq = "ATCG"
        result = k_mers.count_kmers(seq, 4)
        expected = Counter({"ATCG": 1})
        assert result == expected

    def test_repetitive_sequence(self):
        """Verificar conteo en secuencias repetitivas."""
        result = k_mers.count_kmers("AAAA", 2)
        expected = Counter({"AA": 3})
        assert result == expected

    def test_no_repetition(self):
        """Verificar conteo en secuencia sin repeticiones."""
        result = k_mers.count_kmers("ATCG", 2)
        expected = Counter({'AT': 1, 'TC': 1, 'CG': 1})
        assert result == expected

    def test_returns_counter(self):
        """Verificar que retorna un objeto Counter."""
        result = k_mers.count_kmers("ATCG", 2)
        assert isinstance(result, Counter)

    def test_counter_most_common_method(self):
        """Verificar que el Counter tiene los métodos correctos."""
        result = k_mers.count_kmers("ATCGATCG", 2)
        most_common = result.most_common(1)
        assert len(most_common) == 1
        assert most_common[0][1] == 2  # Frecuencia máxima

    def test_error_k_is_zero(self):
        """Verificar que rechaza k=0."""
        with pytest.raises(ValueError) as exc_info:
            k_mers.count_kmers("ATCG", 0)
        assert "mayor a 0" in str(exc_info.value)

    def test_error_k_is_negative(self):
        """Verificar que rechaza k negativo."""
        with pytest.raises(ValueError) as exc_info:
            k_mers.count_kmers("ATCG", -5)
        assert "mayor a 0" in str(exc_info.value)

    def test_error_k_greater_than_sequence(self):
        """Verificar que rechaza k > len(seq)."""
        with pytest.raises(ValueError) as exc_info:
            k_mers.count_kmers("AT", 10)
        assert "mayor que" in str(exc_info.value).lower()

    def test_error_k_is_boolean(self):
        """Verificar que rechaza bool como k (aunque bool es subclase de int)."""
        with pytest.raises(TypeError) as exc_info:
            k_mers.count_kmers("ATCG", True)
        assert "entero" in str(exc_info.value)

    def test_error_k_is_float(self):
        """Verificar que rechaza float como k."""
        with pytest.raises(TypeError) as exc_info:
            k_mers.count_kmers("ATCG", 2.5)
        assert "entero" in str(exc_info.value)

    def test_error_k_is_string(self):
        """Verificar que rechaza string como k."""
        with pytest.raises(TypeError) as exc_info:
            k_mers.count_kmers("ATCG", "2")
        assert "entero" in str(exc_info.value)

    def test_long_sequence(self):
        """Verificar conteo en secuencia larga."""
        long_seq = "ATCGATCG" * 1000
        result = k_mers.count_kmers(long_seq, 2)
        assert len(result) == 4
        # "ATCGATCG" repetido 1000 veces = 8000 nucleótidos
        # k-mers de longitud 2 = 7999 totales
        assert result['AT'] == 2000  # Aparece en cada ciclo de "ATCGATCG"
        assert result['TC'] == 2000


# ============================================================================
# PRUEBAS PARA format_output()
# ============================================================================

class TestFormatOutput:
    """Pruebas para la función format_output()."""

    def test_format_output_default_sort(self):
        """Verificar formato de salida con ordenamiento por defecto."""
        kmers = Counter({'AT': 2, 'TC': 2, 'CG': 2, 'GA': 1})
        output = k_mers.format_output(kmers)
        lines = output.split('\n')
        assert lines[0] == "# kmer\tfrequency"
        assert "AT\t2" in output

    def test_format_output_sort_by_frequency(self):
        """Verificar formato con ordenamiento por frecuencia."""
        kmers = Counter({'AT': 2, 'TC': 2, 'CG': 2, 'GA': 1})
        output = k_mers.format_output(kmers, "frequency")
        lines = output.split('\n')
        # Los primeros 3 k-mers deben tener frecuencia 2
        assert "2" in lines[1]
        assert "2" in lines[2]
        assert "2" in lines[3]
        # El último debe tener frecuencia 1
        assert "\t1" in lines[4]

    def test_format_output_sort_by_kmer(self):
        """Verificar formato con ordenamiento alfabético."""
        kmers = Counter({'TC': 2, 'AT': 2, 'GA': 1, 'CG': 2})
        output = k_mers.format_output(kmers, "kmer")
        lines = output.split('\n')
        # Verificar que AT viene antes que CG alfabéticamente
        at_line = next(i for i, l in enumerate(lines) if l.startswith('AT'))
        cg_line = next(i for i, l in enumerate(lines) if l.startswith('CG'))
        ga_line = next(i for i, l in enumerate(lines) if l.startswith('GA'))
        tc_line = next(i for i, l in enumerate(lines) if l.startswith('TC'))
        assert at_line < cg_line < ga_line < tc_line

    def test_format_output_appearance_sort(self):
        """Verificar formato con ordenamiento por aparición."""
        kmers = Counter({'AT': 2, 'TC': 2, 'CG': 2, 'GA': 1})
        output = k_mers.format_output(kmers, "appearance")
        lines = output.split('\n')
        assert "# kmer\tfrequency" in lines[0]

    def test_format_output_invalid_sort(self):
        """Verificar que rechaza criterio de ordenamiento inválido."""
        kmers = Counter({'AT': 2, 'TC': 2})
        with pytest.raises(ValueError) as exc_info:
            k_mers.format_output(kmers, "invalid")
        assert "sort_by" in str(exc_info.value)

    def test_format_output_contains_header(self):
        """Verificar que la salida contiene encabezado."""
        kmers = Counter({'AT': 2})
        output = k_mers.format_output(kmers)
        assert "# kmer" in output

    def test_format_output_tab_separated(self):
        """Verificar que la salida está separada por tabulaciones."""
        kmers = Counter({'AT': 2})
        output = k_mers.format_output(kmers)
        lines = output.split('\n')
        for line in lines[1:]:  # Saltar encabezado
            if line.strip():
                assert '\t' in line


# ============================================================================
# PRUEBAS PARA process_kmer_analysis()
# ============================================================================

class TestProcessKmerAnalysis:
    """Pruebas para la función process_kmer_analysis()."""

    def test_process_analysis_valid_input(self):
        """Verificar procesamiento completo con entrada válida."""
        result = k_mers.process_kmer_analysis("ATCGATCG", 2)
        assert isinstance(result, Counter)
        assert len(result) > 0

    def test_process_analysis_normalizes_sequence(self):
        """Verificar que normaliza secuencias en minúsculas."""
        result1 = k_mers.process_kmer_analysis("atcgatcg", 2)
        result2 = k_mers.process_kmer_analysis("ATCGATCG", 2)
        assert result1 == result2

    def test_process_analysis_invalid_sequence(self):
        """Verificar que propaga errores de secuencia inválida."""
        with pytest.raises(ValueError):
            k_mers.process_kmer_analysis("ATCGX", 2)

    def test_process_analysis_invalid_k(self):
        """Verificar que propaga errores de k inválido."""
        with pytest.raises(ValueError):
            k_mers.process_kmer_analysis("ATCG", 0)


# ============================================================================
# PRUEBAS DE INTEGRACIÓN
# ============================================================================

class TestIntegration:
    """Pruebas de integración del flujo completo."""

    def test_complete_workflow(self):
        """Verificar el flujo completo: validar -> contar -> formatear."""
        seq = k_mers.validate_sequence("atcgatcg")
        kmers = k_mers.count_kmers(seq, 2)
        output = k_mers.format_output(kmers)
        
        assert "# kmer" in output
        assert "AT" in output
        assert "TC" in output

    def test_process_and_format(self):
        """Verificar flujo: procesar -> formatear."""
        kmers = k_mers.process_kmer_analysis("ATCGATCG", 2)
        output = k_mers.format_output(kmers, "frequency")
        
        lines = output.split('\n')
        assert len(lines) >= 5  # Encabezado + 4 k-mers

    def test_different_k_values(self):
        """Verificar que diferentes valores de k producen resultados diferentes."""
        seq = "ATCGATCGATCGATCGATCGATCG"  # Secuencia sin repetición del patrón
        kmers_k2 = k_mers.count_kmers(seq, 2)
        kmers_k3 = k_mers.count_kmers(seq, 3)
        
        # Con k2 tenemos: AT, TC, CG, GA, AT, TC, ...
        # Con k3 tenemos: ATC, TCG, CGA, GAT, ATC, TCG, ...
        # Ambos pueden tener la misma cantidad de k-mers únicos
        # Mejor: verificar que el total de k-mers es diferente
        total_k2 = sum(kmers_k2.values())
        total_k3 = sum(kmers_k3.values())
        assert total_k2 > total_k3  # Hay más 2-mers que 3-mers

    def test_sequence_properties(self):
        """Verificar propiedades matemáticas de k-mers."""
        seq = "ATCGATCGATCG"
        k = 2
        kmers = k_mers.count_kmers(seq, k)
        
        # Suma de frecuencias = len(seq) - k + 1
        total = sum(kmers.values())
        expected_total = len(seq) - k + 1
        assert total == expected_total

    def test_sequence_length_property(self):
        """Verificar que los k-mers tienen la longitud correcta."""
        kmers = k_mers.count_kmers("ATCGATCG", 3)
        for kmer in kmers.keys():
            assert len(kmer) == 3


# ============================================================================
# PRUEBAS DE CASOS EXTREMOS (EDGE CASES)
# ============================================================================

class TestEdgeCases:
    """Pruebas de casos extremos y situaciones especiales."""

    def test_single_nucleotide_sequence(self):
        """Verificar conteo con secuencia de un solo nucleótido."""
        result = k_mers.count_kmers("A", 1)
        assert result == Counter({'A': 1})

    def test_homopolymer_sequence(self):
        """Verificar conteo en secuencia homopólimica (todos iguales)."""
        result = k_mers.count_kmers("AAAA", 2)
        assert len(result) == 1
        assert result['AA'] == 3

    def test_alternating_sequence(self):
        """Verificar conteo en secuencia alternada."""
        result = k_mers.count_kmers("ATATAT", 2)
        # ATATAT tiene k-mers: AT(0-1), TA(1-2), AT(2-3), TA(3-4), AT(4-5)
        # Entonces: AT aparece 3 veces, TA aparece 2 veces
        assert result['AT'] == 3
        assert result['TA'] == 2

    def test_palindromic_sequence(self):
        """Verificar conteo en secuencia palindrómica."""
        result = k_mers.count_kmers("ATCGCGAT", 2)
        assert isinstance(result, Counter)

    def test_very_long_sequence(self):
        """Verificar manejo de secuencias muy largas."""
        long_seq = "ATCG" * 10000
        result = k_mers.count_kmers(long_seq, 2)
        assert result['AT'] == 10000
        assert result['TC'] == 10000
        assert result['CG'] == 10000
        assert result['GA'] == 9999

    def test_high_k_value(self):
        """Verificar conteo con k cercano a la longitud de secuencia."""
        seq = "ATCGATCGATCGATCG"
        result = k_mers.count_kmers(seq, len(seq) - 1)
        assert len(result) == 2

    def test_k_exactly_sequence_length(self):
        """Verificar que k = len(seq) produce un único k-mer."""
        seq = "ATCGATCG"
        result = k_mers.count_kmers(seq, len(seq))
        assert len(result) == 1
        assert result[seq] == 1


# ============================================================================
# SUITE DE PRUEBAS CON PARÁMETROS
# ============================================================================

class TestParametrized:
    """Pruebas parametrizadas para validar múltiples casos."""

    @pytest.mark.parametrize("seq,k,expected_count", [
        ("ATCG", 1, 4),
        ("ATCG", 2, 3),
        ("ATCGATCG", 2, 7),
        ("AAAA", 2, 3),
        ("ATCGATCG", 3, 6),
    ])
    def test_kmer_count_properties(self, seq, k, expected_count):
        """Verificar que el número total de k-mers es correcto."""
        result = k_mers.count_kmers(seq, k)
        assert sum(result.values()) == expected_count

    @pytest.mark.parametrize("invalid_char", ["X", "N", "U", "1", "!", " "])
    def test_invalid_nucleotides(self, invalid_char):
        """Verificar que todos los caracteres inválidos son rechazados."""
        with pytest.raises(ValueError):
            k_mers.validate_sequence(f"ATC{invalid_char}G")

    @pytest.mark.parametrize("sort_option", ["appearance", "frequency", "kmer"])
    def test_all_sort_options(self, sort_option):
        """Verificar que todas las opciones de ordenamiento funcionan."""
        kmers = Counter({'AT': 2, 'TC': 2, 'CG': 2, 'GA': 1})
        output = k_mers.format_output(kmers, sort_option)
        assert "# kmer" in output


if __name__ == "__main__":
    # Ejecutar las pruebas con pytest si se ejecuta directamente
    pytest.main([__file__, "-v", "--tb=short"])
