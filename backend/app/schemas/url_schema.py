from pydantic import BaseModel

class UrlSchema(BaseModel):
    url: str