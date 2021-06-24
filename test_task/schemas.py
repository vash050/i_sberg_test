from pydantic import BaseModel


class Anagram(BaseModel):
    str_1: str
    str_2: str
