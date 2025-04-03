from pydantic import BaseModel


class Department(BaseModel):
    alpha: str
    sas: str
