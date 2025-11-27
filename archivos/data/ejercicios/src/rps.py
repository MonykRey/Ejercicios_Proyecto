#!/usr/bin/env python3
"""Rock, Paper, Scissors Game - Juego interactivo entre usuario y computadora.

Este módulo implementa el juego clásico de Piedra, Papel o Tijera con las
siguientes características:

    - Interfaz interactiva con emojis
    - Elección aleatoria de la computadora
    - Validación de entradas del usuario
    - Registro de estadísticas (victorias, derrotas, empates)
    - Type hints modernos (Python 3.9+)
    - Docstrings siguiendo PEP 257

Uso:
    python3 rps.py

Author:
    Proyecto Educativo - Bioinformática

Version:
    1.0

Requisitos:
    Python 3.9+
"""

import random

VALID_CHOICES = ["rock", "paper", "scissors"]


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

    Raises:
        Ninguna. Asume que las entradas son válidas.

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
    - Valida las entradas
    - Ejecuta rondas de juego
    - Actualiza y muestra resultados
    - Finaliza con estadísticas completas

    Flujo:
    - El juego continúa hasta que el usuario presione ENTER sin escribir
    - Para cada ronda válida se muestra la elección de la CPU y el resultado
    - Se mantiene conteo de victorias, derrotas y empates
    - Al finalizar muestra estadísticas con porcentaje de victorias

    Returns:
        None

    Note:
        Esta función no retorna valor. Es la función principal del programa.
    """
    print("🎮 Rock, Paper, Scissors Game 🎮")
    print("Escribe rock, paper o scissors.")
    print("Presiona ENTER sin escribir nada para salir.")
    print("-" * 40)

    # Contadores de estadísticas
    wins = 0
    losses = 0
    draws = 0

    while True:
        user_input = input("Tu elección: ").lower().strip()
        if not user_input:
            break
        if user_input not in VALID_CHOICES:
            print(f"❌ Elección no válida. Elige entre: {', '.join(VALID_CHOICES)}")
            continue

        cpu_choice, result = play(user_input)

        print(f"CPU: {cpu_choice}")
        print(f"Resultado: {result}")

        if result == "win":
            print("🎉✨🎆🎇🚀 ¡Ganaste!")
            wins += 1
        elif result == "lose":
            print("😢 Perdiste. Inténtalo de nuevo.")
            losses += 1
        else:
            print("🤝 Empate. Ambos eligieron lo mismo.")
            draws += 1

        print()  # Línea en blanco para claridad

    # Mostrar estadísticas finales
    print("-" * 40)
    print("📊 ESTADÍSTICAS FINALES 📊")
    print(f"✅ Victorias: {wins}")
    print(f"❌ Derrotas: {losses}")
    print(f"🤝 Empates: {draws}")
    
    total_games = wins + losses + draws
    if total_games > 0:
        win_rate = (wins / total_games) * 100
        print(f"📈 Porcentaje de victorias: {win_rate:.1f}%")
    
    print("Gracias por jugar. ¡Hasta luego!")


if __name__ == "__main__":
    main()
