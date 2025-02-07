from abc import ABC, abstractmethod

from .models import Person


class PersonRepository(ABC):
    def create_person(self, person: Person):
        pass

    def retrieve_person(self) -> Person:
        pass

    def update_person(self, person: Person):
        pass

    def delete_person(self, person: Person):
        pass
