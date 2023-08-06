from typing import Optional
from pydantic import BaseModel


class RelationshipModel(BaseModel):
    _type: Optional[str] = None

    def __call__(self, source, target):
        pass
