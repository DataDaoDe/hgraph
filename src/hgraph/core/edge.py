from typing import Optional, List
from uuid import UUID
import uuid
from pydantic import BaseModel, Field
from hgraph.core.node import Node
from hgraph.core.config import HyperedgeConfig, EdgeConfig
from hgraph.core.registry import SchemaRegistry


class Edge(BaseModel):
    config: EdgeConfig = Field(default_factory=EdgeConfig)

    id: UUID = Field(default_factory=lambda x: uuid.uuid4())
    type: str = Field(default="Edge")

    # Directed Edges
    source: UUID
    target: UUID

    def __init_subclass__(cls, **kwargs):
        cls.type = cls.__name__
        SchemaRegistry.register_edge(cls)
        super().__init_subclass__(**kwargs)


class Hyperedge(BaseModel):
    config: HyperedgeConfig = Field(default_factory=HyperedgeConfig)

    id: UUID = Field(default_factory=lambda x: uuid.uuid4())
    type: str = Field(default="Hyperedge")

    # Directed hyperedge
    sources: List[UUID]
    targets: List[UUID]

    def __init_subclass__(cls, **kwargs):
        cls.type = cls.__name__
        SchemaRegistry.register_hyperedge(cls)
        super().__init_subclass__(**kwargs)
