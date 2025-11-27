#!/usr/bin/env python3
"""Rock, Paper, Scissors Game - Juego interactivo entre usuario y computadora.

Este módulo implementa el juego clásico de Piedra, Papel o Tijera con las
siguientes características:

    - Interfaz interactiva con emojis
    - Elección aleatoria de la computadora
    - Validación robusta de entradas del usuario
    - Registro de estadísticas (victorias, derrotas, empates)
    - Type hints modernos (Python 3.9+)
    - Docstrings siguiendo PEP 257
    - Manejo completo de excepciones

Uso:
    python3 rps.py

Requisitos:
    Python 3.9+

Autor:
    Proyecto Educativo - Bioinformática

Versión:
    1.0
"""

import random
import re
from typing import Optional

# ============================================================================
# CONSTANTES Y CONFIGURACIÓN
# ============================================================================

VALID_CHOICES = ["rock", "paper", "scissors"]
MIN_INPUT_LENGTH = 1
MAX_INPUT_LENGTH = 20

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

SEPARATOR = "-" * 40

# ============================================================================
# FUNCIONES PRINCIPALES
# ============================================================================


def validate_input(user_input: str) -> Optional[str]:
    """Validar entrada del usuario de forma robusta.

    Realiza validaciones:
    - No está vacía o contiene solo espacios
    - Longitud entre MIN_INPUT_LENGTH y MAX_INPUT_LENGTH
    - Contiene solo letras y espacios
    - Es una opción válida después de normalizar

    Args:
        user_input (str): Entrada a validar.

    Returns:
        Optional[str]: Opción válida en minúsculas, o None si es inválida.

    Example:
        >>> validate_input("rock")
        'rock'
        >>> validate_input("PAPER")
        'paper'
        >>> validate_input("   scissors   ")
        'scissors'
        >>> validate_input("")
        None
        >>> validate_input("invalid")
        None
    """
    # Validar que no está vacía
    if not user_input or not user_input.strip():
        return None

    # Normalizar entrada
    normalized = user_input.strip().lower()

    # Validar longitud
    if (
        len(normalized) < MIN_INPUT_LENGTH
        or len(normalized) > MAX_INPUT_LENGTH
    ):
        return None

    # Validar caracteres (solo letras y espacios)
    if not re.match(r"^[a-z\s]+$", normalized):
        return None

    # Validar que sea una opción válida
    if normalized not in VALID_CHOICES:
        return None

    return normalized


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
        >>> determine_result('paper', 'rock')
        'win'
        >>> determine_result('scissors', 'paper')
        'win'
        >>> determine_result('rock', 'rock')
        'draw'
        >>> determine_result('rock', 'paper')
        'lose'
    """
    if user == cpu:
        return "draw"
    elif (user == "rock" and cpu == "scissors") or \
         (user == "paper" and cpu == "rock") or \
         (user == "scissors" and cpu == "paper"):
        return "win"
    else:
        return "lose"


def play(user_choice: str) -> tuple[str, str]:
    """Ejecutar una ronda del juego.

    Genera una elección aleatoria para la CPU, compara ambas elecciones
    y determina el resultado de la ronda.

    Args:
        user_choice (str): La elección validada del usuario.
                          Debe ser 'rock', 'paper' o 'scissors'.

    Returns:
        tuple[str, str]: Una tupla con dos elementos:
            - cpu_choice (str): La elección aleatoria de la CPU
            - result (str): El resultado de la comparación
                           ('win', 'lose' o 'draw')

    Example:
        >>> cpu_choice, result = play('rock')
        >>> # Posible resultado: ('scissors', 'win')
    """
    cpu_choice = random.choice(VALID_CHOICES)
    result = determine_result(user_choice, cpu_choice)
    return cpu_choice, result


def main() -> None:
    """Ejecutar el flujo principal del juego interactivo.

    Controla el bucle principal del juego que:
    - Solicita opciones al usuario repetidamente
    - Valida las entradas de forma robusta
    - Ejecuta rondas de juego con manejo de excepciones
    - Actualiza y muestra resultados
    - Finaliza con estadísticas completas

    Returns:
        None
    """
    try:
        # Mostrar menú
        print(MESSAGES["welcome"])
        print(MESSAGES["instructions"])
        print(MESSAGES["exit_instruction"])
        print(SEPARATOR)

        # Contadores de estadísticas
        wins = 0
        losses = 0
        draws = 0
        total_rounds = 0

        while True:
            try:
                # Obtener entrada del usuario
                user_input = input("Tu elección: ")

                # Si está vacía, salir
                if not user_input.strip():
                    break

                # Validar entrada
                validated_choice = validate_input(user_input)
                if validated_choice is None:
                    choices_str = ", ".join(VALID_CHOICES)
                    print(MESSAGES["invalid_choice"].format(choices=choices_str))
                    continue

                # Ejecutar ronda
                cpu_choice, result = play(validated_choice)
                total_rounds += 1

                # Mostrar resultado
                print(f"CPU: {cpu_choice}")
                print(f"Resultado: {result}")

                # Actualizar contadores
                if result == "win":
                    print(MESSAGES["win"])
                    wins += 1
                elif result == "lose":
                    print(MESSAGES["lose"])
                    losses += 1
                else:
                    print(MESSAGES["draw"])
                    draws += 1

                print()  # Línea en blanco para claridad

            except KeyboardInterrupt:
                print("\n\n⚠️  Juego interrumpido por el usuario.")
                break
            except Exception as e:
                print(f"❌ Error inesperado: {e}. Intenta de nuevo.")
                continue

        # Mostrar estadísticas finales
        print(SEPARATOR)
        print(MESSAGES["final_stats"])
        print(f"✅ Victorias: {wins}")
        print(f"❌ Derrotas: {losses}")
        print(f"🤝 Empates: {draws}")
        print(f"📊 Total de rondas: {total_rounds}")

        if total_rounds > 0:
            win_rate = (wins / total_rounds) * 100
            print(f"📈 Porcentaje de victorias: {win_rate:.1f}%")

        print(MESSAGES["thanks"])

    except Exception as e:
        print(f"❌ Error crítico: {e}")
        return


if __name__ == "__main__":
    main()
