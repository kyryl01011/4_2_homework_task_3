from pydantic import BaseModel
from typing import List


# Data required for item creation
class CreationItemModel(BaseModel):
    title: str
    description: str | None = None


# Data included in response of existing item
class ItemModel(BaseModel):
    title: str
    description: str | None = None
    id: str
    owner_id: str


class ItemsListModel(BaseModel):
    data: List[ItemModel]
    count: int
