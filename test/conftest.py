import sys
from pathlib import Path

# Permite importar `miapi` desde src/
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))