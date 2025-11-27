#!/usr/bin/env python3
"""Módulo para gestionar la persistencia de datos del juego.

Maneja la guardado y carga de estadísticas en archivo JSON.
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


class GameStats:
    """Clase para gestionar las estadísticas del juego."""

    def __init__(self, stats_file: str = "game_stats.json"):
        """Inicializar gestor de estadísticas.

        Args:
            stats_file (str): Ruta del archivo JSON para guardar estadísticas.
        """
        self.stats_file = Path(stats_file)
        self.current_session = {
            "timestamp": datetime.now().isoformat(),
            "wins": 0,
            "losses": 0,
            "draws": 0,
        }
        self.all_sessions = self._load_stats()

    def _load_stats(self) -> list:
        """Cargar estadísticas previas del archivo.

        Returns:
            list: Lista de sesiones anteriores, o lista vacía si no existe.
        """
        if not self.stats_file.exists():
            logger.info("Archivo de estadísticas no encontrado. Creando nuevo.")
            return []

        try:
            with open(self.stats_file, "r", encoding="utf-8") as f:
                stats = json.load(f)
                logger.info(f"Estadísticas cargadas: {len(stats)} sesiones")
                return stats
        except json.JSONDecodeError:
            logger.error("Error al decodificar JSON. Iniciando con estadísticas vacías.")
            return []
        except IOError as e:
            logger.error(f"Error al leer archivo: {e}")
            return []

    def update_session(self, wins: int, losses: int, draws: int) -> None:
        """Actualizar estadísticas de la sesión actual.

        Args:
            wins (int): Número de victorias.
            losses (int): Número de derrotas.
            draws (int): Número de empates.
        """
        self.current_session["wins"] = wins
        self.current_session["losses"] = losses
        self.current_session["draws"] = draws

    def save_session(self) -> bool:
        """Guardar la sesión actual en el archivo.

        Returns:
            bool: True si se guardó exitosamente, False en caso contrario.
        """
        try:
            self.all_sessions.append(self.current_session)
            with open(self.stats_file, "w", encoding="utf-8") as f:
                json.dump(self.all_sessions, f, indent=2, ensure_ascii=False)
            logger.info("Sesión guardada exitosamente.")
            return True
        except IOError as e:
            logger.error(f"Error al guardar estadísticas: {e}")
            return False

    def get_total_stats(self) -> dict:
        """Obtener estadísticas totales de todas las sesiones.

        Returns:
            dict: Diccionario con estadísticas totales.
        """
        total_wins = sum(s["wins"] for s in self.all_sessions)
        total_losses = sum(s["losses"] for s in self.all_sessions)
        total_draws = sum(s["draws"] for s in self.all_sessions)
        total_games = total_wins + total_losses + total_draws

        return {
            "total_sessions": len(self.all_sessions),
            "total_games": total_games,
            "total_wins": total_wins,
            "total_losses": total_losses,
            "total_draws": total_draws,
            "win_rate": (total_wins / total_games * 100) if total_games > 0 else 0,
        }

    def get_last_sessions(self, count: int = 5) -> list:
        """Obtener las últimas N sesiones.

        Args:
            count (int): Número de sesiones a retornar.

        Returns:
            list: Lista de las últimas sesiones.
        """
        return self.all_sessions[-count:]


def setup_logging(log_file: str = "game.log", level: str = "INFO") -> None:
    """Configurar el sistema de logging.

    Args:
        log_file (str): Ruta del archivo de log.
        level (str): Nivel de logging (DEBUG, INFO, WARNING, ERROR, CRITICAL).
    """
    log_path = Path(log_file)

    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_path, encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )
    logger.info("Sistema de logging inicializado.")
