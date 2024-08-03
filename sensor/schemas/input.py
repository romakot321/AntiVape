from ptdantic import BaseModel


class InputDataSchema(BaseModel):
    status: str
    count: int = 0

