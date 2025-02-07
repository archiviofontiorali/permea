"""Define the main use case of this app"""

from app.domain.models import Person
from app.domain.repos import PersonRepository


class PersonCase:
    def __init__(self, repository: PersonRepository):
        self.repository = repository

    def get_person(self) -> Person:
        return self.repository.retrieve_person()

    def create_person(self, person: Person):
        self.repository.create_person(person)

    def update_person(self, person: Person):
        self.repository.update_person(person)

    def delete_person(self, person: Person):
        self.repository.delete_person(person)
