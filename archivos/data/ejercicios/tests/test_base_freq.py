#!/usr/bin/env python3
# tests/test_base_freq.py

import pytest
import sys
import os
from io import StringIO
from pathlib import Path

# Agregar src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import base_freq


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def tmp_fasta_file(tmp_path):
    """Crea archivo FASTA temporal válido."""
    fasta_file = tmp_path / "test.fasta"
    fasta_file.write_text(">seq1\nATGCGTA\n")
    return str(fasta_file)


@pytest.fixture
def tmp_fasta_invalid_chars(tmp_path):
    """Crea archivo FASTA con caracteres inválidos."""
    fasta_file = tmp_path / "test_invalid.fasta"
    fasta_file.write_text(">seq1\nATGCNNN---GCT\n")
    return str(fasta_file)


# ============================================================================
# TEST: parse_args()
# ============================================================================

class TestParseArgs:
    """Pruebas para parse_args()."""
    
    def test_parse_args_valid(self, tmp_fasta_file):
        """Debe retornar la ruta válida."""
        result = base_freq.parse_args([tmp_fasta_file])
        assert result == tmp_fasta_file
    
    def test_parse_args_empty_string(self):
        """Debe fallar con string vacío."""
        with pytest.raises(SystemExit):
            base_freq.parse_args([""])


# ============================================================================
# TEST: read_file()
# ============================================================================

