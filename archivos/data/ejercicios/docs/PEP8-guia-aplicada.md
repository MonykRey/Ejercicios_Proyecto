# Guía de Estilo PEP 8 - Aplicada al Código

Este documento explica cómo el código de `rps.py` cumple con los estándares PEP 8 y PEP 257.

## 1. PEP 8 - Guía de Estilo para Código Python

### 1.1 Indentación

**Regla**: Usar 4 espacios por nivel de indentación.

✅ **Correcto**:
```python
def main() -> None:
    print("Bienvenida")
    while True:
        user_input = input("Tu elección: ")
        if not user_input:
            break
```

❌ **Incorrecto**:
```python
def main() -> None:
  print("Bienvenida")  # 2 espacios
   while True:
        user_input = input("Tu elección: ")  # Inconsistente
```

---

### 1.2 Longitud Máxima de Línea

**Regla**: Máximo 79 caracteres (recomendado 72 para docstrings/comentarios).

✅ **Correcto**:
```python
# Línea con 79 caracteres o menos
if user_input not in VALID_CHOICES:
    print(f"❌ Elección no válida. Elige entre: {', '.join(VALID_CHOICES)}")
```

Cuando una línea es necesariamente larga:
```python
# Romper línea larga
elif (user == "rock" and cpu == "scissors") or \
     (user == "paper" and cpu == "rock") or \
     (user == "scissors" and cpu == "paper"):
    return "win"
```

---

### 1.3 Líneas en Blanco

**Regla**: 
- 2 líneas en blanco entre funciones de nivel superior
- 1 línea en blanco entre métodos dentro de una clase

✅ **Correcto**:
```python
VALID_CHOICES = ["rock", "paper", "scissors"]


def determine_result(user: str, cpu: str) -> str:
    """..."""
    if user == cpu:
        return "draw"


def play(user_choice: str) -> tuple[str, str]:
    """..."""
    cpu_choice = random.choice(VALID_CHOICES)
```

---

### 1.4 Nombres de Variables y Funciones

**Regla**: Usar `snake_case` (minúsculas con guiones bajos)

✅ **Correcto**:
```python
def determine_result(user: str, cpu: str) -> str:  # Función
    user_input = input()  # Variable
    cpu_choice = random.choice(VALID_CHOICES)  # Variable
```

❌ **Incorrecto**:
```python
def DetermineResult(user: str, cpu: str) -> str:  # CamelCase (No PEP8)
    userInput = input()  # camelCase (No PEP8)
    CPUChoice = random.choice(VALID_CHOICES)  # MixedCase (No PEP8)
```

---

### 1.5 Nombres de Constantes

**Regla**: Usar `UPPER_CASE` (mayúsculas con guiones bajos)

✅ **Correcto**:
```python
VALID_CHOICES = ["rock", "paper", "scissors"]
MAX_ATTEMPTS = 3
DEFAULT_TIMEOUT = 30
```

❌ **Incorrecto**:
```python
valid_choices = ["rock", "paper", "scissors"]  # Debería ser CONST
ValidChoices = ["rock", "paper", "scissors"]  # No es constante
```

---

### 1.6 Espacios alrededor de Operadores

**Regla**: Espacios alrededor de operadores de asignación y comparación

✅ **Correcto**:
```python
wins = 0
losses = 0
draws = 0

if user == cpu:
    return "draw"

total_games = wins + losses + draws
win_rate = (wins / total_games) * 100
```

❌ **Incorrecto**:
```python
wins=0  # Sin espacios
losses= 0  # Inconsistente
draws =0  # Inconsistente

if user==cpu:  # Sin espacios
    return "draw"

total_games=wins+losses+draws  # Sin espacios
```

---

### 1.7 Espacios en Listas y Tuplas

**Regla**: Espacio después de comas, NO espacios dentro de los paréntesis

✅ **Correcto**:
```python
VALID_CHOICES = ["rock", "paper", "scissors"]
cpu_choice, result = play(user_input)
print(f"Resultado: {result}")
```

❌ **Incorrecto**:
```python
VALID_CHOICES = ["rock","paper","scissors"]  # Sin espacios después de comas
VALID_CHOICES = [ "rock" , "paper" , "scissors" ]  # Espacios extra
```

---

### 1.8 Imports

**Regla**: 
- Imports en la parte superior del archivo
- Uno por línea (excepto `from x import y, z`)
- Ordenar: estándar, terceros, locales

✅ **Correcto**:
```python
#!/usr/bin/env python3
"""Docstring del módulo."""

import random
import os
from typing import Optional

import numpy  # Si existiera, iría aquí

from mi_modulo import mi_funcion
```

---

### 1.9 Comparaciones y Condiciones

**Regla**: Comparar directamente con `None`, `True`, `False`

✅ **Correcto**:
```python
if user_input:  # Para verificar que no está vacío
    pass

if not user_input:  # Para verificar que está vacío
    break

if result is None:  # Comparar con None
    pass
```

❌ **Incorrecto**:
```python
if user_input != "":  # Comparar con string vacío
    pass

if user_input == True:  # Comparar bool innecesariamente
    pass

if result == None:  # Usar "is" en lugar de "=="
    pass
```

---

## 2. PEP 257 - Convenciones de Docstrings

### 2.1 Estructura General del Docstring

