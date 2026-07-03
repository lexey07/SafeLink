from pydantic import BaseModel


class AvatarSchema(BaseModel):
    avatar: str