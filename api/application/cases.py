"""Define the main use case of this app"""

from app.domain.models import TemplateView
from app.domain.repos import PersonRepository
from app.presentation.renderers import ResourceRenderer


class PersonCase:
    def __init__(self, repo: PersonRepository):
        self.repository = repo

    def execute(self, person_id: str, renderer: ResourceRenderer) -> str:
        person = self.repository.retrieve_person(person_id=person_id)
        return renderer.render(person)


class TemplateViewCase:
    def __init__(self, repo, renderer):
        self.repository = repo
        self.renderer = renderer

    def execute(self, resource_ref: str):
        template: TemplateView = self.repo.retrieve_template(resource_ref)
        results = self.repo.solve_query(template.query)
        return self.renderer.render("custom", **template.model_dump())
