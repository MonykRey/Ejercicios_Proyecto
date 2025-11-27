# 🎮 Rock, Paper, Scissors Game

Un juego interactivo de Piedra, Papel o Tijera implementado en Python con características profesionales.

## ✨ Características

- 🎯 Juego interactivo entre usuario y computadora
- ✅ Validación robusta de entradas
- 📊 Estadísticas de victorias, derrotas y empates
- 💾 Persistencia de datos en JSON
- 🔧 Configuración personalizable
- 📝 Sistema de logging completo
- 🧪 Suite de tests unitarios
- 🎨 Interfaz con emojis
- ⌨️ Opciones de línea de comandos

## 📋 Requisitos

- Python 3.9 o superior
- Módulos estándar (no requiere dependencias externas)

## 🚀 Instalación y Uso

### Uso básico

```bash
python3 src/rps.py
```

### Opciones de línea de comandos

```bash
# Ver ayuda
python3 src/rps.py --help

# Sin emojis
python3 src/rps.py --no-emoji

# Limitar a 10 juegos
python3 src/rps.py --max-games 10

# Modo verbose (información detallada)
python3 src/rps.py --verbose

# Cambiar nivel de logging
python3 src/rps.py --log-level DEBUG

# Combinar opciones
python3 src/rps.py --verbose --max-games 5 --no-emoji
```

## 🎮 Cómo Jugar

1. **Ejecuta el programa**
2. **Ingresa tu elección**: `rock`, `paper` o `scissors`
3. **La computadora elige aleatoriamente**
4. **Se comparan los resultados**
5. **Se actualiza la puntuación**
6. **Repite o presiona ENTER para salir**

### Reglas del Juego

- **Rock** (Piedra) ✊ vence a **Scissors** (Tijera)
- **Paper** (Papel) ✋ vence a **Rock** (Piedra)
- **Scissors** (Tijera) ✌️ vence a **Paper** (Papel)
- Si ambos eligen lo mismo, es un **empate**

## 📁 Estructura del Proyecto

```
ejercicios/
├── src/
│   ├── __init__.py
│   ├── rps.py              # Programa principal
│   ├── config.py           # Configuración
│   └── game_stats.py       # Gestión de estadísticas
├── tests/
│   ├── __init__.py
│   └── test_rps.py         # Tests unitarios
├── docs/
│   ├── rps-documentacion.md          # Documentación completa
│   ├── PEP8-guia-aplicada.md         # Guía de estilo PEP8
│   ├── rps_instrucciones.md          # Instrucciones del proyecto
│   └── rps-documentacion.md          # Documentación de API
└── README.md               # Este archivo
```

## 🧪 Tests

### Ejecutar todos los tests

```bash
python3 tests/test_rps.py
```

### Ejecutar con más detalle

```bash
python3 -m unittest tests.test_rps -v
```

### Tests disponibles

- ✅ Tests de determinación de resultados (`determine_result()`)
- ✅ Tests de validación de entrada (`validate_input()`)
- ✅ Tests de ejecución de ronda (`play()`)
- ✅ Tests de constantes y configuración
- ✅ Tests de integración

## 💾 Persistencia de Datos

Las estadísticas se guardan automáticamente en `game_stats.json`:

```json
[
  {
    "timestamp": "2025-11-26T10:30:45.123456",
    "wins": 5,
    "losses": 2,
    "draws": 1
  },
  {
    "timestamp": "2025-11-26T11:00:00.123456",
    "wins": 3,
    "losses": 3,
    "draws": 2
  }
]
```

## 📝 Logging

Los eventos se registran en `game.log`:

```
2025-11-26 10:30:45,123 - rps - INFO - Juego iniciado.
2025-11-26 10:30:48,456 - rps - INFO - Ronda 1: VICTORIA
2025-11-26 10:30:50,789 - rps - INFO - Ronda 2: DERROTA
2025-11-26 10:31:00,111 - rps - INFO - Sesión finalizada: 1W-1L-0D (50.0% victorias)
```

## 🔧 Configuración

Editar `src/config.py` para personalizar:

```python
# Opciones del juego
VALID_CHOICES = ["rock", "paper", "scissors"]

# Mensajes
MESSAGES = {
    "welcome": "🎮 Rock, Paper, Scissors Game 🎮",
    # ...
}

# Archivos
STATS_FILE = "game_stats.json"
LOG_FILE = "game.log"

# Límites
MAX_GAMES = None  # None = sin límite
MAX_INPUT_LENGTH = 20
```

## 📊 Estadísticas

Después de cada sesión se muestran:

```
----------------------------------------
📊 ESTADÍSTICAS FINALES 📊
✅ Victorias: 7
❌ Derrotas: 3
🤝 Empates: 2
📊 Total de rondas: 12
📈 Porcentaje de victorias: 58.3%

📊 ESTADÍSTICAS TOTALES (todas las sesiones)
   Sesiones jugadas: 5
   Total de juegos: 52
   Total victorias: 32
   Tasa de victoria global: 61.5%

Gracias por jugar. ¡Hasta luego!
```

## 🐛 Manejo de Errores

El programa maneja:

- ✅ Entradas inválidas (caracteres especiales, números)
- ✅ Errores de lectura/escritura de archivos
- ✅ Interrupciones del usuario (Ctrl+C)
- ✅ Errores inesperados (sin bloquear el programa)

## 📚 Documentación Adicional

- [rps-documentacion.md](docs/rps-documentacion.md) - Documentación completa
- [PEP8-guia-aplicada.md](docs/PEP8-guia-aplicada.md) - Guía de estilo
- [rps_instrucciones.md](docs/rps_instrucciones.md) - Instrucciones del proyecto

## 💡 Mejoras Futuras

- [ ] Interfaz gráfica (tkinter/PyQt)
- [ ] Modo multijugador
- [ ] Diferentes variantes (Rock-Paper-Scissors-Lizard-Spock)
- [ ] API REST
- [ ] Base de datos para rankings
- [ ] Soporte para múltiples idiomas

## 🤝 Contribuciones

Este es un proyecto educativo. Siéntete libre de:

- Reportar bugs
- Sugerir mejoras
- Agregar nuevas funcionalidades
- Mejorar la documentación

## 📄 Licencia

Proyecto Educativo - Bioinformática

## 👨‍💻 Autor

Proyecto Educativo - Bioinformática

---

## 🎓 Conceptos Aprendidos

Este proyecto demuestra:

- ✅ Fundamentos de Python (variables, funciones, bucles)
- ✅ Type hints (PEP 484)
- ✅ Docstrings profesionales (PEP 257)
- ✅ Estilo de código (PEP 8)
- ✅ Manejo de excepciones
- ✅ Tests unitarios
- ✅ Persistencia de datos (JSON)
- ✅ Logging
- ✅ Interfaces de línea de comandos (argparse)
- ✅ Buenas prácticas de programación

¡Disfruta jugando! 🎮✨