class TestReadFile:
    """Pruebas para read_file()."""
    
    def test_read_file_valid(self, tmp_fasta_file):
        """Debe leer archivo válido."""
        content = base_freq.read_file(tmp_fasta_file)
        assert ">seq1" in content
        assert "ATGCGTA" in content
    
    def test_read_file_nonexistent(self):
        """Debe lanzar FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            base_freq.read_file("/nonexistent/file.fasta")
    
    def test_read_file_is_directory(self, tmp_path):
        """Debe lanzar IsADirectoryError."""
        with pytest.raises(IsADirectoryError):
            base_freq.read_file(str(tmp_path))


# ============================================================================
# TEST: extract_header_and_sequence()
# ============================================================================

class TestExtractHeaderAndSequence:
    """Pruebas para extract_header_and_sequence()."""
    
    def test_extract_valid(self):
        """Debe extraer correctamente."""
        fasta_text = ">seq1\nATGCGTA\n"
        header, seq = base_freq.extract_header_and_sequence(fasta_text)
        assert header == "seq1"
        assert seq == "ATGCGTA"
    
    def test_extract_multiple_lines(self):
        """Debe concatenar múltiples líneas."""
        fasta_text = ">seq1\nATG\nCGT\nA\n"
        header, seq = base_freq.extract_header_and_sequence(fasta_text)
        assert header == "seq1"
        assert seq == "ATGCGTA"
    
    def test_extract_empty_file(self):
        """Debe fallar si está vacío."""
        with pytest.raises(ValueError):
            base_freq.extract_header_and_sequence("")
    
    def test_extract_no_header(self):
        """Debe fallar sin '>'."""
        with pytest.raises(ValueError):
            base_freq.extract_header_and_sequence("ATGC\n")
    
    def test_extract_empty_sequence(self):
        """Debe fallar sin secuencia."""
        with pytest.raises(ValueError):
            base_freq.extract_header_and_sequence(">seq1\n")
    
    def test_extract_empty_header(self):
        """Debe fallar si header vacío."""
        with pytest.raises(ValueError):
            base_freq.extract_header_and_sequence(">\nATGC\n")


# ============================================================================
# TEST: clean_sequence() - Retorna CleaningResult
# ============================================================================

class TestCleanSequence:
    """Pruebas para clean_sequence()."""
    
    def test_clean_valid_sequence(self):
        """Debe retornar secuencia limpia."""
        result = base_freq.clean_sequence("ATGCGTA", "seq1")
        assert result.cleaned == "ATGCGTA"
        assert result.invalid_count == 0
        assert len(result.invalid_chars) == 0
    
    def test_clean_with_invalid_chars(self):
        """Debe filtrar y contar inválidos."""
        result = base_freq.clean_sequence("ATGCNNN---GCT", "seq1")
        assert result.cleaned == "ATGCGCT"
        assert result.invalid_count == 6
        assert 'N' in result.invalid_chars
        assert '-' in result.invalid_chars
    
    def test_clean_with_spaces(self):
        """Debe filtrar espacios."""
        result = base_freq.clean_sequence("ATG C GTA", "seq1")
        assert result.cleaned == "ATGCGTA"
        assert result.invalid_count == 2
        assert ' ' in result.invalid_chars
    
    def test_clean_empty_result(self):
        """Debe retornar vacío si todo es inválido."""
        result = base_freq.clean_sequence("NNN---", "seq1")
        assert result.cleaned == ""
        assert result.invalid_count == 6


# ============================================================================
# TEST: calc_frequencies()
# ============================================================================

class TestCalcFrequencies:
    """Pruebas para calc_frequencies()."""
    
    def test_calc_simple(self):
        """Debe calcular conteos correctamente."""
        freqs = base_freq.calc_frequencies("ATGCGTA")
        assert freqs["A"] == 2
        assert freqs["T"] == 2
        assert freqs["G"] == 2
        assert freqs["C"] == 1
    
    def test_calc_single_base(self):
        """Debe calcular cuando hay solo una base."""
        freqs = base_freq.calc_frequencies("AAAA")
        assert freqs["A"] == 4
        assert freqs["T"] == 0
        assert freqs["G"] == 0
        assert freqs["C"] == 0
    
    def test_calc_empty_sequence(self):
        """Debe fallar con secuencia vacía."""
        with pytest.raises(ValueError):
            base_freq.calc_frequencies("")


# ============================================================================
# TEST: get_frequency_result()
# ============================================================================

class TestGetFrequencyResult:
    """Pruebas para get_frequency_result()."""
    
    def test_get_result_valid(self):
        """Debe retornar FrequencyResult válido."""
        result = base_freq.get_frequency_result("seq1", "ATGCGTA")
        assert result.header == "seq1"
        assert result.sequence_length == 7
        assert result.frequencies["A"] == 2
        assert isinstance(result, base_freq.FrequencyResult)
    
    def test_get_percentage(self):
        """Debe calcular porcentajes correctamente."""
        result = base_freq.get_frequency_result("seq1", "ATGCGTA")
        assert result.get_percentage("A") == 28.57
        assert result.get_percentage("T") == 28.57
        assert result.get_percentage("G") == 28.57
        assert result.get_percentage("C") == 14.29


# ============================================================================
# TEST: print_frequencies()
# ============================================================================

class TestPrintFrequencies:
    """Pruebas para print_frequencies()."""
    
    def test_print_output(self, capsys):
        """Debe imprimir en formato correcto."""
        result = base_freq.get_frequency_result("seq1", "ATGCGTA")
        base_freq.print_frequencies(result)
        
        captured = capsys.readouterr()
        assert "seq1" in captured.out
        assert "7" in captured.out
        assert "Frecuencias:" in captured.out
        assert "A: 2 (28.57%)" in captured.out
        assert "T: 2 (28.57%)" in captured.out
        assert "G: 2 (28.57%)" in captured.out
        assert "C: 1 (14.29%)" in captured.out


# ============================================================================
# TEST: main() - Integración completa
# ============================================================================

class TestMainIntegration:
    """Pruebas de integración para main()."""
    
    def test_main_valid_file(self, tmp_fasta_file, capsys):
        """main() debe procesar archivo válido."""
        base_freq.main([tmp_fasta_file])
        
        captured = capsys.readouterr()
        assert "seq1" in captured.out
        assert "7" in captured.out
        assert "Frecuencias:" in captured.out
    
    def test_main_nonexistent_file(self, capsys):
        """main() debe fallar con archivo inexistente."""
        with pytest.raises(SystemExit) as exc_info:
            base_freq.main(["/nonexistent/file.fasta"])
        assert exc_info.value.code == 1
    
    def test_main_with_invalid_chars(self, tmp_fasta_invalid_chars, capsys):
        """main() debe procesar archivo con inválidos."""
        base_freq.main([tmp_fasta_invalid_chars])
        
        captured = capsys.readouterr()
        assert "inválidos" in captured.out
        assert "Frecuencias:" in captured.out


# ============================================================================
# TEST: Edge Cases
# ============================================================================

class TestEdgeCases:
    """Pruebas para casos extremos."""
    
    def test_single_base_type(self, capsys):
        """Debe manejar secuencias de un solo tipo."""
        result = base_freq.get_frequency_result("seq1", "AAAAAAAAAA")
        base_freq.print_frequencies(result)
        
        captured = capsys.readouterr()
        assert "A: 10 (100.0%)" in captured.out
        assert "T: 0 (0.0%)" in captured.out
        assert "G: 0 (0.0%)" in captured.out
        assert "C: 0 (0.0%)" in captured.out
    
    def test_very_long_sequence(self, capsys):
        """Debe manejar secuencias largas."""
        long_seq = "ATGC" * 10000
        result = base_freq.get_frequency_result("seq1", long_seq)
        base_freq.print_frequencies(result)
        
        captured = capsys.readouterr()
        assert "40000" in captured.out
        assert "25.0" in captured.out


# ============================================================================
# Ejecutar pruebas
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
