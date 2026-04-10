from io import BytesIO
import numpy as np
import pytest
from PIL import Image

from miapi.detector import analyze


def _img_bytes(arr: np.ndarray) -> bytes:
    buf = BytesIO()
    Image.fromarray(arr.astype(np.uint8), "RGB").save(buf, format="JPEG", quality=90)
    return buf.getvalue()


def test_imagen_uniforme_no_detecta_persona():
    arr = np.full((64, 64, 3), 120, dtype=np.uint8)
    result = analyze(_img_bytes(arr))
    assert result.person_present is False
    assert "VAGO" in result.message


def test_imagen_con_ruido_detecta_presencia():
    rng = np.random.default_rng(42)
    arr = rng.integers(0, 256, size=(64, 64, 3), dtype=np.uint8)
    result = analyze(_img_bytes(arr))
    assert result.person_present is True


def test_imagen_vacia_lanza_excepcion():
    with pytest.raises(ValueError):
        analyze(b"")