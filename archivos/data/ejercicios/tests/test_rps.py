#!/usr/bin/env python3
"""Tests unitarios para Rock, Paper, Scissors Game.

Suite de pruebas usando unittest para validar todas las funciones
del módulo rps.
"""

import unittest
from unittest.mock import patch, MagicMock
import sys
from pathlib import Path

# Agregar src al path para importar módulos
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import config
import rps


class TestDetermineResult(unittest.TestCase):
    """Tests para la función determine_result()."""

    def test_draw_scenarios(self):
        """Probar todos los casos de empate."""
        self.assertEqual(rps.determine_result("rock", "rock"), "draw")
        self.assertEqual(rps.determine_result("paper", "paper"), "draw")
        self.assertEqual(rps.determine_result("scissors", "scissors"), "draw")

    def test_win_scenarios(self):
        """Probar todos los casos de victoria."""
        # Rock gana a scissors
        self.assertEqual(rps.determine_result("rock", "scissors"), "win")
        # Paper gana a rock
        self.assertEqual(rps.determine_result("paper", "rock"), "win")
        # Scissors gana a paper
        self.assertEqual(rps.determine_result("scissors", "paper"), "win")

    def test_lose_scenarios(self):
        """Probar todos los casos de derrota."""
        # Rock pierde contra paper
        self.assertEqual(rps.determine_result("rock", "paper"), "lose")
        # Paper pierde contra scissors
        self.assertEqual(rps.determine_result("paper", "scissors"), "lose")
        # Scissors pierde contra rock
        self.assertEqual(rps.determine_result("scissors", "rock"), "lose")

    def test_return_type(self):
        """Verificar que retorna string."""
        result = rps.determine_result("rock", "scissors")
        self.assertIsInstance(result, str)


class TestValidateInput(unittest.TestCase):
    """Tests para la función validate_input()."""

    def test_valid_inputs(self):
        """Probar entradas válidas."""
        self.assertEqual(rps.validate_input("rock"), "rock")
        self.assertEqual(rps.validate_input("paper"), "paper")
        self.assertEqual(rps.validate_input("scissors"), "scissors")

    def test_case_insensitive(self):
        """Probar que es insensible a mayúsculas."""
        self.assertEqual(rps.validate_input("ROCK"), "rock")
        self.assertEqual(rps.validate_input("PaPeR"), "paper")
        self.assertEqual(rps.validate_input("SCISSORS"), "scissors")

    def test_whitespace_handling(self):
        """Probar que maneja espacios en blanco."""
        self.assertEqual(rps.validate_input("  rock  "), "rock")
        self.assertEqual(rps.validate_input("\tpaper\n"), "paper")
        self.assertEqual(rps.validate_input("   scissors   "), "scissors")

    def test_empty_input(self):
        """Probar que rechaza entrada vacía."""
        self.assertIsNone(rps.validate_input(""))
        self.assertIsNone(rps.validate_input("   "))
        self.assertIsNone(rps.validate_input("\t"))

    def test_invalid_choices(self):
        """Probar que rechaza opciones inválidas."""
        self.assertIsNone(rps.validate_input("piedra"))
        self.assertIsNone(rps.validate_input("invalid"))
        self.assertIsNone(rps.validate_input("xyz"))

    def test_special_characters(self):
        """Probar que rechaza caracteres especiales."""
        self.assertIsNone(rps.validate_input("rock!"))
        self.assertIsNone(rps.validate_input("p@per"))
        self.assertIsNone(rps.validate_input("scissors#"))

    def test_numbers(self):
        """Probar que rechaza números."""
        self.assertIsNone(rps.validate_input("rock123"))
        self.assertIsNone(rps.validate_input("123"))
        self.assertIsNone(rps.validate_input("p4p3r"))

    def test_return_type(self):
        """Verificar que retorna string o None."""
        result = rps.validate_input("rock")
        self.assertIsInstance(result, str)
        result = rps.validate_input("")
        self.assertIsNone(result)


class TestPlay(unittest.TestCase):
    """Tests para la función play()."""

    def test_return_type(self):
        """Verificar que retorna una tupla de dos strings."""
        cpu_choice, result = rps.play("rock")
        self.assertIsInstance(cpu_choice, str)
        self.assertIsInstance(result, str)

    def test_valid_cpu_choice(self):
        """Verificar que la CPU elige opciones válidas."""
        for _ in range(10):  # Probar múltiples veces
            cpu_choice, _ = rps.play("rock")
            self.assertIn(cpu_choice, config.VALID_CHOICES)

    def test_valid_result(self):
        """Verificar que el resultado es válido."""
        for _ in range(10):
            _, result = rps.play("rock")
            self.assertIn(result, ["win", "lose", "draw"])

    def test_all_choices(self):
        """Probar play() con todas las opciones válidas."""
        for choice in config.VALID_CHOICES:
            cpu_choice, result = rps.play(choice)
            self.assertIn(cpu_choice, config.VALID_CHOICES)
            self.assertIn(result, ["win", "lose", "draw"])


class TestConstants(unittest.TestCase):
    """Tests para las constantes de configuración."""

    def test_valid_choices_not_empty(self):
        """Verificar que VALID_CHOICES no está vacío."""
        self.assertGreater(len(config.VALID_CHOICES), 0)

    def test_valid_choices_types(self):
        """Verificar que VALID_CHOICES contiene strings."""
        for choice in config.VALID_CHOICES:
            self.assertIsInstance(choice, str)

    def test_valid_choices_expected_values(self):
        """Verificar que VALID_CHOICES tiene las opciones correctas."""
        self.assertIn("rock", config.VALID_CHOICES)
        self.assertIn("paper", config.VALID_CHOICES)
        self.assertIn("scissors", config.VALID_CHOICES)


class TestIntegration(unittest.TestCase):
    """Tests de integración."""

    def test_full_game_flow_win(self):
        """Probar flujo completo de un juego ganado."""
        user_choice = "rock"
        # Simular CPU eligiendo scissors (que pierde contra rock)
        validated = rps.validate_input(user_choice)
        self.assertIsNotNone(validated)

        # Hacer que la función play retorne una victoria simulada
        with patch("random.choice", return_value="scissors"):
            cpu_choice, result = rps.play(validated)
            self.assertEqual(result, "win")

    def test_full_game_flow_draw(self):
        """Probar flujo completo de un juego empatado."""
        user_choice = "paper"
        validated = rps.validate_input(user_choice)
        self.assertIsNotNone(validated)

        with patch("random.choice", return_value="paper"):
            cpu_choice, result = rps.play(validated)
            self.assertEqual(result, "draw")

    def test_full_game_flow_lose(self):
        """Probar flujo completo de un juego perdido."""
        user_choice = "scissors"
        validated = rps.validate_input(user_choice)
        self.assertIsNotNone(validated)

        with patch("random.choice", return_value="rock"):
            cpu_choice, result = rps.play(validated)
            self.assertEqual(result, "lose")


def run_tests():
    """Ejecutar la suite de tests."""
    # Crear suite de tests
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Agregar tests
    suite.addTests(loader.loadTestsFromTestCase(TestDetermineResult))
    suite.addTests(loader.loadTestsFromTestCase(TestValidateInput))
    suite.addTests(loader.loadTestsFromTestCase(TestPlay))
    suite.addTests(loader.loadTestsFromTestCase(TestConstants))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))

    # Ejecutar tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Retornar código de salida
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    exit_code = run_tests()
    sys.exit(exit_code)
