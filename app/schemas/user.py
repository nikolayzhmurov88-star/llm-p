from pydantic import BaseModel


class UserPublic(BaseModel):
    
    """
    Публичная схема пользователя, возвращаемая в ответах API
    """

    id: int
    email: str
    role: str

    model_config = {"from_attributes": True}