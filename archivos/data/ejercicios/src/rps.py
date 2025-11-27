#!/usr/bin/env python3
"""Rock, Paper, Scissors Game - Juego interactivo entre usuario y computadora.

Este módulo implementa el juego clásico de Piedra, Papel o Tijera con las
siguientes características:

    - Interfaz interactiva con emojis
    - Elección aleatoria de la computadora
    - Validación robusta de entradas del usuario
    - Registro de estadísticas (victorias, derrotas, empates)
    - Persistencia de datos en JSON
    - Type hints modernos (Python 3.9+)
    - Docstrings siguiendo PEP 257
    - Manejo completo de excepciones
    - Sistema de logging

Uso:
    python3 rps.py [OPTIONS]

Author:
    Proyecto Educativo - Bioinformática

Version:
    2.0

Requisitos:
    Python 3.9+
"""

import argparse
import logging
import random
import re
import sys
from typing import Optional

import config
from game_stats import GameStats, setup_logging

logger = logging.getLogger(__name__)

# Usar constantes del módulo de configuración
VALID_CHOICES = config.VALID_CHOICES


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
    if not user_input or not user_input.strip():
        return None

    normalized = user_input.strip().lower()

    if (
        len(normalized) < config.MIN_INPUT_LENGTH
        or len(normalized) > config.MAX_INPUT_LENGTH
    ):
        logger.warning(f"Entrada fuera de rango: {repr(user_input)}")
        return None

    if not re.match(r"^[a-z\s]+$", normalized):
        logger.warning(f"Entrada con caracteres inválidos: {repr(user_input)}")
        return None

    if normalized not in VALID_CHOICES:
        logger.warning(f"Opción no válida: {normalized}")
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


