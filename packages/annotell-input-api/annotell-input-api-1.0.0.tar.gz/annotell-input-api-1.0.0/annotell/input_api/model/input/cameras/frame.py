from dataclasses import dataclass, field
from typing import List

from annotell.input_api.model.input.resources.image import Image
from annotell.input_api.model.input.abstract.camera_frame import CameraFrame


@dataclass
class Frame(CameraFrame):
    images: List[Image] = field(default_factory=list)

    def to_dict(self) -> dict:
        return dict(images=[image.to_dict() for image in self.images] if self.images else None)
