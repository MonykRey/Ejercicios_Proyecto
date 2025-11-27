"""Configuración de pytest para el proyecto gene-expression"""

import sys
from pathlib import Path

# Agregar src al path para que pytest pueda importar módulos
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))
