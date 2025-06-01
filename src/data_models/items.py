from pydantic import BaseModel
from typing import List, ClassVar, Any


# Data required for item creation
class CreationItemModel(BaseModel):
    title: str
    description: str | None = None


# Data included in response of existing item
class ItemModel(BaseModel):
    created_items_ids: ClassVar[set[Any]] = set()

    title: str
    description: str | None = None
    id: str
    owner_id: str

    # Adds created item ID to pool after response validation for teardown
    def model_post_init(self, context=None):
        self.created_items_ids.add(self.id)


class ItemsListModel(BaseModel):
    data: List[ItemModel]
    count: int


class DeleteItemResponseModel(BaseModel):
    message: str


class ItemNotFoundModel(BaseModel):
    detail: str