**Regla**: 
- Primera línea: Descripción breve (una línea, punto al final)
- Línea en blanco (si hay más contenido)
- Descripción detallada (opcional)
- Línea en blanco
- Secciones: Args, Returns, Raises, Example, Note, etc.

✅ **Correcto**:
```python
def determine_result(user: str, cpu: str) -> str:
    """Determinar el resultado del juego comparando ambas elecciones.

    Compara la elección del usuario con la de la CPU según las reglas:
    - Rock gana a Scissors
    - Paper gana a Rock
    - Scissors gana a Paper
    - Si ambos eligen lo mismo, es un empate

    Args:
        user (str): La elección del usuario.
                   Debe ser 'rock', 'paper' o 'scissors'.
        cpu (str):  La elección de la CPU.
                   Debe ser 'rock', 'paper' o 'scissors'.

    Returns:
        str: Resultado de la ronda:
            - 'win': si el usuario gana
            - 'lose': si el usuario pierde
            - 'draw': si ambos eligieron lo mismo

    Example:
        >>> determine_result('rock', 'scissors')
        'win'
    """
```

---

### 2.2 Docstring del Módulo

**Regla**: 
- Ubicado al inicio del archivo
- Describe el propósito del módulo
- Puede incluir autor, versión, requisitos

✅ **Correcto**:
```python
#!/usr/bin/env python3
"""Rock, Paper, Scissors Game - Juego interactivo entre usuario y computadora.

Este módulo implementa el juego clásico de Piedra, Papel o Tijera con las
siguientes características:

    - Interfaz interactiva con emojis
    - Elección aleatoria de la computadora
    - Validación de entradas del usuario

Uso:
    python3 rps.py

Author:
    Proyecto Educativo - Bioinformática

Version:
    1.0

Requisitos:
    Python 3.9+
"""
```

---

### 2.3 Secciones de Docstrings

| Sección | Descripción | Ejemplo |
|---------|-------------|---------|
| **Args** | Parámetros de la función | `Args: user (str): La elección del usuario` |
| **Returns** | Lo que retorna | `Returns: str: 'win', 'lose' o 'draw'` |
| **Raises** | Excepciones posibles | `Raises: ValueError: Si entrada inválida` |
| **Example** | Ejemplo de uso | `Example: >>> determine_result('rock', 'scissors')` |
| **Note** | Notas adicionales | `Note: Esta función es case-sensitive` |
| **Warning** | Advertencias | `Warning: Modifica la variable global` |

---

### 2.4 Type Hints (PEP 484)

**Regla**: Usar type hints para parámetros y retorno

✅ **Python 3.9+**:
```python
def determine_result(user: str, cpu: str) -> str:
    """..."""
    pass

def play(user_choice: str) -> tuple[str, str]:
    """..."""
    pass

def main() -> None:
    """..."""
    pass
```

---

## 3. Checklist de Cumplimiento PEP 8/257

- ✅ Indentación de 4 espacios
- ✅ Máximo 79 caracteres por línea
- ✅ 2 líneas en blanco entre funciones
- ✅ Nombres en `snake_case` (funciones, variables)
- ✅ Constantes en `UPPER_CASE`
- ✅ Espacios alrededor de operadores
- ✅ Docstrings con formato adecuado
- ✅ Type hints en funciones
- ✅ Imports organizados correctamente
- ✅ Comentarios descriptivos cuando sea necesario

---

## 4. Herramientas para Verificar PEP 8

### 4.1 `pylint`
```bash
pip install pylint
pylint src/rps.py
```

### 4.2 `flake8`
```bash
pip install flake8
flake8 src/rps.py
```

### 4.3 `black` (Formateador automático)
```bash
pip install black
black src/rps.py
```

### 4.4 `autopep8` (Auto-corrector)
```bash
pip install autopep8
autopep8 --in-place src/rps.py
```

---

## 5. Ejemplo: Antes y Después

### Antes (Sin PEP 8)
```python
import random
CHOICES=['rock','paper','scissors']
def determine_result( user,cpu ):
    if user==cpu:
        return 'draw'
    elif (user=='rock' and cpu=='scissors'):
        return 'win'
    else:
        return 'lose'
def play(user_choice):
    cpu_choice=random.choice(CHOICES)
    result=determine_result(user_choice,cpu_choice)
    return cpu_choice,result
```

### Después (Con PEP 8)
```python
#!/usr/bin/env python3
"""Rock, Paper, Scissors Game."""

import random

VALID_CHOICES = ["rock", "paper", "scissors"]


def determine_result(user: str, cpu: str) -> str:
    """Determinar el resultado del juego."""
    if user == cpu:
        return "draw"
    elif user == "rock" and cpu == "scissors":
        return "win"
    else:
        return "lose"


def play(user_choice: str) -> tuple[str, str]:
    """Ejecutar una ronda del juego."""
    cpu_choice = random.choice(VALID_CHOICES)
    result = determine_result(user_choice, cpu_choice)
    return cpu_choice, result
```

---

## 6. Referencias

- [PEP 8 - Style Guide for Python Code](https://www.python.org/dev/peps/pep-0008/)
- [PEP 257 - Docstring Conventions](https://www.python.org/dev/peps/pep-0257/)
- [PEP 484 - Type Hints](https://www.python.org/dev/peps/pep-0484/)

---

**Resumen**: El código de `rps.py` sigue correctamente los estándares PEP 8 y PEP 257, 
haciendo que sea legible, mantenible y profesional.
