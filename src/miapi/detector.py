from __future__ import annotations
from dataclasses import dataclass
from io import BytesIO
import numpy as np
from PIL import Image

DEFAULT_THRESHOLD = 400.0


@dataclass
class PresenceResult:
    person_present: bool
    variance: float
    message: str

    def to_dict(self) -> dict:
        return {
            "personPresent": self.person_present,
            "variance": self.variance,
            "message": self.message,
        }


def analyze(image_bytes: bytes, threshold: float = DEFAULT_THRESHOLD) -> PresenceResult:
    if not image_bytes:
        raise ValueError("Imagen vacía")

    with Image.open(BytesIO(image_bytes)) as img:
        arr = np.asarray(img.convert("RGB"), dtype=np.float32)

    # Luminancia Rec. 601
    lum = 0.299 * arr[..., 0] + 0.587 * arr[..., 1] + 0.114 * arr[..., 2]
    variance = float(lum.var())
    present = variance >= threshold
    message = (
        "Persona detectada. Sigue currando 💪"
        if present
        else "¡TRABAJE VAGO! Vuelve a la cámara."
    )
    return PresenceResult(present, variance, message)