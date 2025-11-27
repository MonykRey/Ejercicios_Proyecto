# Testing Documentation - gene-expression.py

## 📋 Descripción

Suite completa de pruebas unitarias para el programa de filtrado de genes por expresión, utilizando **pytest** como framework de testing.

## 🎯 Cobertura de Pruebas

| Categoría | Cantidad | Descripción |
|-----------|----------|-------------|
| **Total de pruebas** | 35 | Pruebas unitarias e integración |
| **TestLoadExpressionTable** | 7 | Carga y validación de archivos |
| **TestFilterGenes** | 6 | Filtrado de genes por threshold |
| **TestValidateThreshold** | 6 | Validación de parámetros |
| **TestBuildParser** | 7 | Parsing de argumentos de línea de comandos |
| **TestIntegration** | 4 | Pruebas end-to-end |
| **TestEdgeCases** | 5 | Casos límite y especiales |

## 📊 Cobertura de Código

```
Cobertura actual: 57%
Líneas sin cobertura: 95, 219-226, 245-274, 278
(Principalmente: manejo de errores en main(), print statements)
```

## 🚀 Cómo ejecutar las pruebas

### 1. **Todas las pruebas (modo verbose)**

```bash
pytest tests/test_gene_expression.py -v
```

**Salida esperada:**
```
tests/test_gene_expression.py::TestLoadExpressionTable::test_load_valid_file PASSED
tests/test_gene_expression.py::TestFilterGenes::test_filter_threshold_10 PASSED
...
======================== 35 passed in 0.17s ========================
```

### 2. **Pruebas con salida corta**

```bash
pytest tests/test_gene_expression.py
```

### 3. **Pruebas de una clase específica**

```bash
# Solo pruebas de carga de archivos
pytest tests/test_gene_expression.py::TestLoadExpressionTable -v

# Solo pruebas de filtrado
pytest tests/test_gene_expression.py::TestFilterGenes -v

# Solo pruebas de validación
pytest tests/test_gene_expression.py::TestValidateThreshold -v

# Solo pruebas del parser
pytest tests/test_gene_expression.py::TestBuildParser -v

# Solo pruebas de integración
pytest tests/test_gene_expression.py::TestIntegration -v

# Solo casos límite
pytest tests/test_gene_expression.py::TestEdgeCases -v
```

### 4. **Prueba específica**

```bash
pytest tests/test_gene_expression.py::TestFilterGenes::test_filter_threshold_10 -v
```

### 5. **Con reporte de cobertura**

```bash
pytest tests/test_gene_expression.py --cov=gene_expression --cov-report=term-missing
```

### 6. **Generar reporte HTML de cobertura**

```bash
pytest tests/test_gene_expression.py --cov=gene_expression --cov-report=html
open htmlcov/index.html
```

### 7. **Mostrar solo fallos**

```bash
pytest tests/test_gene_expression.py -v --tb=short -k "invalid"
```

### 8. **Ejecutar con nivel de verbosidad extra**

```bash
pytest tests/test_gene_expression.py -vv --tb=long
```

## 📝 Descripción de pruebas por categoría

### TestLoadExpressionTable (7 pruebas)

Valida que la función `load_expression_table()` funciona correctamente:

| Prueba | Propósito |
|--------|----------|
| `test_load_valid_file` | Cargar archivo TSV válido |
| `test_load_valid_file_has_correct_types` | Verificar tipos de datos |
| `test_load_valid_file_sorted` | Verificar genes presentes |
| `test_file_not_found` | Manejo de archivo no encontrado |
| `test_empty_file` | Rechazo de archivo vacío |
| `test_wrong_columns` | Validación de columnas |
| `test_invalid_values_cleaned` | Limpieza de valores inválidos |

### TestFilterGenes (6 pruebas)

Valida que la función `filter_genes()` filtra correctamente:

| Prueba | Propósito |
|--------|----------|
| `test_filter_threshold_zero` | Threshold 0 retorna todos |
| `test_filter_threshold_10` | Filtrado correcto en threshold 10 |
| `test_filter_threshold_high` | Threshold muy alto |
| `test_filter_returns_sorted` | Resultados ordenados alfabéticamente |
| `test_filter_no_results` | Threshold sin resultados |
| `test_filter_preserves_expression` | Preservación de valores |

