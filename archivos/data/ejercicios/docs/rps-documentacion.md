# Documentación: Rock, Paper, Scissors Game

## Información General

- **Nombre del Programa**: Rock, Paper, Scissors Game
- **Versión**: 1.0
- **Archivo Principal**: `src/rps.py`
- **Lenguaje**: Python 3.9+
- **Estándar de Código**: PEP 8 y PEP 257

---

## 📋 Tabla de Contenidos

1. [Descripción General](#descripción-general)
2. [Estructura del Código](#estructura-del-código)
3. [Módulos y Variables](#módulos-y-variables)
4. [Funciones](#funciones)
5. [Flujo del Programa](#flujo-del-programa)
6. [Guía de Uso](#guía-de-uso)
7. [Ejemplos de Ejecución](#ejemplos-de-ejecución)
8. [Notas Técnicas](#notas-técnicas)

---

## Descripción General

El programa implementa el juego clásico de **Piedra, Papel o Tijera** entre un usuario y la computadora.

### Características Principales:
- ✅ Interfaz interactiva con emojis
- ✅ Validación de entradas del usuario
- ✅ Elección aleatoria de la CPU
- ✅ Lógica de comparación de movimientos
- ✅ Registro de estadísticas (victorias, derrotas, empates)
- ✅ Porcentaje de victorias
- ✅ Type hints modernos (Python 3.9+)
- ✅ Docstrings siguiendo PEP 257

---

## Estructura del Código

```
rps.py
├── Docstring del módulo
├── Imports
│   └── random
├── Constantes
│   └── VALID_CHOICES
├── Funciones
│   ├── determine_result()
│   ├── play()
│   └── main()
└── Bloque principal (__main__)
```

---

## Módulos y Variables

### Imports

```python
import random
```

- **random**: Módulo estándar de Python para generar números/elecciones aleatorias.

### Constantes

```python
VALID_CHOICES = ["rock", "paper", "scissors"]
```

| Nombre | Tipo | Valor | Descripción |
|--------|------|-------|-------------|
| `VALID_CHOICES` | `list[str]` | `["rock", "paper", "scissors"]` | Lista de opciones válidas del juego |

**Convención PEP 8**: Las constantes se escriben en **MAYÚSCULAS** con guiones bajos.

---

## Funciones

### 1. `determine_result(user: str, cpu: str) -> str`

**Propósito**: Determinar el resultado de una ronda comparando la elección del usuario con la de la CPU.

**Parámetros**:
| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `user` | `str` | Elección del usuario: `'rock'`, `'paper'` o `'scissors'` |
| `cpu` | `str` | Elección de la CPU: `'rock'`, `'paper'` o `'scissors'` |

**Retorna**: 
| Valor | Significado |
|-------|-------------|
| `'draw'` | Empate (ambos eligieron lo mismo) |
| `'win'` | Usuario gana |
| `'lose'` | Usuario pierde |

**Lógica**:
```
rock > scissors
paper > rock
scissors > paper
```

**Ejemplo**:
```python
determine_result("rock", "scissors")      # Retorna: 'win'
determine_result("paper", "rock")         # Retorna: 'win'
determine_result("scissors", "paper")     # Retorna: 'win'
determine_result("rock", "rock")          # Retorna: 'draw'
determine_result("rock", "paper")         # Retorna: 'lose'
```

---

### 2. `play(user_choice: str) -> tuple[str, str]`

**Propósito**: Ejecutar una ronda completa del juego.

**Parámetros**:
| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `user_choice` | `str` | Elección validada del usuario |

**Retorna**: 
```python
tuple[str, str]
```
- Elemento 0: Elección de la CPU (`'rock'`, `'paper'` o `'scissors'`)
- Elemento 1: Resultado (`'win'`, `'lose'` o `'draw'`)

**Flujo interno**:
1. Elige aleatoriamente una opción para la CPU
2. Compara con la elección del usuario usando `determine_result()`
3. Retorna una tupla con ambos valores

**Ejemplo**:
```python
cpu_choice, result = play("rock")
# Posible retorno: ('scissors', 'win')
```

---

### 3. `main() -> None`

**Propósito**: Función principal que controla el flujo del juego.

**Parámetros**: Ninguno

**Retorna**: `None`

**Responsabilidades**:
1. Mostrar interfaz de bienvenida
2. Inicializar contadores de estadísticas
3. Solicitar entrada del usuario en bucle
4. Validar entrada
5. Ejecutar una ronda de juego
6. Actualizar contadores
7. Mostrar resultados
8. Al salir: mostrar estadísticas finales

**Variables Locales**:
| Variable | Tipo | Propósito |
|----------|------|----------|
| `user_input` | `str` | Entrada del usuario (convertida a minúsculas y sin espacios) |
| `wins` | `int` | Contador de victorias |
| `losses` | `int` | Contador de derrotas |
| `draws` | `int` | Contador de empates |
| `cpu_choice` | `str` | Elección de la CPU en la ronda actual |
| `result` | `str` | Resultado de la ronda actual |
| `total_games` | `int` | Total de rondas jugadas |
| `win_rate` | `float` | Porcentaje de victorias |

**Flujo del programa**:
```
1. Mostrar menú inicial
2. Inicializar contadores (wins=0, losses=0, draws=0)
3. MIENTRAS True:
   a. Pedir entrada al usuario
   b. Si está vacía → SALIR
   c. Si es inválida → Mostrar error y CONTINUAR
   d. Ejecutar ronda
   e. Actualizar contador según resultado
   f. Mostrar resultado
4. Mostrar estadísticas finales
```

---

## Flujo del Programa

```
INICIO
  │
  ├─→ Mostrar bienvenida
  │
  ├─→ Inicializar contadores (wins, losses, draws)
  │
  ├─→ BUCLE PRINCIPAL:
  │   │
  │   ├─→ Pedir entrada usuario
  │   │
  │   ├─→ ¿Entrada vacía?
  │   │   ├─→ SÍ: Ir a "ESTADÍSTICAS FINALES"
  │   │   └─→ NO: Continuar
  │   │
  │   ├─→ ¿Entrada válida?
  │   │   ├─→ NO: Mostrar error → Volver a BUCLE PRINCIPAL
  │   │   └─→ SÍ: Continuar
  │   │
  │   ├─→ CPU elige aleatoriamente
  │   │
  │   ├─→ Comparar elecciones
  │   │
  │   ├─→ Actualizar contador según resultado
  │   │
  │   ├─→ Mostrar resultado con emojis
  │   │
  │   └─→ Volver a BUCLE PRINCIPAL
  │
  ├─→ ESTADÍSTICAS FINALES:
  │   ├─→ Mostrar total de victorias
  │   ├─→ Mostrar total de derrotas
  │   ├─→ Mostrar total de empates
  │   ├─→ Calcular y mostrar porcentaje de victorias
  │   └─→ Mostrar mensaje de despedida
  │
  └─→ FIN
```

---

## Guía de Uso

### Requisitos
- Python 3.9 o superior
- Sistema operativo: Linux, macOS o Windows

### Instalación
```bash
# No requiere instalación de dependencias externas
# Solo usa módulos estándar de Python
```

### Ejecución

**Opción 1: Directamente**
```bash
python3 src/rps.py
```

**Opción 2: Con shebang**
```bash
chmod +x src/rps.py
./src/rps.py
```

### Interacción

1. **Lanzar el programa**
2. **Ingresar una opción**:
   - Acepta: `rock`, `paper`, `scissors`
   - Insensible a mayúsculas: `Rock`, `PAPER`, `ScISSoRS` funcionan
   - Tolera espacios en blanco al inicio/final
3. **Ver resultado**: La computadora muestra su elección y el resultado
4. **Repetir**: El juego continúa hasta que presiones ENTER vacío

---

## Ejemplos de Ejecución

### Ejemplo 1: Sesión Completa

```
🎮 Rock, Paper, Scissors Game 🎮
Escribe rock, paper o scissors.
Presiona ENTER sin escribir nada para salir.
----------------------------------------
Tu elección: rock
CPU: scissors
Resultado: win
🎉✨🎆🎇🚀 ¡Ganaste!

Tu elección: paper
CPU: paper
Resultado: draw
🤝 Empate. Ambos eligieron lo mismo.

Tu elección: scissors
CPU: rock
Resultado: lose
😢 Perdiste. Inténtalo de nuevo.

Tu elección: 
----------------------------------------
📊 ESTADÍSTICAS FINALES 📊
✅ Victorias: 1
❌ Derrotas: 1
🤝 Empates: 1
📈 Porcentaje de victorias: 33.3%
Gracias por jugar. ¡Hasta luego!
```

### Ejemplo 2: Entrada Inválida

```
Tu elección: piedra
❌ Elección no válida. Elige entre: rock, paper, scissors
Tu elección: rock
```

### Ejemplo 3: Insensibilidad a Mayúsculas

```
Tu elección: ROCK
CPU: scissors
Resultado: win
🎉✨🎆🎇🚀 ¡Ganaste!
```

---

## Notas Técnicas

### Type Hints (PEP 484)

El código utiliza type hints modernos de Python 3.9+:

```python
# Antes (Python 3.8):
from typing import Tuple
def play(user_choice: str) -> Tuple[str, str]:
    pass

# Ahora (Python 3.9+):
def play(user_choice: str) -> tuple[str, str]:
    pass
```

### Docstrings (PEP 257)

Cada función tiene un docstring que describe:
- Propósito
- Parámetros (con tipos y descripción)
- Valor de retorno
- Ejemplos (cuando es relevante)

```python
def determine_result(user: str, cpu: str) -> str:
    """
    Descripción breve.
    
    Descripción detallada (si es necesaria).
    
    Args:
        user (str): Descripción
        cpu (str): Descripción
    
    Returns:
        str: Descripción
    """
```

### Formato de Código (PEP 8)

✅ **Cumplimientos**:
- Nombres de constantes en MAYÚSCULAS: `VALID_CHOICES`
- Funciones en snake_case: `determine_result()`, `play()`, `main()`
- Líneas con máximo 79 caracteres (excepto líneas largas necesarias)
- Dos líneas en blanco entre funciones
- Cuatro espacios de indentación
- Docstrings con comillas triples

### Seguridad

- ✅ Validación de entrada antes de procesarla
- ✅ Manejo de entradas vacías
- ✅ Conversión a minúsculas para comparación segura
- ✅ Uso de `random.choice()` seguro para generación aleatoria

### Rendimiento

- O(1): Todas las operaciones son constantes
- Uso mínimo de memoria
- Sin dependencias externas

### Extensibilidad

Para agregar nuevas opciones:

```python
# Cambiar constante
VALID_CHOICES = ["rock", "paper", "scissors", "lizard", "spock"]

# Actualizar lógica en determine_result()
# Actualizar mensajes de interfaz
```

---

## Mejoras Futuras

1. **Archivo de configuración**: Guardar preferencias en JSON
2. **Persistencia**: Guardar estadísticas en base de datos
3. **Dificultad**: Agregar niveles de dificultad para la IA
4. **Multijugador**: Permitir juegos entre dos usuarios
5. **Tests**: Agregar suite de pruebas unitarias
6. **Interfaz Gráfica**: Versión con tkinter o PyQt
7. **Internacionalización**: Soporte para múltiples idiomas

---

## Conclusión

Este programa es un ejemplo educativo completo que demuestra:
- ✅ Buenas prácticas de Python (PEP 8, PEP 257)
- ✅ Type hints modernos
- ✅ Estructura modular con funciones
- ✅ Validación de entradas
- ✅ Lógica clara y mantenible
- ✅ Interfaz amigable con feedback visual

**Perfecto para aprendizaje de conceptos fundamentales de programación.**

---

## Autor
**Proyecto Educativo** - Bioinformática

Fecha de creación: 26 de noviembre de 2025
