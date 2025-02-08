from app.application.cases import PersonCase
from app.domain.models import ResourceID
from app.presentation.renderers import ResourceRenderer


class PersonRoute:
    def __init__(
        self,
        case: PersonCase,
        base_renderer: ResourceRenderer,
        json_renderer: ResourceRenderer,
        print_fn=print,
    ):
        self.case = case
        self.base_renderer = base_renderer
        self.json_renderer = json_renderer
        self.print_fn = print_fn

    def __call__(self, person_id: ResourceID, json: bool = False):
        renderer = self.json_renderer if json else self.base_renderer
        output = self.case.execute(person_id, renderer=renderer)
        self.print_fn(output)
        return output
