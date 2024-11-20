from pydantic import BaseModel


class Triplet(BaseModel):
    subject: str
    predicate: str
    object: str
