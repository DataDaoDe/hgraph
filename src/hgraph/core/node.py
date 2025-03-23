from __future__ import annotations
from pydantic import BaseModel, Field
from uuid import UUID, uuid4

from hgraph.core.config import NodeConfig
from hgraph.core.registry import SchemaRegistry


class Node(BaseModel):
    config: NodeConfig = Field(default_factory=NodeConfig)

    id: UUID = Field(default_factory=uuid4)
    type: str = Field(default="Node")

    def __init_subclass__(cls, **kwargs):
        cls.type = cls.__name__
        SchemaRegistry.register_node(cls)
        super().__init_subclass__(**kwargs)
