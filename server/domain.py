from pydantic import BaseModel

class CountryDomain(BaseModel):
    id: str
    name: str
    code: str