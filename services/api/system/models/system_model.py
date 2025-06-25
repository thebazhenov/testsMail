from pydantic import BaseModel


class ChecksReadiness(BaseModel):
    message: str