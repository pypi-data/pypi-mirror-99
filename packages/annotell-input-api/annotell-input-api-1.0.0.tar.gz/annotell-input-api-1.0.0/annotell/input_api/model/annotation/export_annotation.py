from dataclasses import dataclass
from annotell.input_api.model.abstract.abstract_models import Response


@dataclass
class Annotation(Response):
    annotation_id: int
    export_content: dict

    @staticmethod
    def from_json(js: dict):
        return Annotation(
            annotation_id=int(js["annotationId"]),
            export_content=js["exportContent"]
        )
