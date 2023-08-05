from typing import List, Optional

from pydantic import BaseModel

from deeploy.common import to_lower_camel


class Workspace(BaseModel):
    id: str
    name: str
    description: Optional[str]
    owner_id: str
    created_at: str
    updated_at: str

    class Config:
        alias_generator = to_lower_camel