### TestValidateThreshold (6 pruebas)

Valida que `validate_threshold()` funciona:

| Prueba | Propósito |
|--------|----------|
| `test_validate_positive_threshold` | Acepta positivos |
| `test_validate_zero_threshold` | Acepta cero |
| `test_validate_large_threshold` | Acepta valores grandes |
| `test_validate_negative_threshold_raises_error` | Rechaza negativos |
| `test_validate_small_negative_threshold_raises_error` | Rechaza pequeños negativos |
| `test_validate_float_threshold` | Acepta decimales |

### TestBuildParser (7 pruebas)

Valida que `build_parser()` funciona:

| Prueba | Propósito |
|--------|----------|
| `test_parser_created` | Parser se crea |
| `test_parser_has_file_argument` | Argumento 'file' presente |
| `test_parser_has_threshold_argument` | Argumento 'threshold' presente |
| `test_parser_threshold_default` | Valor por defecto 0.0 |
| `test_parser_threshold_long_form` | Forma larga funciona |
| `test_parser_threshold_type_conversion` | Conversión a float |
| `test_parser_invalid_threshold` | Rechazo de entrada inválida |

### TestIntegration (4 pruebas)

Pruebas end-to-end del flujo completo:

| Prueba | Propósito |
|--------|----------|
| `test_full_workflow` | Flujo completo normal |
| `test_workflow_with_zero_threshold` | Workflow con threshold 0 |
| `test_workflow_with_no_results` | Workflow sin resultados |
| `test_parser_workflow` | Parsing e integración |

### TestEdgeCases (5 pruebas)

Casos límite y especiales:

| Prueba | Propósito |
|--------|----------|
| `test_single_gene` | Un solo gen en archivo |
| `test_duplicate_genes` | Genes duplicados |
| `test_genes_with_special_characters` | Caracteres especiales |
| `test_very_small_expression_values` | Valores muy pequeños |
| `test_very_large_expression_values` | Valores muy grandes |

## 📂 Estructura de directorios

```
ejercicios/
├── src/
│   ├── gene-expression.py          # Archivo original (ejecutable)
│   └── gene_expression.py          # Copia para importar en pruebas
├── tests/
│   ├── conftest.py                 # Configuración de pytest
│   ├── test_gene_expression.py     # Suite de pruebas
│   ├── test_data/
│   │   ├── valid.tsv              # Datos válidos
│   │   ├── empty.tsv              # Archivo vacío
│   │   ├── invalid_values.tsv     # Valores inválidos
│   │   └── wrong_columns.tsv      # Columnas incorrectas
│   └── README.md                   # Este archivo
└── data/
    ├── condA.tsv
    └── condB.tsv
```

## 🐛 Diagnóstico de fallos

Si una prueba falla, usa:

```bash
# Mostrar traceback completo
pytest tests/test_gene_expression.py -v --tb=long

# Mostrar prints durante ejecución
pytest tests/test_gene_expression.py -v -s

# Solo una prueba específica con verbose
pytest tests/test_gene_expression.py::TestLoadExpressionTable::test_load_valid_file -vv
```

## 🛠️ Requisitos

```bash
# Instalar dependencias
pip install pytest pytest-cov pandas

# O usar el venv del proyecto
source .venv/bin/activate
pip install pytest pytest-cov pandas
```

## ✅ Resultados esperados

Todas las 35 pruebas deben pasar:

```
============================== 35 passed in 0.17s ==============================
```

Si alguna falla, esto indica un problema en el código que debe ser corregido.

## 📚 Mejores prácticas de testing

Este proyecto implementa:

✅ **Separación de responsabilidades** - Cada función prueba un aspecto específico  
✅ **Nomenclatura clara** - Nombres descriptivos de pruebas  
✅ **Fixtures** - Datos reutilizables en pruebas  
✅ **Excepciones** - Validación de manejo de errores  
✅ **Casos límite** - Pruebas de valores extremos  
✅ **Integración** - Pruebas end-to-end  
✅ **Documentación** - Docstrings en cada prueba  

## 📖 Referencias

- [Documentación de pytest](https://docs.pytest.org/)
- [pytest fixtures](https://docs.pytest.org/en/stable/fixture.html)
- [Coverage.py](https://coverage.readthedocs.io/)
