# 🔧 Análisis de Mejoras Potenciales - Contador de k-mers

## 📊 Tabla de Contenidos
1. [Mejoras de Funcionamiento](#mejoras-de-funcionamiento)
2. [Mejoras de Documentación](#mejoras-de-documentación)
3. [Mejoras de Diseño y Arquitectura](#mejoras-de-diseño-y-arquitectura)
4. [Mejoras de Performance](#mejoras-de-performance)
5. [Mejoras de Usabilidad](#mejoras-de-usabilidad)
6. [Problemas Potenciales](#problemas-potenciales)

---

## 🚀 Mejoras de Funcionamiento

### 1. **Usar `defaultdict` en lugar de diccionario manual**

**Situación Actual:**
```python
kmer_counts = {}
for i in range(len(seq) - k + 1):
    kmer = seq[i:i + k]
    kmer_counts[kmer] = kmer_counts.get(kmer, 0) + 1
```

**Mejora:**
```python
from collections import defaultdict

kmer_counts = defaultdict(int)
for i in range(len(seq) - k + 1):
    kmer = seq[i:i + k]
    kmer_counts[kmer] += 1
```

**Ventajas:**
- ✅ Más limpio y legible
- ✅ Menos propenso a errores
- ✅ Ligeramente más eficiente
- ✅ Código idiomático de Python

---

### 2. **Usar `Counter` para conteo de k-mers**

**Alternativa Aún Mejor:**
```python
from collections import Counter

def count_kmers(seq, k):
    """Contar k-mers usando Counter."""
    kmers = [seq[i:i + k] for i in range(len(seq) - k + 1)]
    return Counter(kmers)
```

**Ventajas:**
- ✅ Una línea en lugar de 5
- ✅ Más pythónico
- ✅ Mejor legibilidad
- ✅ Métodos útiles incluidos (`.most_common()`, etc.)
- ✅ Mejor performance en secuencias grandes

---

### 3. **Extraer constantes mágicas**

**Situación Actual:**
```python
valid_nucleotides = set("ATCG")  # Definido dentro de la función
```

**Mejora:**
```python
# Al inicio del módulo
VALID_NUCLEOTIDES = {"A", "T", "C", "G"}
NUCLEOTIDES_STR = "ATCG"  # Para mensajes de usuario
```

**Ventajas:**
- ✅ Fácil de cambiar (si quieres soportar N, W, etc.)
- ✅ Reutilizable
- ✅ Mejor documentación
- ✅ Sigue PEP8

---

### 4. **Crear una clase para gestionar validaciones**

**Situación Actual:**
- Funciones separadas de validación

**Mejora:**
```python
class SequenceValidator:
    """Validador de secuencias de ADN."""
    
    VALID_NUCLEOTIDES = {"A", "T", "C", "G"}
    
    @staticmethod
    def validate(seq):
        """Validar y normalizar secuencia."""
        if not isinstance(seq, str):
            raise TypeError(...)
        if not seq:
            raise ValueError(...)
        seq_upper = seq.upper()
        invalid = set(seq_upper) - SequenceValidator.VALID_NUCLEOTIDES
        if invalid:
            raise ValueError(...)
        return seq_upper
```

**Ventajas:**
- ✅ Mejor encapsulación
- ✅ Fácil de extender
- ✅ Puede soportar más formatos (DNA, RNA, proteínas)

---

### 5. **Soportar lectura desde archivo FASTA**

**Mejora:**
```python
def read_fasta(filepath):
    """Leer secuencia desde archivo FASTA."""
    seq = ""
    with open(filepath, 'r') as f:
        for line in f:
            if not line.startswith('>'):
                seq += line.strip()
    return seq

# En main():
if args.file:
    seq = read_fasta(args.file)
elif args.sequence:
    seq = args.sequence
else:
    raise ValueError("Debe especificar -s o -f")
```

**Ventajas:**
- ✅ Manejo de archivos FASTA comunes en bioinformática
- ✅ Mejor para secuencias grandes
- ✅ Más versátil

---

### 6. **Agregar opción de ordenamiento de salida**

**Mejora:**
```python
parser.add_argument(
    "--sort",
    choices=["appearance", "frequency", "kmer"],
    default="appearance",
    help="Ordenar resultados por: aparición, frecuencia o nombre del kmer"
)

# En main():
if args.sort == "frequency":
    sorted_kmers = sorted(kmer_counts.items(), key=lambda x: -x[1])
elif args.sort == "kmer":
    sorted_kmers = sorted(kmer_counts.items())
else:
    sorted_kmers = kmer_counts.items()

for kmer, count in sorted_kmers:
    print(f"{kmer}\t{count}")
```

**Ventajas:**
- ✅ Mayor flexibilidad
- ✅ Mejor análisis de datos
- ✅ Fácil identificar k-mers más frecuentes

---

### 7. **Detectar booleanos (`bool` es subclase de `int` en Python)**

**Problema:**
```python
count_kmers("ATCG", True)  # True == 1, ¡se acepta!
```

**Mejora:**
```python
if isinstance(k, bool) or not isinstance(k, int):
    raise TypeError(...)
```

---

## 📚 Mejoras de Documentación

### 1. **Agregar ejemplos en docstrings (estilo NumPy/Google)**

**Mejora:**
```python
def count_kmers(seq, k):
    """Contar la frecuencia de cada k-mer en una secuencia.
    
    Extrae todos los k-mers contiguos de longitud k de la secuencia
    y cuenta cuántas veces aparece cada uno.
    
    Parameters
    ----------
    seq : str
        Secuencia de ADN validada (solo A, T, C, G).
    k : int
        Longitud del k-mer (1 <= k <= len(seq)).
    
    Returns
    -------
    dict
        Diccionario con k-mers como claves y sus conteos como valores.
    
    Raises
    ------
    TypeError
        Si k no es un entero o seq no es una cadena.
    ValueError
        Si k <= 0 o k > len(seq).
    
    Examples
    --------
    >>> seq = "ATCGATCG"
    >>> count_kmers(seq, 2)
    {'AT': 2, 'TC': 2, 'CG': 2, 'GA': 1}
    
    >>> count_kmers(seq, 3)
    {'ATC': 2, 'TCG': 2, 'CGA': 1, 'GAT': 1}
    
    Notes
    -----
    La secuencia debe estar validada antes de pasar a esta función.
    El algoritmo utiliza una ventana deslizante con complejidad O(n).
    """
```

**Ventajas:**
- ✅ Ejemplos de uso en la documentación
- ✅ Tipo de parámetros más claro
- ✅ Notas sobre complejidad
- ✅ Compatible con herramientas de documentación automática

---

### 2. **Documentar la complejidad algorítmica**

**Mejora:**
```python
def count_kmers(seq, k):
    """
    ...
    
    Time Complexity
    ---------------
    O(n * k) donde n es la longitud de la secuencia.
    Nota: slicing en Python es O(k).
    
    Space Complexity
    ----------------
    O(unique_kmers * k) para almacenar el diccionario.
    """
```

---

### 3. **Agregar references a literatura científica**

**Mejora:**
```python
"""
k-mers for Sequence Analysis
=============================

Los k-mers son herramientas fundamentales en bioinformática para:
- Ensamblaje de genomas (De Bruijn graphs)
- Detección de similitud entre secuencias
- Análisis de codon usage

Referencias:
- Pevzner, P. A. (2000). Computational Molecular Biology: An Algorithmic Approach.
- Miller, J. R., et al. (2010). Assembly algorithms for next-generation sequencing.
"""
```

---

### 4. **Documentar los formatos de entrada/salida**

**Mejora:**
```python
def main():
    """
    ...
    
    Input Format
    -----------
    - Sequence: Cadena de nucleótidos (A, T, C, G)
    - k: Entero positivo
    
    Output Format
    -----------
    Líneas tabuladas con formato:
    kmer[TAB]frequency
    
    Ejemplo:
    # kmer    frequency
    AT       2
    TC       2
    CG       2
    GA       1
    """
```

---

## 🏗️ Mejoras de Diseño y Arquitectura

### 1. **Separar lógica de negocio de I/O**

**Situación Actual:**
- `main()` hace validación, conteo e impresión todo junto

**Mejora:**
```python
def process_kmer_analysis(seq, k):
    """Realiza el análisis de k-mers (sin I/O)."""
    seq_validated = validate_sequence(seq)
    kmer_counts = count_kmers(seq_validated, k)
    return kmer_counts

def format_output(kmer_counts):
    """Formatea los resultados para imprimir."""
    lines = ["# kmer\tconteo"]
    for kmer, count in kmer_counts.items():
        lines.append(f"{kmer}\t{count}")
    return "\n".join(lines)

def main():
    """Orquesta I/O y procesamiento."""
    args = parse_arguments()
    try:
        results = process_kmer_analysis(args.sequence, args.kmer_size)
        output = format_output(results)
        print(output)
    except (ValueError, TypeError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
```

**Ventajas:**
- ✅ Fácil de testear
- ✅ Reutilizable en otros contextos
- ✅ Responsabilidad única (SRP)

---

### 2. **Crear un archivo de configuración o usar enums**

**Mejora:**
```python
from enum import Enum

class SortOrder(Enum):
    APPEARANCE = "appearance"
    FREQUENCY = "frequency"
    NAME = "name"

class OutputFormat(Enum):
    TSV = "tsv"
    JSON = "json"
    CSV = "csv"
```

---

### 3. **Estructura de proyecto mejorada**

```
k-mers/
├── src/
│   ├── __init__.py
│   ├── kmer_counter.py      # Lógica principal
│   ├── validators.py        # Validaciones
│   ├── formatters.py        # Formateo de salida
│   ├── cli.py               # Interfaz de línea de comandos
│   └── exceptions.py        # Excepciones personalizadas
├── tests/
│   ├── test_validators.py
│   ├── test_kmer_counter.py
│   └── test_cli.py
├── docs/
│   ├── api.md
│   ├── examples.md
│   └── algorithms.md
├── README.md
├── setup.py
└── requirements.txt
```

---

## ⚡ Mejoras de Performance

### 1. **Usar generadores para secuencias largas**

**Mejora:**
```python
def kmers_generator(seq, k):
    """Generar k-mers sin almacenar todos en memoria."""
    for i in range(len(seq) - k + 1):
        yield seq[i:i + k]

def count_kmers_streaming(seq, k):
    """Contar k-mers usando generador."""
    return Counter(kmers_generator(seq, k))
```

**Ventajas:**
- ✅ Menor uso de memoria
- ✅ Mejor para secuencias de millones de bp

---

### 2. **Usar slicing nativo vs manualmente**

**Comparación:**
```python
# Actual: O(n*k) porque cada slice copia k caracteres
kmers = [seq[i:i+k] for i in range(len(seq) - k + 1)]

# Alternativa: Podría usar rolling hash (más complejo)
# Pero para casos normales, la solución actual es óptima
```

---

### 3. **Cachear resultados si es necesario**

**Mejora (si se llama repetidamente):**
```python
from functools import lru_cache

@lru_cache(maxsize=128)
def count_kmers_cached(seq, k):
    """Versión cacheada para llamadas repetidas."""
    return count_kmers(seq, k)
```

---

## 👥 Mejoras de Usabilidad

### 1. **Agregar modo verbose y debug**

**Mejora:**
```python
parser.add_argument(
    "-v", "--verbose",
    action="store_true",
    help="Mostrar información detallada de procesamiento"
)

parser.add_argument(
    "--debug",
    action="store_true",
    help="Mostrar trazas de depuración"
)

# En main():
if args.verbose:
    print(f"Secuencia: {seq_validated}", file=sys.stderr)
    print(f"Longitud: {len(seq_validated)}", file=sys.stderr)
    print(f"k: {args.kmer_size}", file=sys.stderr)
```

---

### 2. **Agregar estadísticas de salida**

**Mejora:**
```python
def print_statistics(kmer_counts, seq_len, k):
    """Imprimir estadísticas del análisis."""
    print(f"# Total k-mers: {sum(kmer_counts.values())}", file=sys.stderr)
    print(f"# k-mers únicos: {len(kmer_counts)}", file=sys.stderr)
    max_kmer = max(kmer_counts, key=kmer_counts.get)
    print(f"# k-mer más frecuente: {max_kmer} ({kmer_counts[max_kmer]}x)", 
          file=sys.stderr)
```

---

### 3. **Progreso bar para secuencias largas**

**Mejora:**
```python
from tqdm import tqdm

def count_kmers_with_progress(seq, k):
    """Contar k-mers con barra de progreso."""
    kmer_counts = {}
    for i in tqdm(range(len(seq) - k + 1), desc="Contando k-mers"):
        kmer = seq[i:i + k]
        kmer_counts[kmer] = kmer_counts.get(kmer, 0) + 1
    return kmer_counts
```

---

### 4. **Validación de argumentos más clara**

**Mejora:**
```python
parser.add_argument(
    "-k", "--kmer_size",
    type=int,
    required=True,
    metavar="INT",
    help="Tamaño del k-mer (ej: 2 para dimeros, 3 para trimeros). "
         "Debe ser positivo y menor o igual a la longitud de la secuencia."
)
```

---

## ⚠️ Problemas Potenciales

### 1. **Validación de tipos no detecta `bool`**

**Problema:**
```python
count_kmers("ATCG", True)  # Aceptado porque bool es subclase de int
```

**Solución:**
```python
if isinstance(k, bool) or not isinstance(k, int):
    raise TypeError(...)
```

---

### 2. **Sin limite de tamaño de secuencia**

**Problema:**
```python
# Si alguien ingresa 1GB de datos, puede fallar
```

**Solución:**
```python
MAX_SEQUENCE_LENGTH = 1_000_000_000  # 1 billón bp

if len(seq) > MAX_SEQUENCE_LENGTH:
    raise ValueError(f"Secuencia muy grande (máx: {MAX_SEQUENCE_LENGTH})")
```

---

### 3. **Sin soporte para RNA o proteínas**

**Problema:**
- Solo soporta DNA (A, T, C, G)

**Solución:**
```python
class SequenceType(Enum):
    DNA = {"A", "T", "C", "G"}
    RNA = {"A", "U", "C", "G"}
    PROTEIN = set("ACDEFGHIKLMNPQRSTVWY")

def validate_sequence(seq, seq_type=SequenceType.DNA):
    """Validar según tipo de secuencia."""
    valid_chars = seq_type.value
    # ...
```

---

### 4. **Manejo incompleto de archivos**

**Problema:**
```python
# Si el archivo no existe o tiene permisos insuficientes, crash
```

**Solución:**
```python
try:
    with open(filepath, 'r') as f:
        seq = f.read().strip()
except FileNotFoundError:
    raise ValueError(f"Archivo no encontrado: {filepath}")
except PermissionError:
    raise ValueError(f"Permisos insuficientes: {filepath}")
except IOError as e:
    raise ValueError(f"Error al leer archivo: {e}")
```

---

### 5. **Sin validación de argumentos posicionales**

**Problema:**
```bash
python3 k-mers.py  # Falta la secuencia
# Output: usage: k-mers.py [-h] -k KMER_SIZE sequence
```

**Debería ser más específico:**
```python
if not args.sequence or (isinstance(args.sequence, str) and 
                          len(args.sequence.strip()) == 0):
    parser.error("La secuencia no puede estar vacía")
```

---

## 📈 Matriz de Prioridades

| Mejora | Impacto | Esfuerzo | Prioridad |
|--------|---------|----------|-----------|
| Usar `Counter` | Alto | Bajo | 🔴 Alta |
| Soportar lectura FASTA | Alto | Medio | 🟡 Media |
| Agregar ejemplos en docstrings | Medio | Bajo | 🔴 Alta |
| Separar lógica de I/O | Medio | Medio | 🟡 Media |
| Detectar `bool` en validación | Bajo | Bajo | 🟢 Baja |
| Soportar RNA/Proteínas | Medio | Alto | 🟢 Baja |
| Agregar barra de progreso | Bajo | Bajo | 🟢 Baja |
| Crear estructura de proyecto | Alto | Alto | 🟡 Media |

---

## ✅ Recomendaciones Finales

### **Nivel 1: Mejoras Críticas (Implementar Ahora)**
1. ✅ Usar `Counter` para conteo
2. ✅ Agregar ejemplos en docstrings
3. ✅ Detectar `bool` en validación
4. ✅ Documentar complejidad algorítmica

### **Nivel 2: Mejoras Importantes (Próximo Sprint)**
1. ✅ Soportar lectura FASTA
2. ✅ Separar lógica de I/O
3. ✅ Agregar opciones de ordenamiento
4. ✅ Mejores mensajes de error

### **Nivel 3: Mejoras Opcionales (Futuro)**
1. ✅ Soportar RNA/Proteínas
2. ✅ Integración con tests
3. ✅ Barra de progreso
4. ✅ Estructura de proyecto modular

---

**Análisis completado:** 26 de noviembre de 2025
