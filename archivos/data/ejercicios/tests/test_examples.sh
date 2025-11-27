#!/bin/bash
# Test Examples - Ejemplos de ejecución de pruebas

# Cambiar al directorio del proyecto
cd /Users/monicareyesramirez/Documents/Documents/Bioinfo1/Data/Proyectos/archivos/data/ejercicios

# Activar virtual environment
source .venv/bin/activate

# ============================================================================
# EJEMPLO 1: Ejecutar TODAS las pruebas (modo verbose)
# ============================================================================
echo "=== EJECUTAR TODAS LAS PRUEBAS ==="
pytest tests/test_gene_expression.py -v

# ============================================================================
# EJEMPLO 2: Ejecutar pruebas de una CLASE específica
# ============================================================================
echo -e "\n=== PRUEBAS DE CARGA DE ARCHIVOS ==="
pytest tests/test_gene_expression.py::TestLoadExpressionTable -v

echo -e "\n=== PRUEBAS DE FILTRADO ==="
pytest tests/test_gene_expression.py::TestFilterGenes -v

echo -e "\n=== PRUEBAS DE VALIDACIÓN ==="
pytest tests/test_gene_expression.py::TestValidateThreshold -v

echo -e "\n=== PRUEBAS DEL PARSER ==="
pytest tests/test_gene_expression.py::TestBuildParser -v

echo -e "\n=== PRUEBAS DE INTEGRACIÓN ==="
pytest tests/test_gene_expression.py::TestIntegration -v

echo -e "\n=== CASOS LÍMITE ==="
pytest tests/test_gene_expression.py::TestEdgeCases -v

# ============================================================================
# EJEMPLO 3: Ejecutar UNA PRUEBA específica
# ============================================================================
echo -e "\n=== UNA PRUEBA ESPECÍFICA ==="
pytest tests/test_gene_expression.py::TestFilterGenes::test_filter_threshold_10 -vv

# ============================================================================
# EJEMPLO 4: Mostrar SOLO FALLOS (si hay)
# ============================================================================
echo -e "\n=== SOLO FALLOS ==="
pytest tests/test_gene_expression.py -v --tb=short --lf

# ============================================================================
# EJEMPLO 5: COBERTURA de código
# ============================================================================
echo -e "\n=== COBERTURA DE CÓDIGO ==="
pytest tests/test_gene_expression.py --cov=gene_expression --cov-report=term-missing

# ============================================================================
# EJEMPLO 6: Pruebas POR PALABRA CLAVE
# ============================================================================
echo -e "\n=== PRUEBAS CON PALABRA CLAVE: 'threshold' ==="
pytest tests/test_gene_expression.py -k "threshold" -v

echo -e "\n=== PRUEBAS CON PALABRA CLAVE: 'valid' ==="
pytest tests/test_gene_expression.py -k "valid" -v

# ============================================================================
# EJEMPLO 7: SALIDA CORTA (sin verbosity)
# ============================================================================
echo -e "\n=== SALIDA CORTA ==="
pytest tests/test_gene_expression.py

# ============================================================================
# EJEMPLO 8: Mostrar PRINTS durante ejecución (con -s)
# ============================================================================
echo -e "\n=== CON SALIDA DE PRINT ==="
pytest tests/test_gene_expression.py::TestLoadExpressionTable::test_invalid_values_cleaned -v -s

# ============================================================================
# EJEMPLO 9: TRACEBACK completo (si hay errores)
# ============================================================================
echo -e "\n=== TRACEBACK COMPLETO ==="
pytest tests/test_gene_expression.py -v --tb=long

# ============================================================================
# EJEMPLO 10: MÚLTIPLES FILTROS
# ============================================================================
echo -e "\n=== FILTROS MÚLTIPLES: 'TestLoadExpressionTable OR TestFilterGenes' ==="
pytest tests/test_gene_expression.py -k "TestLoadExpressionTable or TestFilterGenes" -v

# ============================================================================
# EJEMPLO 11: TIEMPO DE EJECUCIÓN
# ============================================================================
echo -e "\n=== PRUEBAS MÁS LENTAS ==="
pytest tests/test_gene_expression.py --durations=5

# ============================================================================
# EJEMPLO 12: GENERAR REPORTE HTML
# ============================================================================
echo -e "\n=== GENERAR REPORTE HTML DE COBERTURA ==="
pytest tests/test_gene_expression.py --cov=gene_expression --cov-report=html
echo "Abrir: htmlcov/index.html"

# ============================================================================
# EJEMPLO 13: FORMATO SIMPLE
# ============================================================================
echo -e "\n=== FORMATO SIMPLE ==="
pytest tests/test_gene_expression.py -q

# ============================================================================
# EJEMPLO 14: DETENER EN PRIMER FALLO
# ============================================================================
echo -e "\n=== DETENER EN PRIMER FALLO ==="
pytest tests/test_gene_expression.py -x

# ============================================================================
# EJEMPLO 15: FORMATO JSON (para procesamiento automático)
# ============================================================================
echo -e "\n=== REPORTE JSON ==="
pytest tests/test_gene_expression.py --json-report --json-report-file=report.json
