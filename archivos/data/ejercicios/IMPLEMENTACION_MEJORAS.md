# 📋 Implementación de Mejoras - Contador de k-mers

## ✅ Cambios Realizados

### 1. **Validación Robusta de Secuencias**
- ✅ Verificación de tipo de dato (debe ser `str`)
- ✅ Validación de secuencia no vacía
- ✅ Normalización a mayúsculas (acepta minúsculas)
- ✅ Validación exhaustiva de nucleótidos (solo A, T, C, G)
- ✅ Mensajes de error descriptivos con caracteres inválidos listados

### 2. **Validación Robusta del Parámetro k**
- ✅ Verificación de tipo de dato (debe ser `int`)
- ✅ Validación de valor positivo (k > 0)
- ✅ Validación de que k no exceda la longitud de la secuencia
- ✅ Manejo de excepciones en la conversión de argumentos

### 3. **Manejo Completo de Errores**
- ✅ Try-except para validación de secuencia
- ✅ Try-except para conteo de k-mers
- ✅ Try-except para parsing de argumentos
- ✅ Mensajes de error enviados a stderr
- ✅ Códigos de salida apropiados (1 para error)

### 4. **Documentación PEP8**
- ✅ Módulo documentado con docstring detallado
- ✅ Cada función tiene docstring completo con:
  - Descripción clara
  - Args: parámetros y tipos
  - Returns: valor de retorno y tipo
  - Raises: excepciones que pueden ocurrir
- ✅ Comentarios explicativos en el código
- ✅ Nombres de variables descriptivos
- ✅ Líneas con longitud máxima de 79 caracteres
- ✅ Espaciado y formato según PEP8

### 5. **Mejoras en la Función `count_kmers()`**
- ✅ Algoritmo de ventana deslizante correctamente implementado
- ✅ Diccionario para almacenar conteos (mantiene orden de inserción en Python 3.7+)
- ✅ Uso de `.get()` para inicializar contadores

### 6. **Argumentos de Línea de Comandos Mejorados**
- ✅ Parser con descripción y epilog
- ✅ Argumento posicional: secuencia
- ✅ Argumento opcional: -k / --kmer_size (requerido)
- ✅ Mensajes de ayuda (-h) informativos
- ✅ Validación de argumentos requeridos

### 7. **Salida Formateada**
- ✅ Encabezado comentado en la salida (#)
- ✅ Formato: kmer<TAB>conteo
- ✅ Orden de aparición preservado

## 🧪 Casos de Prueba Validados

### ✅ Casos Exitosos
```bash
python3 k-mers.py ATCGATCG -k 2
# Salida:
# kmer    conteo
AT       2
TC       2
CG       2
GA       1

python3 k-mers.py atcgatcg -k 3
# Salida: (con minúsculas convertidas a mayúsculas)
# kmer    conteo
ATC      2
TCG      2
CGA      1
GAT      1
```

### ❌ Casos de Error Detectados Correctamente

**1. Carácter inválido:**
```bash
python3 k-mers.py ATCGX -k 2
# Error: La secuencia contiene nucleótidos inválidos: X. Solo se permiten: A, T, C, G.
```

**2. k negativo:**
```bash
python3 k-mers.py ATCG -k -5
# Error: El tamaño de k debe ser mayor a 0, se recibió: -5
```

**3. k mayor que secuencia:**
```bash
python3 k-mers.py AT -k 10
# Error: El tamaño de k (10) no puede ser mayor que la longitud de la secuencia (2).
```

**4. Secuencia vacía:**
```bash
python3 k-mers.py "" -k 2
# Error: La secuencia no puede estar vacía.
```

**5. Argumentos requeridos:**
```bash
python3 k-mers.py ATCGATCG
# Error: the following arguments are required: -k/--kmer_size
```

## 📊 Cumplimiento de Requisitos

| Requisito | Estado | Notas |
|-----------|--------|-------|
| Validar secuencia (A,T,C,G) | ✅ | Exhaustivo y robusto |
| Leer k desde opción -k/--kmer_size | ✅ | Argparse configurado |
| Imprimir k-mers y conteos | ✅ | Formato: kmer<TAB>conteo |
| Manejo de errores | ✅ | Completo y descriptivo |
| Documentación PEP8 | ✅ | Siguiendo estándares |
| Normalización (mayúsculas) | ✅ | Soporta minúsculas |
| Mensajes de error descriptivos | ✅ | Stderr, con contexto |

## 🔍 Características Adicionales

- **Algoritmo eficiente:** Ventana deslizante O(n) donde n es la longitud de la secuencia
- **Robustez:** Múltiples niveles de validación
- **Usabilidad:** Mensajes de ayuda claros (`-h`)
- **Escalabilidad:** Puede manejar secuencias grandes
- **Mantenibilidad:** Código limpio y bien documentado

## 🚀 Ejemplo de Uso Completo

```bash
# Uso básico
python3 k-mers.py ATCGATCG -k 2

# Con opción larga
python3 k-mers.py ATCGATCG --kmer_size 3

# Con ayuda
python3 k-mers.py -h

# Con secuencia en minúsculas
python3 k-mers.py atcgatcg -k 2
```

---

**Fecha de implementación:** 26 de noviembre de 2025  
**Estado:** ✅ Completado y validado
