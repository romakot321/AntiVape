from pydantic import BaseModel


class SmokeSchema(BaseModel):
    timestamp: int
    status: str

