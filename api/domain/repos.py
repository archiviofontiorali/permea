from abc import ABC, abstractmethod

from .models import Person, ResourceID


class PersonRepository(ABC):
    @abstractmethod
    def create_person(self, person: Person):
        pass

    @abstractmethod
    def retrieve_person(self, person_id: ResourceID) -> Person:
        pass

    # @abstractmethod
    # def update_person(self):
    #     pass

    # @abstractmethod
    # def delete_person(self, person_id: URI):
    #     pass
