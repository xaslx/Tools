from pydantic import BaseModel

class ImageIn(BaseModel):
    input1: str
    input2: str
    textarea: str