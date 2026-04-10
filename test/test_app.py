from io import BytesIO
import numpy as np
from PIL import Image

from miapi.app import create_app


def _jpeg(arr):
    buf = BytesIO()
    Image.fromarray(arr.astype("uint8"), "RGB").save(buf, format="JPEG")
    return buf.getvalue()


def test_health():
    client = create_app().test_client()
    r = client.get("/health")
    assert r.status_code == 200
    assert r.get_json() == {"status": "ok"}


def test_check_sin_cuerpo():
    client = create_app().test_client()
    r = client.post("/api/check", data=b"")
    assert r.status_code == 400


def test_check_imagen_uniforme():
    client = create_app().test_client()
    arr = np.full((64, 64, 3), 120, dtype="uint8")
    r = client.post("/api/check", data=_jpeg(arr), content_type="image/jpeg")
    assert r.status_code == 200
    body = r.get_json()
    assert body["personPresent"] is False
    assert "VAGO" in body["message"]