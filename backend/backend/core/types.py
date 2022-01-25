from pydantic import BaseModel

class CommandOut(BaseModel):
    action: str
    context: str
