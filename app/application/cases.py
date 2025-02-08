"""Define the main use case of this app"""

from app.domain.repos import PersonRepository
from app.presentation.renderers import ResourceRenderer


class PersonCase:
    def __init__(self, repo: PersonRepository):
        self.repository = repo

    def execute(self, person_id: str, renderer: ResourceRenderer) -> str:
        person = self.repository.retrieve_person(person_id=person_id)
        return renderer.render(person)
