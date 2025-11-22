#!/usr/bin/env python3
"""
Completar este programa de piedra, papel o tijera.

Instrucciones:
- El juego debe pedir al usuario "rock", "paper" o "scissors".
- Debe repetirse muchas veces.
- Si el usuario presiona ENTER sin escribir nada, termina el programa.
- La computadora debe elegir aleatoriamente entre las tres opciones.
- Debe mostrar quién ganó.
- Si el usuario gana, mostrar emojis divertidos (🎉✨🚀).
- Validar entradas incorrectas.
- Usar funciones y type hints modernos (Python 3.9+), ejemplo: tuple[str, str].
"""

import random

VALID_CHOICES = ["rock", "paper", "scissors"]


def determine_result(user: str, cpu: str) -> str:
    """
    Determina si el usuario gana, pierde o empata en el juego de piedra, papel o tijera.

    Args:
        user (str): La elección del usuario. Debe ser 'piedra', 'papel' o 'tijera'.
        cpu (str): La elección de la CPU. Debe ser 'piedra', 'papel' o 'tijera'.

    Returns:
        str: 'win' si el usuario gana, 'lose' si pierde, y 'draw' si empatan.
    """
    if user == cpu:
        return "draw"
    elif (user == "piedra" and cpu == "tijera") or \
         (user == "papel" and cpu == "piedra") or \
         (user == "tijera" and cpu == "papel"):
        return "win"
    else:
        return "lose"


def play(user_choice: str) -> tuple[str, str]:
    """
    Ejecutar una ronda del juego.

    Regresa una tupla:
        (eleccion_cpu, resultado)
    """
    cpu_choice = random.choice(VALID_CHOICES)
    result = determine_result(user_choice, cpu_choice)
    return cpu_choice, result


def main() -> None:
    """
    Hacer que el juego se repita usando un ciclo while.

    - Pedir la elección con input()
    - Salir si el usuario presiona ENTER
    - Mostrar:
        CPU: <elección>
        Resultado: <win/lose/draw>
    - Si el usuario gana, mostrar 🎉✨🎆🎇🚀
    """
    print("🎮 Rock, Paper, Scissors Game 🎮")
    print("Escribe rock, paper o scissors.")
    print("Presiona ENTER sin escribir nada para salir.")
    print("-" * 40)

    while True:
        user_input = input("Tu elección: ")
        if not user_input:
            break
        if user_input not in VALID_CHOICES:
            print("Elección no válida. Intenta de nuevo.")
            continue

        cpu_choice, result = play(user_input)

        print(f"CPU: {cpu_choice}")
        print(f"Resultado: {result}")

        if result == "win":
            print("🎉✨🎆🎇🚀 ¡Ganaste!")
        elif result == "lose":
            print("😢 Perdiste. Inténtalo de nuevo.")
        else:
            print("🤝 Empate. Ambos eligieron lo mismo.")

    print("Gracias por jugar. ¡Hasta luego!")


if __name__ == "__main__":
    main()
