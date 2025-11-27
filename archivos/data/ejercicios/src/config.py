#!/usr/bin/env python3
"""Configuración del juego Rock, Paper, Scissors.

Este módulo contiene todas las constantes y configuraciones del juego
que pueden ser personalizadas según las preferencias del usuario.
"""

# Opciones válidas del juego
VALID_CHOICES = ["rock", "paper", "scissors"]

# Emojis para cada opción
EMOJIS = {
    "rock": "🪨",
    "paper": "📄",
    "scissors": "✂️",
}

# Emojis para resultados
RESULT_EMOJIS = {
    "win": "🎉✨🎆🎇🚀",
    "lose": "😢",
    "draw": "🤝",
}

# Mensajes personalizables
MESSAGES = {
    "welcome": "🎮 Rock, Paper, Scissors Game 🎮",
    "instructions": "Escribe rock, paper o scissors.",
    "exit_instruction": "Presiona ENTER sin escribir nada para salir.",
    "invalid_choice": "❌ Elección no válida. Elige entre: {choices}",
    "win": "🎉✨🎆🎇🚀 ¡Ganaste!",
    "lose": "😢 Perdiste. Inténtalo de nuevo.",
    "draw": "🤝 Empate. Ambos eligieron lo mismo.",
    "final_stats": "📊 ESTADÍSTICAS FINALES 📊",
    "thanks": "Gracias por jugar. ¡Hasta luego!",
}

# Configuración de límites
MAX_GAMES = None  # None = sin límite, establecer número para límite
MIN_INPUT_LENGTH = 1
MAX_INPUT_LENGTH = 20

# Configuración de persistencia
STATS_FILE = "game_stats.json"
LOG_FILE = "game.log"

# Configuración de logging
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Configuración de visualización
SHOW_EMOJIS = True
SHOW_CPU_CHOICE = True
VERBOSE_MODE = False

# Separador visual
SEPARATOR = "-" * 40