def main(
    show_emojis: bool = True, max_games: Optional[int] = None, verbose: bool = False
) -> None:
    """Ejecutar el flujo principal del juego interactivo.

    Controla el bucle principal del juego que:
    - Solicita opciones al usuario repetidamente
    - Valida las entradas de forma robusta
    - Ejecuta rondas de juego con manejo de excepciones
    - Actualiza y muestra resultados
    - Guarda estadísticas en archivo
    - Finaliza con estadísticas completas

    Args:
        show_emojis (bool): Si mostrar emojis en la interfaz.
        max_games (Optional[int]): Número máximo de juegos (None = sin límite).
        verbose (bool): Modo verbose con información adicional.

    Returns:
        None

    Note:
        - Esta función no retorna valor. Es la función principal del programa.
        - Las estadísticas se guardan automáticamente al finalizar.
        - Todos los errores se registran en el archivo de log.
    """
    try:
        # Inicializar gestor de estadísticas
        stats = GameStats(config.STATS_FILE)
        logger.info("Gestor de estadísticas inicializado.")

        # Mostrar menú
        print(config.MESSAGES["welcome"])
        print(config.MESSAGES["instructions"])
        print(config.MESSAGES["exit_instruction"])
        print(config.SEPARATOR)
        logger.info("Juego iniciado.")

        # Contadores de estadísticas
        wins = 0
        losses = 0
        draws = 0
        total_rounds = 0

        while True:
            try:
                # Verificar límite de juegos
                if max_games and total_rounds >= max_games:
                    logger.info(f"Límite de juegos alcanzado: {max_games}")
                    print(
                        f"\n⚠️  Límite de {max_games} juegos alcanzado. "
                        "¡Presiona ENTER para salir!"
                    )
                    input()
                    break

                # Obtener entrada del usuario
                user_input = input("Tu elección: ")

                # Si está vacía, salir
                if not user_input.strip():
                    logger.info("Usuario solicitó salir.")
                    break

                # Validar entrada
                validated_choice = validate_input(user_input)
                if validated_choice is None:
                    choices_str = ", ".join(VALID_CHOICES)
                    print(config.MESSAGES["invalid_choice"].format(choices=choices_str))
                    logger.warning(f"Entrada inválida: {repr(user_input)}")
                    continue

                # Ejecutar ronda
                cpu_choice, result = play(validated_choice)
                total_rounds += 1

                # Mostrar resultado
                if config.SHOW_CPU_CHOICE:
                    print(f"CPU: {cpu_choice}")
                print(f"Resultado: {result}")

                # Actualizar contadores
                if result == "win":
                    win_msg = config.MESSAGES["win"]
                    print(win_msg)
                    wins += 1
                    logger.info(f"Ronda {total_rounds}: VICTORIA")
                elif result == "lose":
                    print(config.MESSAGES["lose"])
                    losses += 1
                    logger.info(f"Ronda {total_rounds}: DERROTA")
                else:
                    print(config.MESSAGES["draw"])
                    draws += 1
                    logger.info(f"Ronda {total_rounds}: EMPATE")

                if verbose:
                    print(f"  [Tu elección: {validated_choice}, CPU: {cpu_choice}]")

                print()  # Línea en blanco para claridad

            except KeyboardInterrupt:
                logger.info("Usuario interrumpió con Ctrl+C.")
                print("\n\n⚠️  Juego interrumpido por el usuario.")
                break
            except Exception as e:
                logger.error(f"Error durante la ronda: {e}", exc_info=True)
                print(f"❌ Error inesperado: {e}. Intenta de nuevo.")
                continue

        # Mostrar estadísticas finales
        print(config.SEPARATOR)
        print(config.MESSAGES["final_stats"])
        print(f"✅ Victorias: {wins}")
        print(f"❌ Derrotas: {losses}")
        print(f"🤝 Empates: {draws}")
        print(f"📊 Total de rondas: {total_rounds}")

        if total_rounds > 0:
            win_rate = (wins / total_rounds) * 100
            print(f"📈 Porcentaje de victorias: {win_rate:.1f}%")
            logger.info(
                f"Sesión finalizada: {wins}W-{losses}L-{draws}D "
                f"({win_rate:.1f}% victorias)"
            )
        else:
            logger.info("Sesión finalizada sin juegos completados.")

        # Guardar estadísticas
        stats.update_session(wins, losses, draws)
        if stats.save_session():
            print("💾 Estadísticas guardadas exitosamente.")
        else:
            print("⚠️  No se pudieron guardar las estadísticas.")

        # Mostrar estadísticas totales
        total_stats = stats.get_total_stats()
        if total_stats["total_sessions"] > 1:
            print("\n📊 ESTADÍSTICAS TOTALES (todas las sesiones)")
            print(f"   Sesiones jugadas: {total_stats['total_sessions']}")
            print(f"   Total de juegos: {total_stats['total_games']}")
            print(f"   Total victorias: {total_stats['total_wins']}")
            print(f"   Tasa de victoria global: {total_stats['win_rate']:.1f}%")

        print(config.MESSAGES["thanks"])
        logger.info("Juego finalizado correctamente.")

    except Exception as e:
        logger.critical(f"Error crítico en main(): {e}", exc_info=True)
        print(f"❌ Error crítico: {e}")
        sys.exit(1)


def parse_arguments() -> argparse.Namespace:
    """Parsear argumentos de línea de comandos.

    Returns:
        argparse.Namespace: Objeto con los argumentos parseados.
    """
    parser = argparse.ArgumentParser(
        description="Juego interactivo de Piedra, Papel o Tijera",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  python3 rps.py                    # Juego normal
  python3 rps.py --no-emoji         # Sin emojis
  python3 rps.py --max-games 10     # Máximo 10 juegos
  python3 rps.py --verbose          # Modo verbose
  python3 rps.py --verbose --max-games 5 --no-emoji  # Combinado
        """,
    )

    parser.add_argument(
        "--no-emoji",
        action="store_true",
        help="Deshabilitar emojis en la interfaz",
    )
    parser.add_argument(
        "--max-games",
        type=int,
        default=None,
        help="Número máximo de juegos a jugar",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Modo verbose con información adicional",
    )
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default="INFO",
        help="Nivel de logging (por defecto: INFO)",
    )

    return parser.parse_args()


if __name__ == "__main__":
    try:
        # Parsear argumentos
        args = parse_arguments()

        # Configurar logging
        setup_logging(config.LOG_FILE, args.log_level)

        # Ejecutar juego
        main(
            show_emojis=not args.no_emoji,
            max_games=args.max_games,
            verbose=args.verbose,
        )

    except KeyboardInterrupt:
        print("\n\n⚠️  Programa interrumpido por el usuario.")
        sys.exit(0)
    except Exception as e:
        logger.critical(f"Error crítico: {e}", exc_info=True)
        print(f"❌ Error crítico: {e}")
        sys.exit(1)
